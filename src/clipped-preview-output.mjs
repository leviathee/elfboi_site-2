import { fromPCM, roundPeaks } from './clipped-waveform.mjs';

// Read only the chosen ~0.4 s of the backend's mono float WAV. This is optional:
// range/CORS failure leaves the input preview in place and never holds a result.
export async function outputPreview(url, window, { signal, fetcher = fetch } = {}) {
  let budget = 256 * 1024;
  async function range(start, length, allowShort = false) {
    if (!Number.isSafeInteger(start) || start < 0 || length < 1 || (budget -= length) < 0) throw new Error('Preview range budget');
    const response = await fetcher(url, { headers: { Range: `bytes=${start}-${start + length - 1}` },
      signal, credentials: 'omit', referrerPolicy: 'no-referrer', priority: 'low' });
    // In particular, never consume a whole file if the server ignores Range.
    if (response.status !== 206) { await response.body?.cancel(); throw new Error('No partial response'); }
    const size = response.headers.get('Content-Length');
    if (size !== null && Number(size) > length) { await response.body?.cancel(); throw new Error('Oversized range'); }
    const reader = response.body.getReader();
    const bytes = new Uint8Array(length);
    let used = 0;
    try {
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        if (used + value.length > length) throw new Error('Oversized range');
        bytes.set(value, used); used += value.length;
      }
    } finally { await reader.cancel(); reader.releaseLock(); }
    if (used !== length && !(allowShort && used >= 12)) throw new Error('Truncated range');
    return bytes.subarray(0, used);
  }
  const header = await range(0, 4096, true);
  async function read(start, length) {
    return start + length <= header.length ? header.subarray(start, start + length) : range(start, length);
  }
  const tag = (b, offset = 0) => String.fromCharCode(...b.subarray(offset, offset + 4));
  const view = b => new DataView(b.buffer, b.byteOffset, b.byteLength);
  if (tag(header) !== 'RIFF' || tag(header, 8) !== 'WAVE') throw new Error('Not a WAV');
  let format;
  for (let offset = 12, chunks = 0; chunks < 64; chunks++) {
    const chunk = await read(offset, 8), length = view(chunk).getUint32(4, true);
    offset += 8;
    if (tag(chunk) === 'fmt ') {
      if (length < 16) throw new Error('Invalid WAV format');
      const fmt = view(await read(offset, Math.min(length, 40)));
      let code = fmt.getUint16(0, true);
      if (code === 65534 && length >= 40) code = fmt.getUint16(24, true);
      format = { code, channels: fmt.getUint16(2, true), rate: fmt.getUint32(4, true),
        align: fmt.getUint16(12, true), bits: fmt.getUint16(14, true) };
    } else if (tag(chunk) === 'data') {
      if (!format || format.code !== 3 || format.channels !== 1 || format.bits !== 32 || format.align !== 4 || format.rate !== 48000) throw new Error('Unexpected output format');
      const start = Math.max(0, Math.round(window.start * format.rate));
      const frames = Math.min(Math.floor(length / 4) - start, Math.round(window.duration * format.rate));
      if (frames <= 0 || !Number.isFinite(frames)) throw new Error('Empty output window');
      const pcm = new Float32Array(frames), data = view(await read(offset + start * 4, frames * 4));
      for (let i = 0; i < frames; i++) pcm[i] = data.getFloat32(i * 4, true);
      return roundPeaks(fromPCM(pcm, format.rate, true).surface);
    }
    offset += length + (length % 2);
  }
  throw new Error('WAV data unavailable');
}
