// Presentation estimate, not time remaining. Measured upload/inference progress
// anchors the bar; unknown work advances gradually within a bounded range.
export class OverallProgress {
  constructor() { this.reset(); }
  reset(now = performance.now()) {
    this.value = 0; this.target = 0; this.ceiling = 0; this.seconds = 30;
    this.active = false; this.last = now; this.text = 'Waiting for a file';
  }
  update(view, now = performance.now()) {
    this.tick(now);
    if (view.job?.state === 'completed' || view.phase === 'completed') {
      this.value = this.target = this.ceiling = 1;
      this.active = false; this.text = 'Done'; return;
    }
    if (view.error || view.needsFile || view.phase === 'reconnecting' || view.text === 'Reconnecting') {
      this.active = false; this.text = view.text; return;
    }
    if (!view.busy) { this.reset(now); return; }
    this.active = true; this.text = 'Restoring your audio…';
    let target = 0.01, ceiling = 0.05, seconds = 15;
    const phase = view.phase;
    const fraction = Number.isFinite(view.value) ? Math.max(0, Math.min(1, view.value)) : 0;
    if (phase === 'upload') {
      target = 0.05 + 0.15 * fraction; ceiling = target;
    } else if (view.job?.state === 'queued') {
      target = 0.34; ceiling = 0.40; seconds = 60;
    } else if (phase === 'inspecting' || phase === 'ready') {
      target = 0.20; ceiling = 0.34; seconds = 45;
    } else if (phase === 'processing') {
      target = 0.45 + 0.48 * fraction; ceiling = target;
    } else if (phase === 'encoding' || phase === 'uploading') {
      target = 0.93; ceiling = 0.99; seconds = 30;
    } else if (view.job?.state === 'processing') {
      target = 0.40; ceiling = 0.45;
    }
    // Retries and older server snapshots never rewind the current file's bar.
    this.target = Math.max(this.target, target);
    this.ceiling = Math.max(this.target, ceiling);
    this.seconds = seconds;
  }
  tick(now = performance.now()) {
    const elapsed = Math.max(0, (now - this.last) / 1000);
    this.last = now;
    if (this.active) {
      this.target += (this.ceiling - this.target) * (1 - Math.exp(-elapsed / this.seconds));
      this.value += (this.target - this.value) * (1 - Math.exp(-elapsed / 0.25));
    }
    return this.value;
  }
}
