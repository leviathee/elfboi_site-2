// The original display: 34 consecutive 12 ms slices, first channel only,
// geometric-mean RMS window selection, signed peak decimation and normalization.
export const ROWS = 34, COLS = 112;

export function fromPCM(pcm, sampleRate, fixed = false) {
  if (!pcm.length || !Number.isFinite(sampleRate) || sampleRate <= 0) throw new Error('No preview samples');
  const slice = Math.max(1, Math.min(Math.max(64, Math.round(sampleRate * .012)), Math.floor(pcm.length / ROWS)));
  const span = Math.min(pcm.length, slice * ROWS);
  const step = Math.max(1, Math.floor(slice / 24));
  const count = Math.floor(pcm.length / slice);
  let best = 0;
  if (!fixed && count >= ROWS) {
    const logs = new Float64Array(count + 1);
    for (let s = 0; s < count; s++) {
      let acc = 0, n = 0;
      for (let k = s * slice; k < (s + 1) * slice; k += step) {
        const v = Number.isFinite(pcm[k]) ? pcm[k] : 0;
        acc += v * v; n++;
      }
      logs[s + 1] = logs[s] + Math.log(Math.sqrt(acc / n) + 1e-6);
    }
    let score = -Infinity;
    for (let j = 0; j + ROWS <= count; j++) {
      const next = logs[j + ROWS] - logs[j];
      if (next > score) { score = next; best = j * slice; }
    }
  }
  let peak = 1e-6;
  for (let k = best; k < best + span; k++) {
    if (Number.isFinite(pcm[k])) peak = Math.max(peak, Math.abs(pcm[k]));
  }
  const bin = Math.max(1, Math.floor(slice / COLS));
  const surface = Array.from({ length: ROWS }, (_, r) => Array.from({ length: COLS + 1 }, (_, i) => {
    const from = best + r * slice + Math.floor(i / COLS * (slice - bin));
    let hi = 0;
    for (let q = 0; q < bin; q++) {
      const v = pcm[from + q];
      if (Number.isFinite(v) && Math.abs(v) > Math.abs(hi)) hi = v;
    }
    return hi / peak;
  }));
  return { surface, start: best / sampleRate, duration: span / sampleRate, peak };
}

// Original cosmetic rounding, on the tiny display surface only, never the WAV.
export function roundPeaks(surface) {
  const result = surface.map(row => row.slice());
  for (const row of result) {
    for (let i = 0; i < row.length;) {
      const v = row[i];
      if (Math.abs(v) < .05) { i++; continue; }
      let end = i + 1;
      while (end < row.length && Math.abs(row[end] - v) <= .03) end++;
      const len = end - i;
      if (len >= 2) {
        const rise = Math.abs(v) * Math.min(.75, .14 + .09 * len);
        for (let k = 0; k < len; k++) row[i + k] = Math.sign(v) * (Math.abs(v) + rise * Math.sin(Math.PI * (k + 1) / (len + 1)));
      }
      i = end;
    }
  }
  let peak = 1;
  for (const row of result) for (const value of row) peak = Math.max(peak, Math.abs(value));
  return result.map(row => row.map(value => value / peak));
}
