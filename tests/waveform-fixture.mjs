// Float-WAV fixture with different left/right channels and optional leading silence.
export function wav({ seconds = 12, rate = 48000, channels = 1, silence = 0, metadata = false } = {}) {
  const frames = Math.round(seconds * rate), extra = metadata ? 22 : 0;
  const bytes = Buffer.alloc(44 + extra + frames * channels * 4);
  bytes.write('RIFF'); bytes.writeUInt32LE(bytes.length - 8, 4); bytes.write('WAVEfmt ', 8);
  bytes.writeUInt32LE(16, 16); bytes.writeUInt16LE(3, 20); bytes.writeUInt16LE(channels, 22);
  bytes.writeUInt32LE(rate, 24); bytes.writeUInt32LE(rate * channels * 4, 28);
  bytes.writeUInt16LE(channels * 4, 32); bytes.writeUInt16LE(32, 34);
  if (metadata) { bytes.write('JUNK', 36); bytes.writeUInt32LE(13, 40); bytes.write('odd metadata!', 44); }
  bytes.write('data', 36 + extra); bytes.writeUInt32LE(frames * channels * 4, 40 + extra);
  for (let i = 0; i < frames; i++) for (let ch = 0; ch < channels; ch++) {
    const sample = i < silence * rate ? 0 : ch ? .5 : Math.max(-.42, Math.min(.42, Math.sin(i * .031) * (.6 + .2 * Math.sin(i * .00003))));
    bytes.writeFloatLE(sample, 44 + extra + (i * channels + ch) * 4);
  }
  return bytes;
}
