// A time-weighted presentation estimate, not a countdown. Stages change the
// speed, never the position. Defaults come from saved T4 preparation/inference
// runs; observed upload/chunk rates replace them when available.
const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
function remaining(expected, elapsed) {
  // If a wait overruns its estimate, keep moving more slowly instead of
  // exhausting a stage's fixed percentage allocation or racing toward 100%.
  return Math.max(expected - elapsed, expected * 0.25 + Math.max(0, elapsed - expected) * 1.5);
}
export class OverallProgress {
  constructor() { this.reset(); }
  reset(now = performance.now()) {
    this.value = 0; this.rate = 0.02; this.last = now;
    this.active = false; this.finishing = false; this.finished = false;
    this.phase = 'starting'; this.phaseElapsed = 0; this.fraction = 0;
    this.sampleElapsed = 0; this.measuredSeconds = null;
    this.duration = 60; this.ahead = 0; this.text = 'Waiting for a file';
  }
  get animating() { return this.active || this.finishing; }
  update(view, now = performance.now()) {
    this.tick(now);
    if (view.job?.state === 'completed' || view.phase === 'completed') {
      if (!this.finished) {
        this.finished = true; this.finishing = true;
        this.finishFrom = this.value; this.finishElapsed = 0;
      }
      // The download is already available; only the final visual fill eases out.
      this.active = false; this.text = 'Done'; return;
    }
    if (view.phase === 'cancelled') { this.reset(now); this.text = 'Cancelled'; return; }
    if (view.phase === 'cancelling') { this.active = false; this.finishing = false; this.rate = 0; this.text = view.text; return; }
    if (view.error || view.needsFile || view.phase === 'reconnecting' || view.text === 'Reconnecting') {
      this.active = false; this.rate = 0; this.text = view.text; return;
    }
    if (!view.busy) { this.reset(now); return; }
    this.active = true; this.text = 'Restoring your audio…';
    const duration = view.job?.inspection?.source?.duration_seconds || view.job?.actual_seconds || view.durationSeconds;
    if (Number.isFinite(duration) && duration > 0) this.duration = clamp(duration, 1, 7200);
    this.ahead = Math.max(0, view.job?.queue?.jobs_ahead || 0);
    const phase = view.job?.state === 'queued' ? 'queue'
      : view.phase === 'upload' ? 'upload'
      : view.phase === 'inspecting' ? 'preparing'
      : view.phase === 'processing' ? 'inference'
      : ['encoding', 'uploading'].includes(view.phase) ? 'saving'
      : view.phase === 'ready' || view.job?.state === 'processing' ? 'dispatch' : 'starting';
    const fraction = Number.isFinite(view.value) ? clamp(view.value, 0, 1) : 0;
    if (phase !== this.phase) {
      this.phase = phase; this.phaseElapsed = 0; this.sampleElapsed = 0;
      this.fraction = fraction; this.measuredSeconds = null;
    } else if (fraction > this.fraction) {
      const elapsed = this.phaseElapsed - this.sampleElapsed;
      if (elapsed > 0) {
        const seconds = elapsed / (fraction - this.fraction);
        this.measuredSeconds = this.measuredSeconds == null ? seconds : (this.measuredSeconds + seconds) / 2;
      }
      this.fraction = fraction; this.sampleElapsed = this.phaseElapsed;
    }
  }
  remainingSeconds() {
    const preparation = 25 + this.duration / 120;
    const inference = 1 + this.duration / 30;
    const saving = 1 + this.duration / 60;
    if (this.phase === 'starting') return remaining(3, this.phaseElapsed) + preparation + inference + saving;
    if (this.phase === 'upload') {
      const upload = this.measuredSeconds == null ? 3 : this.measuredSeconds * (1 - this.fraction);
      return upload + preparation + inference + saving;
    }
    if (this.phase === 'preparing') return remaining(preparation, this.phaseElapsed) + 2 + inference + saving;
    // Queue position gives a count, not the duration of other people's jobs.
    // Widen that uncertainty as we wait instead of counting it down to zero.
    if (this.phase === 'queue') return 3 + 20 * this.ahead + this.phaseElapsed * 0.5 + inference + saving;
    if (this.phase === 'dispatch') return remaining(2, this.phaseElapsed) + inference + saving;
    if (this.phase === 'inference') {
      const work = (this.measuredSeconds ?? inference) * (1 - this.fraction);
      return remaining(Math.max(0.5, work), this.phaseElapsed - this.sampleElapsed) + saving;
    }
    return remaining(saving, this.phaseElapsed);
  }
  tick(now = performance.now()) {
    const elapsed = Math.max(0, (now - this.last) / 1000);
    this.last = now;
    if (this.finishing) {
      this.finishElapsed += elapsed;
      const fraction = Math.min(1, this.finishElapsed / 0.6);
      this.value = this.finishFrom + (1 - this.finishFrom) * (1 - (1 - fraction) ** 3);
      if (fraction === 1) { this.value = 1; this.finishing = false; }
    } else if (this.active) {
      this.phaseElapsed += elapsed;
      // Age the estimate while hidden, but don't replay minutes of animation
      // as a single jump when the tab returns. Ordinary frames are time-based.
      const dt = Math.min(elapsed, 0.25);
      const desired = Math.min(0.08, (0.99 - this.value) / Math.max(1, this.remainingSeconds()));
      const ease = 1 - Math.exp(-dt / 1.2);
      this.value = Math.min(0.99, this.value + desired * dt + (this.rate - desired) * 1.2 * ease);
      this.rate += (desired - this.rate) * ease;
    }
    return this.value;
  }
}
