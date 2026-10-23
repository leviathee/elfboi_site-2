import { Input, CustomSource, AudioSampleSink, WAVE, MP3, MP4, QTFF, FLAC, OGG, ADTS, MATROSKA, WEBM } from '../vendor/mediabunny-preview.mjs';
import { fromPCM } from './clipped-waveform.mjs';

export const READ_LIMIT = 16 * 1024 * 1024;
const EXCERPT_SECONDS = 6;

export async function decodePreview(file) {
  let bytesRead = 0;
  const input = new Input({ formats: [WAVE, MP3, MP4, QTFF, FLAC, OGG, ADTS, MATROSKA, WEBM],
    source: new CustomSource({ getSize: () => file.size, maxCacheSize: 2 * 1024 * 1024,
      prefetchProfile: 'fileSystem',
      handleUnhandledError: () => {}, // Abandoned prefetches can hit the same read limit.
      read: async (start, end) => {
        if (end - start > READ_LIMIT - bytesRead) throw new Error('Preview read budget exceeded');
        bytesRead += end - start;
        return new Uint8Array(await file.slice(start, end).arrayBuffer());
      }
    }) });
  try {
    const track = await input.getPrimaryAudioTrack();
    if (!track) throw new Error('No audio track');
    const rate = await track.getSampleRate(), channels = await track.getNumberOfChannels();
    if (rate < 8000 || rate > 192000 || channels > 8 || !await track.canDecode()) throw new Error('No preview decoder');
    const sink = new AudioSampleSink(track);
    const first = await track.getFirstTimestamp();
    async function excerpt(start) {
      const pcm = new Float32Array(Math.ceil(EXCERPT_SECONDS * rate));
      let length = 0;
      for await (const sample of sink.samples(first + start, first + start + EXCERPT_SECONDS)) {
        try {
          if (sample.sampleRate !== rate) throw new Error('Changing sample rate');
          const offset = Math.round((sample.timestamp - first - start) * rate);
          const skip = Math.max(0, -offset), dest = Math.max(0, offset);
          const frames = Math.min(sample.numberOfFrames - skip, pcm.length - dest);
          if (frames > 0) {
            sample.copyTo(pcm.subarray(dest, dest + frames), { format: 'f32-planar', planeIndex: 0, frameOffset: skip, frameCount: frames });
            length = Math.max(length, dest + frames);
          }
        } finally { sample.close(); }
      }
      const result = fromPCM(pcm.subarray(0, length), rate);
      result.start += start;
      return result;
    }
    let result = await excerpt(0);
    // Don't scan a long recording just to improve a decoration. A silent opening
    // gets one extra attempt, using metadata duration (never a whole-file scan).
    if (result.peak < 1e-4) {
      try {
        const duration = await input.getDurationFromMetadata();
        if (duration > EXCERPT_SECONDS * 2) {
          const later = await excerpt(Math.min(duration / 2, duration - EXCERPT_SECONDS));
          if (later.peak > result.peak) result = later;
        }
      } catch { /* Keep the first excerpt if seeking is unavailable/too expensive. */ }
    }
    return { ...result, bytesRead };
  } finally { input.dispose(); }
}
