import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fromPCM, roundPeaks } from '../src/clipped-waveform.mjs';
import { decodePreview, READ_LIMIT } from '../src/clipped-preview-decode.mjs';
import { WaveformPreview } from '../src/clipped-preview.mjs';
import { outputPreview } from '../src/clipped-preview-output.mjs';
import { wav } from './waveform-fixture.mjs';

const tick = () => new Promise(resolve => setImmediate(resolve));
function checkSurface(surface) {
  assert.equal(surface.length, 34);
  for (const row of surface) {
    assert.equal(row.length, 113);
    assert.ok(row.every(v => Number.isFinite(v) && Math.abs(v) <= 1.000001));
  }
}
test('original window scoring prefers sustained audio, preserves signs and normalizes peaks', () => {
  const pcm = new Float32Array(48000 * 6);
  pcm[300] = 1; // A louder isolated transient must lose to a sustained passage.
  for (let i = 48000 * 3; i < 48000 * 4; i++) pcm[i] = .5 * Math.sin(i * .04);
  const result = fromPCM(pcm, 48000);
  assert.ok(result.start >= 3 && result.start < 4);
  assert.equal(result.duration, .408);
  checkSurface(result.surface);
  assert.ok(result.surface.flat().some(v => v < -.9));
  assert.ok(result.surface.flat().some(v => v > .9));
});
test('silence, tiny files and nonfinite input never produce invalid display coordinates', () => {
  for (const pcm of [new Float32Array(5), new Float32Array(4800), Float32Array.of(NaN, Infinity, -.5)]) checkSurface(fromPCM(pcm, 48000).surface);
  assert.throws(() => fromPCM(new Float32Array(), 48000));
});
test('cosmetic rounding only changes the display copy and keeps silence quiet', () => {
  const flat = Array.from({ length: 34 }, () => Array(113).fill(.5));
  const rounded = roundPeaks(flat);
  assert.equal(flat[0][50], .5);
  assert.ok(rounded[0][56] > rounded[0][0]);
  checkSurface(rounded);
  assert.deepEqual(roundPeaks([[0, 0, 0]]), [[0, 0, 0]]);
});
test('PCM preview reads only a bounded excerpt of a long stereo file, using the left channel', async () => {
  const bytes = wav({ seconds: 60, channels: 2 });
  let read = 0;
  const file = { size: bytes.length, slice(start, end) {
    read += end - start;
    assert.ok(read <= READ_LIMIT);
    return new Blob([bytes.subarray(start, end)]);
  }, arrayBuffer() { throw new Error('Full-file read is forbidden'); } };
  const result = await decodePreview(file);
  assert.ok(result.bytesRead < bytes.length / 4);
  checkSurface(result.surface);
  assert.ok(result.surface.flat().some(v => v < -.9)); // Right channel is constant positive.
  const pcm = new Float32Array(48000 * 6);
  for (let i = 0; i < pcm.length; i++) pcm[i] = bytes.readFloatLE(44 + i * 8);
  assert.deepEqual(result.surface, fromPCM(pcm, 48000).surface);
});
test('a silent opening gets one bounded later excerpt; unsupported input fails independently', async () => {
  const result = await decodePreview(new Blob([wav({ seconds: 20, silence: 8 })]));
  assert.ok(result.start >= 10 && result.start < 16);
  assert.ok(result.peak > .4);
  await assert.rejects(decodePreview(new Blob(['not audio'])));
});
test('the read budget stops high-rate multichannel previews before large reads', async () => {
  const size = 200 * 1024 * 1024, header = wav({ seconds: .001, channels: 8, rate: 192000 }).subarray(0, 44);
  header.writeUInt32LE(size - 8, 4); header.writeUInt32LE(size - 44, 40);
  let read = 0;
  const file = { size, slice(start, end) {
    read += end - start; assert.ok(read <= READ_LIMIT);
    const data = new Uint8Array(end - start);
    if (start < header.length) data.set(header.subarray(start, Math.min(end, header.length)));
    return new Blob([data]);
  } };
  await assert.rejects(decodePreview(file), /budget exceeded/);
  assert.ok(read > 0 && read <= READ_LIMIT);
});

function rangeFetcher(bytes, calls = []) {
  return async (_, options) => {
    const [start, end] = options.headers.Range.match(/\d+/g).map(Number);
    calls.push([start, end]);
    // No Content-Range exposure required by production R2 CORS.
    return new Response(bytes.subarray(start, end + 1), { status: 206 });
  };
}
test('completed preview reads the same time window from WAV with odd-sized metadata', async () => {
  const bytes = wav({ seconds: 30, metadata: true }), calls = [];
  const surface = await outputPreview('https://output.test', { start: 12, duration: .408 }, { fetcher: rangeFetcher(bytes, calls) });
  checkSurface(surface);
  assert.equal(calls.length, 2);
  assert.equal(calls[1][0], 66 + 12 * 48000 * 4);
  assert.ok(calls.reduce((n, [start, end]) => n + end - start + 1, 0) < 90_000);
  const pcm = new Float32Array(48000 * .408);
  for (let i = 0; i < pcm.length; i++) pcm[i] = bytes.readFloatLE(calls[1][0] + i * 4);
  assert.deepEqual(surface, roundPeaks(fromPCM(pcm, 48000, true).surface));
});
test('tiny output works; ignored, truncated, oversized or incorrect ranges fail safely', async () => {
  checkSurface(await outputPreview('test', { start: 0, duration: .001 }, { fetcher: rangeFetcher(wav({ seconds: .001 })) }));
  for (const response of [new Response(new Uint8Array(20_000)), new Response('bad', { status: 206 }),
    new Response(new Uint8Array(5000), { status: 206 }), new Response(wav({ channels: 2 }).subarray(0, 4096), { status: 206 })]) {
    await assert.rejects(outputPreview('test', { start: 0, duration: .408 }, { fetcher: async () => response }));
  }
});

function previewFixture(options = {}) {
  const workers = [], surfaces = [];
  const preview = new WaveformPreview({ onSurface: value => surfaces.push(value), workerFactory: () => {
    const worker = { terminated: false, postMessage(file) { this.file = file; }, terminate() { this.terminated = true; } };
    workers.push(worker); return worker;
  }, ...options });
  return { preview, workers, surfaces };
}
test('new files and cancellation discard late worker and output responses', async () => {
  let resolveOutput, outputSignal;
  const f = previewFixture({ readOutput: (_, __, { signal }) => { outputSignal = signal; return new Promise(resolve => { resolveOutput = resolve; }); } });
  f.preview.start('first');
  f.workers[0].onmessage({ data: { surface: 'input' } });
  f.preview.finish(async () => ({ url: 'first-output' }));
  await tick();
  f.preview.start('second');
  assert.equal(outputSignal.aborted, true);
  resolveOutput('stale output');
  f.workers[0].onmessage({ data: { surface: 'stale input' } });
  await tick();
  assert.deepEqual(f.surfaces, ['input']);
  f.preview.clear();
  f.workers[1].onmessage({ data: { surface: 'cancelled input' } });
  assert.deepEqual(f.surfaces, ['input']);
  assert.ok(f.workers.every(worker => worker.terminated));
});
test('completion before preview does not wait; optional output follows once input is ready', async () => {
  const f = previewFixture({ readOutput: async () => 'restored' });
  f.preview.start('file');
  assert.equal(f.preview.finish(async () => ({ url: 'output' })), undefined);
  assert.deepEqual(f.surfaces, []);
  f.workers[0].onmessage({ data: { surface: 'input' } });
  await tick();
  assert.deepEqual(f.surfaces, ['input', 'restored']);
  f.preview.clear();
});
test('worker failure, unavailable workers, deadline and output failure all remain optional', async () => {
  const f = previewFixture({ timeout: 5, readOutput: async () => { throw new Error('CORS'); } });
  f.preview.start('timeout');
  await new Promise(resolve => setTimeout(resolve, 20));
  assert.equal(f.workers[0].terminated, true);
  f.workers[0].onmessage({ data: { surface: 'too late' } });
  assert.deepEqual(f.surfaces, []);
  f.preview.start('error'); f.workers[1].onerror({});
  assert.equal(f.workers[1].terminated, true);
  f.preview.start('valid'); f.workers[2].onmessage({ data: { surface: 'input' } });
  f.preview.finish(async () => ({ url: 'output' }));
  await tick(); assert.deepEqual(f.surfaces, ['input']);
  f.preview.clear();
  const unavailable = previewFixture({ workerFactory: () => { throw new Error('Workers disabled'); } });
  assert.doesNotThrow(() => unavailable.preview.start('file'));
});
