import { outputPreview } from './clipped-preview-output.mjs';

// Own the optional work separately from DeclipClient. Terminating the worker
// also bounds a decoder/parser that stalls or encounters an expensive file.
export class WaveformPreview {
  constructor({ onSurface, workerFactory = () => new Worker(new URL('./clipped-preview.worker.mjs', import.meta.url), { type: 'module' }),
    readOutput = outputPreview, timeout = 8000 } = {}) {
    Object.assign(this, { onSurface, workerFactory, readOutput, timeout });
    this.current = null;
  }
  clear() {
    const state = this.current;
    this.current = null;
    if (!state) return;
    clearTimeout(state.timer);
    state.worker?.terminate();
    state.abort.abort();
  }
  start(file) {
    this.clear();
    const state = this.current = { abort: new AbortController() };
    try {
      const worker = state.worker = this.workerFactory();
      const settle = result => {
        if (this.current !== state || !state.worker) return;
        clearTimeout(state.timer); worker.terminate(); state.worker = null;
        state.result = result;
        if (result) this.onSurface(result.surface);
        this.restore(state);
      };
      worker.onmessage = ({ data }) => settle(data);
      worker.onerror = event => { event.preventDefault?.(); settle(null); };
      state.timer = setTimeout(() => settle(null), this.timeout);
      // File structured cloning shares the underlying blob; no full-file copy.
      worker.postMessage(file);
    } catch { this.clear(); }
  }
  finish(getGrant) {
    const state = this.current;
    if (!state || state.getGrant) return;
    state.getGrant = getGrant;
    this.restore(state);
  }
  async restore(state) {
    if (this.current !== state || !state.result || !state.getGrant || state.restoring) return;
    state.restoring = true;
    // The timeout includes the grant, not just fetching/reading audio.
    const timer = setTimeout(() => state.abort.abort(), 5000);
    try {
      const grant = await state.getGrant();
      if (this.current !== state || state.abort.signal.aborted) return;
      const surface = await this.readOutput(grant.url, state.result, { signal: state.abort.signal });
      if (this.current === state && !state.abort.signal.aborted) this.onSurface(surface);
    } catch { /* The render/download is already ready; this is decoration only. */ }
    finally { clearTimeout(timer); }
  }
}
