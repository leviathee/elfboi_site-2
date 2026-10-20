// The website owns presentation; this client owns one durable remote job.
export class ApiError extends Error {
  constructor(message, status = 0, method = 'GET') { super(message); this.status = status; this.method = method; }
}
const ACTIVE_KEY = 'elfboi.declip.active.v1';
const BANK_KEY = 'elfboi.declip.bank.v1';
const retryableInspection = new Set(['unavailable', 'timeout', 'input_changed']);
const terminal = new Set(['completed', 'failed', 'expired']);
export const validId = value => typeof value === 'string' && /^[a-f0-9-]{36}$/.test(value);
function browserStorage() { try { return globalThis.localStorage; } catch { return null; } }
function load(storage, key) { try { return JSON.parse(storage?.getItem(key) || 'null'); } catch { return null; } }
function save(storage, key, value) { try { value ? storage?.setItem(key, JSON.stringify(value)) : storage?.removeItem(key); } catch { /* Private browsing can disable persistence. */ } }
export function readBank(storage = browserStorage()) {
  const rows = load(storage, BANK_KEY);
  return Array.isArray(rows) ? rows.filter(row => validId(row?.id) && typeof row.name === 'string' && Number.isFinite(row.dur) && Number.isFinite(row.expires_at)).slice(0, 10) : [];
}
export function saveBank(rows, storage = browserStorage()) {
  save(storage, BANK_KEY, rows.slice(0, 10).map(({ id, name, dur, out, expires_at }) => ({ id, name, dur, out, expires_at })));
}
export function metadataDuration(file, timeout = 2500) {
  // Metadata only, bounded in time; no decodeAudioData or whole-file reads.
  return new Promise(resolve => {
    const audio = document.createElement('audio');
    const url = URL.createObjectURL(file);
    let timer;
    const finish = () => {
      const duration = Number.isFinite(audio.duration) && audio.duration > 0 ? audio.duration : null;
      clearTimeout(timer); audio.onloadedmetadata = audio.onerror = null;
      audio.removeAttribute('src'); audio.load(); URL.revokeObjectURL(url); resolve(duration);
    };
    audio.preload = 'metadata'; audio.onloadedmetadata = finish; audio.onerror = finish;
    timer = setTimeout(finish, timeout); audio.src = url;
  });
}
export function uploadFile(grant, file, progress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open(grant.method || 'PUT', grant.url);
    xhr.withCredentials = false;
    xhr.timeout = Math.min(1800000, (grant.expires_in || 1800) * 1000);
    for (const [name, value] of Object.entries(grant.headers || {})) xhr.setRequestHeader(name, value);
    xhr.upload.onprogress = event => { if (event.lengthComputable && event.total) progress(event.loaded / event.total); };
    xhr.onload = () => xhr.status >= 200 && xhr.status < 300 ? resolve() : reject(new Error('Upload failed. Retry the same file.'));
    xhr.onerror = xhr.ontimeout = xhr.onabort = () => reject(new Error('Upload interrupted. Retry the same file.'));
    xhr.send(file);
  });
}
export function jobView(job) {
  const phase = job.progress?.stage || job.state;
  const titles = { awaiting_upload: 'Choose the same file to finish uploading', inspecting: 'Checking your audio', ready: 'Preparing your audio',
    downloading: 'Preparing your audio', decoding: 'Preparing your audio', processing: 'Restoring', encoding: 'Preparing download',
    uploading: 'Preparing download', completed: 'Done', failed: 'Restoration failed', expired: 'This file has expired', inspection_failed: 'Audio check needs a retry' };
  let text = titles[phase] || 'Preparing your audio';
  if (job.state === 'queued') text = job.queue?.dispatching ? 'Preparing your audio'
    : job.queue?.jobs_ahead ? `Waiting in queue · ${job.queue.jobs_ahead} ahead` : 'Waiting in queue';
  const total = job.progress?.total_chunks;
  const value = phase === 'processing' && total > 0 ? Math.max(0, Math.min(1, (job.progress.completed_chunks || 0) / total))
    : job.state === 'completed' ? 1 : null;
  if (job.state === 'failed') text = ({ video: 'Choose an audio-only file', channels: 'Choose mono or stereo audio',
    duration: 'Audio must be no longer than two hours', sample_rate: 'Choose audio at 8–192 kHz',
    samples: 'This file contains invalid audio samples' })[job.inspection_error] || 'Restoration failed. Try another file.';
  const warning = job.inspection?.source?.channels === 2 ? 'Using the left channel' : '';
  return { phase, text, value, job, warning, error: job.state === 'failed' || job.state === 'expired' };
}
export class DeclipClient {
  constructor({ base = '/api/declip', fetch: fetcher = globalThis.fetch.bind(globalThis), storage = browserStorage(),
    token = async () => '', upload = uploadFile, duration = metadataDuration,
    wait = ms => new Promise(resolve => setTimeout(resolve, ms)), hidden = () => globalThis.document?.hidden,
    onChange = () => {}, onQuota = () => {}, onComplete = () => {} } = {}) {
    Object.assign(this, { base, fetcher, storage, token, upload, duration, wait, hidden, onChange, onQuota, onComplete });
    const active = load(storage, ACTIVE_KEY);
    this.active = active && (validId(active.id) || (typeof active.request?.request_id === 'string' && active.request.request_id.length >= 16)) ? active : null;
    this.running = false; this.file = null; this.job = null; this.session = null;
  }
  persist() { save(this.storage, ACTIVE_KEY, this.active); }
  emit(view) { this.onChange({ durationSeconds: this.active?.request?.duration_seconds, busy: !!this.active, canRetry: false, canDiscard: false, needsFile: false, ...view }); }
  async api(path, body) {
    const method = body === undefined ? 'GET' : 'POST';
    let response;
    try {
      response = await this.fetcher(this.base + path, { method, credentials: 'same-origin', cache: 'no-store',
        headers: body === undefined ? {} : { 'Content-Type': 'application/json' },
        ...(body === undefined ? {} : { body: JSON.stringify(body) }), signal: AbortSignal.timeout(20000) });
    } catch { throw new ApiError('Reconnecting', 0, method); }
    let data;
    try { data = await response.json(); } catch { throw new ApiError('Service unavailable. Please retry.', response.status >= 400 ? response.status : 502, method); }
    if (!response.ok) throw new ApiError(data.error || 'Request failed. Please retry.', response.status, method);
    return data;
  }
  async refreshQuota() {
    if (!this.quotaRequest) this.quotaRequest = this.api('/session').then(data => {
      this.session = data; this.onQuota(data); return data;
    }).finally(() => { this.quotaRequest = null; });
    return this.quotaRequest;
  }
  async initialize() {
    try {
      await this.refreshQuota();
      if (this.active) {
        if (this.active.id) await this.drive();
        else this.needFile();
      } else if (!this.running) this.emit({ text: 'Waiting for a file', value: 0 });
    } catch (error) { this.problem(error); }
  }
  needFile() {
    this.emit({ phase: 'awaiting_upload', text: 'Choose the same file to finish uploading', needsFile: true, canDiscard: true });
  }
  problem(error) {
    if (error instanceof ApiError && error.status === 410 && this.active?.id && this.job?.state === 'created') {
      this.emit({ text: 'Upload window expired. Discard this upload to choose another file.', error: true, canDiscard: true });
      return;
    }
    if (error instanceof ApiError && [401, 404, 410].includes(error.status)) {
      this.active = null; this.file = null; this.persist();
      this.emit({ text: 'This file is no longer available in this browser', error: true });
      return;
    }
    this.emit({ text: error.message || 'Please retry', error: true, canRetry: true,
      canDiscard: !!this.active && (!this.job || this.job.state === 'created'), needsFile: !!this.active && !this.file && !this.active.uploaded });
  }
  async submit(file) {
    if (!file || this.running) return;
    if (this.active && this.job && this.job.state !== 'created') return;
    this.running = true;
    try {
      if (!this.session) await this.refreshQuota();
      if (file.size <= 0 || file.size > this.session.limits.max_bytes) throw new Error('Choose a file up to 200 MiB');
      if (this.active?.request) {
        const prior = this.active.request;
        if (prior.size !== file.size || prior.filename !== file.name || this.active.lastModified !== file.lastModified) {
          throw new Error('Choose the same file, or discard this upload first');
        }
      } else {
        this.emit({ text: 'Reading the file', busy: true });
        const estimate = await this.duration(file);
        this.active = { request: { request_id: crypto.randomUUID(), filename: file.name, size: file.size,
          duration_seconds: Number.isFinite(estimate) && estimate > 0 && estimate <= this.session.limits.max_seconds ? estimate : null },
          lastModified: file.lastModified, uploaded: false };
        this.persist();
      }
      this.file = file;
      await this.create();
    } catch (error) { this.problem(error); return; }
    finally { this.running = false; }
    await this.drive();
  }
  async create() {
    this.emit({ text: this.active.id ? 'Reconnecting' : 'Preparing your audio' });
    const token = this.active.id || this.session.local ? '' : await this.token();
    const result = await this.api('/jobs', { ...this.active.request, turnstile_token: token });
    this.active.id = result.job.id; this.persist(); this.job = result.job;
    this.grant = result.upload;
    this.refreshQuota().catch(() => {});
  }
  async retry() {
    if (this.running) return;
    if (!this.session) return this.initialize();
    if (!this.active) return this.initialize();
    if (!this.active.id) {
      if (!this.file) return this.needFile();
      this.running = true;
      try { await this.create(); } catch (error) { this.problem(error); return; } finally { this.running = false; }
    }
    this.retryInspection = true;
    await this.drive();
  }
  async drive() {
    if (this.running || !this.active?.id) return;
    this.running = true;
    let failures = 0, quotaState = '';
    try {
      while (this.active?.id) {
        try {
          const { job } = await this.api('/jobs/' + this.active.id);
          this.job = job;
          const nextQuota = job.state + ':' + job.actual_seconds;
          if (quotaState !== nextQuota) { quotaState = nextQuota; this.refreshQuota().catch(() => {}); }
          this.emit(jobView(job));
          if (terminal.has(job.state)) {
            const name = this.active.request?.filename || job.download_name;
            if (job.state === 'completed') this.onComplete({ id: job.id, name, out: job.download_name,
              dur: job.actual_seconds || job.inspection?.source?.duration_seconds || 0, expires_at: job.expires_at }, job);
            this.active = null; this.file = null; this.persist(); this.emit(jobView(job)); return;
          }
          if (job.state === 'created') {
            if (job.inspection_error && !this.retryInspection) {
              this.emit({ ...jobView(job), error: true, canRetry: retryableInspection.has(job.inspection_error), canDiscard: true }); return;
            }
            if (job.inspection) {
              await this.api(`/jobs/${job.id}/start`, { inspection_id: job.inspection.id, acknowledge_conversions: true });
              failures = 0; continue;
            }
            if (job.progress?.stage !== 'inspecting') {
              if (!this.active.uploaded && !job.inspection_error) {
                if (!this.file) { this.needFile(); return; }
                if (!this.grant) await this.create();
                if (this.job.state !== 'created' || this.job.inspection || this.job.progress?.stage === 'inspecting') continue;
                try {
                  await this.upload(this.grant, this.file, value => this.emit({ text: value < 1 ? 'Uploading' : 'Checking your audio', phase: 'upload', value }));
                } catch (error) { this.grant = null; throw error; }
                this.active.uploaded = true; this.persist(); this.grant = null;
              }
              this.retryInspection = false;
              await this.api(`/jobs/${job.id}/inspect`, {});
              failures = 0; continue;
            }
          }
          failures = 0;
          await this.wait(this.hidden() ? 5000 : 1000);
        } catch (error) {
          // A lost response is not a failed restoration. Read the same job before
          // retrying idempotent inspect/start; never create a replacement job.
          if (error instanceof ApiError && (error.status === 0 || (error.method === 'GET' && error.status >= 500))) {
            this.emit({ text: 'Reconnecting', phase: 'reconnecting', job: this.job });
            await this.wait(Math.min(15000, (this.hidden() ? 5000 : 1000) * 2 ** Math.min(failures++, 4)));
            continue;
          }
          this.problem(error); return;
        }
      }
    } finally { this.running = false; }
  }
  async abandon() {
    if (this.running || !this.active) return;
    this.running = true;
    try {
      if (!this.active.id) {
        // Resolve an uncertain create response without a fresh challenge. An
        // already-created job is returned before Turnstile validation.
        try { const result = await this.api('/jobs', { ...this.active.request, turnstile_token: '' }); this.active.id = result.job.id; this.persist(); }
        catch (error) { if (!(error instanceof ApiError && [400, 403].includes(error.status))) throw error; }
      }
      if (this.active.id) await this.api(`/jobs/${this.active.id}/abandon`, {});
      this.active = null; this.file = null; this.job = null; this.grant = null; this.persist();
      this.emit({ text: 'Waiting for a file', value: 0 });
      await this.refreshQuota();
    } catch (error) { this.problem(error); } finally { this.running = false; }
  }
  async download(id) {
    if (!validId(id)) throw new Error('This file is unavailable');
    return (await this.api(`/jobs/${id}/download-url`, {})).download;
  }
}
