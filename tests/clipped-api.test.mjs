import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { DeclipClient, jobView, readBank, saveBank } from '../src/clipped-api.mjs';

const id = 'aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa';
const activeKey = 'elfboi.declip.active.v1';
const file = { name: 'voice.flac', size: 256, lastModified: 123 };
function storage() {
  const values = new Map();
  return { getItem: k => values.get(k), setItem: (k,v) => values.set(k,v), removeItem: k => values.delete(k) };
}
function fixture(options = {}) {
  const store = options.storage || storage(), requests = [], views = [], completed = [], waits = [];
  let uploads = 0, creates = 0, inspectPosts = 0, startPosts = 0, statusGets = 0;
  let failCreate = options.failCreate, failStart = options.failStart, failGet = options.failGet, failUpload = options.failUpload;
  let job = { id, state: 'created', progress: { stage: 'awaiting_upload' }, inspection: null, inspection_error: null,
    created_at: 100, expires_at: 9999999999, download_name: 'voice-declipped-mono-48k.wav', ...options.job };
  const inspection = { id: 'inspection', source: { duration_seconds: 12, channels: 2 } };
  const client = new DeclipClient({ storage: store, hidden: () => !!options.hidden,
    duration: options.readDuration || (async () => options.duration ?? null), token: async () => 'challenge',
    onChange: v => views.push(v), onQuota: () => {}, onComplete: row => completed.push(row),
    wait: async ms => {
      waits.push(ms); assert.ok(waits.length < 20, 'polling must converge');
      if (job.progress.stage === 'inspecting') { job.inspection = inspection; job.progress.stage = 'ready'; }
      else if (job.state === 'queued') { job.state = 'processing'; job.progress = { stage: 'processing', completed_chunks: 1, total_chunks: 2 }; }
      else if (job.state === 'processing') { job.state = 'completed'; job.actual_seconds = 12; job.progress = { stage: 'completed', completed_chunks: 2, total_chunks: 2 }; }
    },
    upload: async (grant, uploadedFile, progress) => {
      uploads++; assert.equal(uploadedFile, file); assert.equal(grant.method, 'PUT');
      progress(0.5); progress(1);
      if (failUpload) { failUpload = false; throw new Error('Upload interrupted'); }
    },
    fetch: async (path, init) => {
      const body = init.body ? JSON.parse(init.body) : null;
      requests.push({ path, body, method: init.method });
      assert.equal(init.credentials, 'same-origin'); assert.equal(init.cache, 'no-store');
      const response = (data, status = 200) => Response.json(data, { status });
      if (path.endsWith('/session')) return response({ local: false, limits: { max_bytes: 209715200, max_seconds: 7200, device_seconds_per_day: 21600, device_seconds_reserved_or_used: 12 } });
      if (path === '/api/declip/jobs') {
        creates++;
        if (options.expiredGrant && creates > 1) return response({ error: 'Object access has expired.' }, 410);
        if (failCreate) { failCreate = false; throw new TypeError('lost create response'); }
        return response({ job, upload: { url: 'https://private.test/input', method: 'PUT', headers: {}, expires_in: 1800 } });
      }
      if (path === '/api/declip/jobs/' + id) {
        statusGets++;
        if (options.unavailable) return response({ error: 'Job not found' }, 404);
        if (failGet) { failGet = false; throw new TypeError('offline'); }
        return response({ job });
      }
      if (path.endsWith('/inspect')) {
        inspectPosts++; job.inspection_error = null; job.progress.stage = 'inspecting'; return response({ job }, 202);
      }
      if (path.endsWith('/start')) {
        startPosts++; assert.deepEqual(body, { inspection_id: 'inspection', acknowledge_conversions: true });
        job.state = 'queued'; job.progress.stage = 'waiting'; job.queue = { jobs_ahead: 2, dispatching: false };
        if (failStart) { failStart = false; throw new TypeError('lost start response'); }
        return response({ job });
      }
      if (path.endsWith('/download-url')) return response({ download: { url: 'https://private.test/output?grant=' + requests.length, method: 'GET', headers: {}, expires_in: 900 } });
      if (path.endsWith('/abandon')) { job.state = 'expired'; return response({ job }); }
      throw new Error('Unexpected route: ' + path);
    },
  });
  return { client, store, views, requests, completed, waits, get counts() { return { uploads, creates, inspectPosts, startPosts, statusGets }; } };
}
function saveActive(store, extra = {}) {
  store.setItem(activeKey, JSON.stringify({ id, request: { request_id: 'frozen-request-id', filename: file.name, size: file.size, duration_seconds: null }, lastModified: file.lastModified, uploaded: true, ...extra }));
}
test('original file follows create/upload/async inspection/start; only the real completed job enters the bank', async () => {
  const f = fixture(); await f.client.submit(file);
  assert.deepEqual({ ...f.counts, statusGets: 0 }, { creates: 1, uploads: 1, inspectPosts: 1, startPosts: 1, statusGets: 0 });
  assert.equal(f.requests.find(r => r.path.endsWith('/jobs')).body.duration_seconds, null);
  assert.equal(f.completed.length, 1); assert.equal(f.completed[0].out, 'voice-declipped-mono-48k.wav');
  assert.equal(f.client.active, null); assert.equal(f.store.getItem(activeKey), undefined);
  assert.ok(f.views.some(v => v.warning === 'Using the left channel'));
  assert.ok(f.views.some(v => v.phase === 'processing' && v.value === 0.5));
  assert.equal(f.views.at(-1).busy, false);
});
test('refresh and a dropped connection resume the saved job without uploading or creating again', async () => {
  const store = storage(); saveActive(store);
  const f = fixture({ storage: store, failGet: true, hidden: true, job: { progress: { stage: 'inspecting' } } });
  await f.client.initialize();
  assert.equal(f.counts.creates, 0); assert.equal(f.counts.uploads, 0); assert.equal(f.counts.startPosts, 1);
  assert.equal(f.completed.length, 1); assert.ok(f.views.some(v => v.text === 'Reconnecting'));
  assert.ok(f.waits.every(ms => ms >= 5000));
});
test('a lost start response polls the same job and does not start or create another', async () => {
  const f = fixture({ failStart: true }); await f.client.submit(file);
  assert.equal(f.counts.startPosts, 1); assert.equal(f.counts.creates, 1); assert.equal(f.completed.length, 1);
  assert.ok(f.views.some(v => v.text === 'Reconnecting'));
});
test('a lost create response retains request metadata for an explicit retry', async () => {
  const f = fixture({ failCreate: true, duration: 12 }); await f.client.submit(file);
  assert.equal(f.completed.length, 0); assert.equal(f.views.at(-1).canRetry, true);
  const pending = JSON.parse(f.store.getItem(activeKey)); assert.equal(pending.request.duration_seconds, 12);
  await f.client.retry();
  const creates = f.requests.filter(r => r.path === '/api/declip/jobs');
  assert.equal(creates.length, 2); assert.deepEqual(creates[0].body, creates[1].body);
  assert.equal(f.completed.length, 1);
});
test('inspection failures stop until explicit retry; they do not create a replacement job', async () => {
  const store = storage(); saveActive(store);
  const f = fixture({ storage: store, job: { inspection_error: 'timeout', progress: { stage: 'inspection_failed' } } });
  await f.client.initialize(); assert.equal(f.counts.inspectPosts, 0); assert.equal(f.views.at(-1).canRetry, true);
  await f.client.retry(); assert.equal(f.counts.inspectPosts, 1); assert.equal(f.counts.creates, 0); assert.equal(f.completed.length, 1);
});
test('an interrupted upload retries the same bytes and reaches inspection only after successful PUT', async () => {
  const f = fixture({ failUpload: true }); await f.client.submit(file);
  assert.equal(f.counts.inspectPosts, 0); assert.equal(f.views.at(-1).canRetry, true);
  await f.client.retry(); assert.equal(f.counts.uploads, 2); assert.equal(f.counts.inspectPosts, 1); assert.equal(f.completed.length, 1);
});
test('refresh before PUT requires the same file; discard releases the known job', async () => {
  const store = storage(); saveActive(store, { uploaded: false });
  const f = fixture({ storage: store }); await f.client.initialize();
  assert.equal(f.views.at(-1).needsFile, true); assert.equal(f.counts.creates, 0);
  await f.client.submit({ ...file, name: 'different.wav' }); assert.equal(f.counts.creates, 0);
  await f.client.abandon(); assert.equal(f.client.active, null);
  assert.equal(f.requests.filter(r => r.path.endsWith('/abandon')).length, 1);
});
test('loss of ownership clears the local active reference without creating another job', async () => {
  const store = storage(); saveActive(store);
  const f = fixture({ storage: store, unavailable: true }); await f.client.initialize();
  assert.equal(f.client.active, null); assert.equal(f.counts.creates, 0); assert.equal(f.views.at(-1).error, true);
});
test('download gets fresh grants and bank persistence never stores signed URLs or buffers', async () => {
  const f = fixture(); const a = await f.client.download(id), b = await f.client.download(id); assert.notEqual(a.url, b.url);
  saveBank([{ id, name: '<script>.wav', dur: 12, out: 'output.wav', expires_at: 9999999999, url: a.url, _buf: [1,2] }], f.store);
  assert.deepEqual(readBank(f.store), [{ id, name: '<script>.wav', dur: 12, out: 'output.wav', expires_at: 9999999999 }]);
});
test('queue and saving are indeterminate, independently of restoration progress', () => {
  assert.equal(jobView({ state: 'queued', queue: { jobs_ahead: 3 } }).text, 'Waiting in queue · 3 ahead');
  assert.equal(jobView({ state: 'processing', progress: { stage: 'uploading', completed_chunks: 2, total_chunks: 2 } }).value, null);
  assert.equal(jobView({ state: 'processing', progress: { stage: 'processing', completed_chunks: 2, total_chunks: 2 } }).value, 1);
});
test('Vercel exposes only the website API surface and overwrites the server-only proxy secret', () => {
  const config = JSON.parse(readFileSync(new URL('../vercel.json', import.meta.url), 'utf8'));
  const route = config.routes[0], pattern = new RegExp(route.src);
  for (const path of ['health', 'session', 'jobs', `jobs/${id}`, `jobs/${id}/start`, `jobs/${id}/download-url`]) assert.ok(pattern.test('/api/declip/' + path));
  for (const path of ['internal/modal/' + id + '/claim', 'local/objects/' + id, `jobs/${id}/preview-urls`, 'session/extra', 'healthx']) assert.equal(pattern.test('/api/declip/' + path), false, path);
  assert.equal(route.transforms[0].type, 'request.headers'); assert.equal(route.transforms[0].op, 'set');
  assert.deepEqual(route.transforms[0].env, ['DECLIP_PROXY_SECRET']);
  assert.equal(config.buildCommand, 'python3 build.py');
});

test('an expired upload grant keeps the job available for discard and quota release', async () => {
  const f = fixture({ failUpload: true, expiredGrant: true }); await f.client.submit(file);
  await f.client.retry();
  assert.equal(f.client.active.id, id);
  assert.equal(f.views.at(-1).canDiscard, true);
  assert.equal(f.views.at(-1).canRetry, false);
  await f.client.abandon(); assert.equal(f.client.active, null);
});


test('initial session loading cannot reset the UI while a dropped file is being read', async () => {
  let release, entered;
  const started = new Promise(resolve => { entered = resolve; });
  const metadata = new Promise(resolve => { release = resolve; });
  const f = fixture({ readDuration: () => { entered(); return metadata; } });
  const initializing = f.client.initialize();
  const submitting = f.client.submit(file);
  await started;
  await initializing;
  assert.equal(f.views.some(v => v.text === 'Waiting for a file'), false);
  release(12);
  await submitting;
  assert.equal(f.completed.length, 1);
});

function deferred() {
  let resolve, reject;
  const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
}
function cancelFixture(options = {}) {
  const f = fixture(options), fetcher = f.client.fetcher;
  let attempts = 0;
  f.client.fetcher = async (path, init) => {
    if (path.endsWith('/cancel')) {
      f.requests.push({ path, body: {}, method: 'POST' });
      if (options.failCancel && attempts++ === 0) throw new TypeError('offline');
      return Response.json({ job: options.completed ? { id, state: 'completed', actual_seconds: 12, expires_at: 9999999999, download_name: 'restored.wav' }
        : { id, state: 'expired', error: 'job_cancelled' } });
    }
    return fetcher(path, init);
  };
  return f;
}
test('cancel while reading metadata stops before creating or uploading and allows a fresh file', async () => {
  const entered = deferred(), metadata = deferred();
  const f = cancelFixture({ readDuration: () => { entered.resolve(); return metadata.promise; } });
  const submitting = f.client.submit(file); await entered.promise;
  await f.client.cancel(); await submitting;
  assert.equal(f.counts.creates, 0); assert.equal(f.counts.uploads, 0);
  assert.equal(f.views.at(-1).phase, 'cancelled'); assert.equal(f.views.at(-1).busy, false);
  metadata.resolve(12); await Promise.resolve();
  assert.equal(f.client.active, null);
  f.client.duration = async () => 12; await f.client.submit(file);
  assert.equal(f.completed.length, 1);
});
test('cancel aborts an in-flight upload and never starts inspection', async () => {
  const entered = deferred(); const f = cancelFixture(); let aborted = false;
  f.client.upload = (grant, file, progress, signal) => new Promise((resolve, reject) => {
    signal.addEventListener('abort', () => { aborted = true; reject(new DOMException('Cancelled', 'AbortError')); });
    entered.resolve();
  });
  const submitting = f.client.submit(file); await entered.promise;
  await f.client.cancel(); await submitting;
  assert.equal(aborted, true); assert.equal(f.counts.inspectPosts, 0);
  assert.equal(f.completed.length, 0); assert.equal(f.client.active, null);
  assert.equal(f.requests.filter(r=>r.path.endsWith('/cancel')).length, 1);
});
test('cancel waits for an in-flight create and cancels that exact job', async () => {
  const entered = deferred(), release = deferred(); const f = cancelFixture(); const fetcher=f.client.fetcher;
  f.client.fetcher=async (path,init)=> {
    if (path === '/api/declip/jobs') { entered.resolve(); await release.promise; }
    return fetcher(path,init);
  };
  const submitting=f.client.submit(file); await entered.promise;
  const cancelling=f.client.cancel();
  assert.equal(f.views.at(-1).phase,'cancelling');
  release.resolve(); await cancelling; await submitting;
  assert.equal(f.counts.uploads,0); assert.equal(f.counts.creates,1);
  assert.equal(f.requests.filter(r=>r.path.endsWith('/cancel')).length,1);
  assert.equal(f.client.active,null);
});
test('cancelling preparation, queueing and inference interrupts polling without creating replacement jobs', async () => {
  for (const state of ['created','queued','processing']) {
    const store=storage(); saveActive(store);
    const f=cancelFixture({storage:store,job:{state,progress:{stage:state==='created'?'inspecting':state}}});
    const entered=deferred(); f.client.wait=()=>{entered.resolve();return new Promise(()=>{});};
    const initializing=f.client.initialize();await entered.promise;
    await f.client.cancel();await initializing;
    assert.equal(f.completed.length,0);assert.equal(f.counts.creates,0);assert.equal(f.client.active,null);
    assert.equal(f.views.at(-1).text,'Cancelled');
  }
});
test('failed cancellation survives refresh and resumes cancellation instead of restoration', async () => {
  const store=storage();saveActive(store);
  const f=cancelFixture({storage:store,failCancel:true});await f.client.cancel();
  assert.equal(JSON.parse(store.getItem(activeKey)).cancelRequested,true);
  assert.equal(f.views.at(-1).canRetry,true);
  const resumed=cancelFixture({storage:store});await resumed.client.initialize();
  assert.equal(resumed.counts.startPosts,0);assert.equal(resumed.counts.statusGets,0);
  assert.equal(resumed.client.active,null);assert.equal(store.getItem(activeKey),undefined);
});
test('a completed result winning the cancellation race is preserved in the bank', async () => {
  const store=storage();saveActive(store);
  const f=cancelFixture({storage:store,completed:true});await f.client.cancel();
  assert.equal(f.completed.length,1);assert.equal(f.completed[0].id,id);
  assert.equal(f.views.at(-1).phase,'completed');assert.equal(f.client.active,null);
});
test('uncertain create is resolved using the same request before cancellation', async () => {
  const f=cancelFixture({failCreate:true});await f.client.submit(file);await f.client.cancel();
  const creates=f.requests.filter(r=>r.path==='/api/declip/jobs');
  assert.equal(creates.length,2);assert.equal(creates[0].body.request_id,creates[1].body.request_id);
  assert.equal(creates[1].body.turnstile_token,'');assert.equal(f.counts.uploads,0);
  assert.equal(f.client.active,null);
});
test('cancel is allowed through the website proxy, while internal cancellation checks remain private', () => {
  const config=JSON.parse(readFileSync(new URL('../vercel.json',import.meta.url),'utf8'));
  const pattern=new RegExp(config.routes[0].src);
  assert.ok(pattern.test(`/api/declip/jobs/${id}/cancel`));
  assert.equal(pattern.test(`/api/declip/internal/modal/${id}/cancel-check`),false);
});

test('cancel during verification aborts the token wait and never uploads', async () => {
  const f=cancelFixture(), entered=deferred(); let aborted=false;
  f.client.token=signal=>new Promise((resolve,reject)=>{
    signal.addEventListener('abort',()=>{aborted=true;reject(new DOMException('Cancelled','AbortError'));});
    entered.resolve();
  });
  const submitting=f.client.submit(file);await entered.promise;
  await f.client.cancel();await submitting;
  assert.equal(aborted,true);assert.equal(f.counts.uploads,0);assert.equal(f.counts.inspectPosts,0);
  assert.equal(f.client.active,null);
});
test('a stale polling response after cancel cannot start inference or overwrite the cancelled state', async () => {
  const store=storage();saveActive(store);const f=cancelFixture({storage:store});
  const entered=deferred(),release=deferred(),fetcher=f.client.fetcher;
  f.client.fetcher=async(path,init)=>{
    if(path==='/api/declip/jobs/'+id){entered.resolve();await release.promise;return Response.json({job:{id,state:'created',inspection:{id:'inspection'}}});}
    return fetcher(path,init);
  };
  const initializing=f.client.initialize();await entered.promise;
  const cancelling=f.client.cancel();release.resolve();await cancelling;await initializing;
  assert.equal(f.counts.startPosts,0);assert.equal(f.views.at(-1).phase,'cancelled');
});
test('retry after uncertain cancellation keeps cancelling rather than restarting work', async () => {
  const store=storage();saveActive(store);const f=cancelFixture({storage:store,failCancel:true});
  await f.client.cancel();await f.client.retry();
  assert.equal(f.requests.filter(r=>r.path.endsWith('/cancel')).length,2);
  assert.equal(f.counts.statusGets,0);assert.equal(f.client.active,null);
});
