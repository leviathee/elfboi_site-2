import { roundPeaks } from './clipped-waveform.mjs';

const copy = surface => surface.map(row => row.slice());
const clamp = (value, limit) => Math.max(-limit, Math.min(limit, value));

// Display-only reconstruction. Keep the input immutable and give progress a
// rounded destination immediately; the real output replaces that destination
// later without changing the audio or waiting to make its download available.
export class WaveformAnimation {
  constructor(idle, clip = .34) {
    this.source = idle;
    this.surface = copy(idle);
    this.clip = clip;
    this.target = null;
    this.fade = null;
    this.progress = 0;
  }
  set(surface, { kind = 'input', progress = 0, now = performance.now(), immediate = false } = {}) {
    // Capture the current interpolated shape, including an unfinished fade.
    this.tick(progress, now);
    this.fade = immediate ? null : { from: copy(this.surface), start: now, duration: kind === 'result' ? 650 : 350 };
    if (kind === 'result') this.target = surface;
    else {
      this.source = surface;
      this.target = kind === 'input' ? roundPeaks(surface) : null;
    }
    this.tick(progress, now);
  }
  get animating() { return this.fade !== null; }
  tick(progress, now) {
    const p = Math.max(0, Math.min(1, progress));
    // Cancellation/new-file resets must not carry tall completed peaks into
    // the clipped state (including its height-based color ramp).
    if (p < this.progress) this.fade = null;
    this.progress = p;
    const ceiling = this.clip + (1 - this.clip) * p;
    const t = this.fade ? Math.max(0, Math.min(1, (now - this.fade.start) / this.fade.duration)) : 1;
    const blend = t * t * (3 - 2 * t);
    for (let r = 0; r < this.surface.length; r++) {
      for (let i = 0; i < this.surface[r].length; i++) {
        const input = this.source[r][i];
        const start = clamp(input, this.clip);
        // Morph directly from the clipped surface to the rounded one. Clamping
        // again afterward would keep the rebuilding peaks flat until the end.
        const desired = this.target ? start + (this.target[r][i] - start) * p : clamp(input, ceiling);
        this.surface[r][i] = this.fade ? this.fade.from[r][i] + (desired - this.fade.from[r][i]) * blend : desired;
      }
    }
    if (t === 1) this.fade = null;
    return this.surface;
  }
}
