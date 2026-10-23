import { test } from 'node:test';
import assert from 'node:assert/strict';
import { WaveformAnimation } from '../src/clipped-waveform-animation.mjs';
import { roundPeaks } from '../src/clipped-waveform.mjs';

const copy = surface => surface.map(row => row.slice());
function near(actual, expected) {
  assert.equal(actual.length, expected.length);
  for (let r = 0; r < actual.length; r++) {
    assert.equal(actual[r].length, expected[r].length);
    for (let i = 0; i < actual[r].length; i++) assert.ok(Math.abs(actual[r][i] - expected[r][i]) < 1e-12);
  }
}
const input = [[0, .8, .8, .8, .8, .8, 0], [0, -.8, -.8, -.8, -.8, -.8, 0]];
const idle = input.map(row => row.map(() => 0));
const result = [[0, .2, .7, 1, .65, .3, 0], [0, -.3, -.6, -.9, -.7, -.2, 0]];

test('clipped plateaus grow into rounded peaks throughout progress without changing input', () => {
  const source = copy(input), before = copy(source), animation = new WaveformAnimation(idle);
  animation.set(source, { now: 0, immediate: true });
  assert.deepEqual(animation.tick(0, 0)[0], [0, .34, .34, .34, .34, .34, 0]);
  for (const progress of [.1, .3, .6, .9]) {
    const surface = animation.tick(progress, progress * 10000);
    assert.ok(surface[0][3] > surface[0][1], 'curvature should appear before completion');
    assert.ok(surface[0][3] > .34);
    assert.ok(surface[1][3] < surface[1][1]);
    assert.ok(surface.flat().every(value => Number.isFinite(value) && Math.abs(value) <= 1));
  }
  near(animation.tick(1, 10000), roundPeaks(input));
  assert.deepEqual(source, before);
});
test('a late real result starts from exactly the displayed shape and settles without delaying completion', () => {
  const animation = new WaveformAnimation(idle);
  animation.set(input, { now: 0, immediate: true });
  const before = copy(animation.tick(1, 2000));
  animation.set(result, { kind: 'result', progress: 1, now: 2000 });
  assert.deepEqual(animation.surface, before);
  const halfway = copy(animation.tick(1, 2325));
  for (let r = 0; r < result.length; r++) for (let i = 0; i < result[r].length; i++)
    assert.ok(Math.abs(halfway[r][i] - (before[r][i] + result[r][i]) / 2) < 1e-12);
  assert.equal(animation.animating, true);
  near(animation.tick(1, 2650), result);
  assert.equal(animation.animating, false);
});
test('real output arriving during the final progress ramp is continuous and reaches the result', () => {
  const animation = new WaveformAnimation(idle);
  animation.set(input, { now: 0, immediate: true });
  const before = copy(animation.tick(.96, 1000));
  animation.set(result, { kind: 'result', progress: .96, now: 1000 });
  assert.deepEqual(animation.surface, before);
  const next = animation.tick(.97, 1016);
  assert.ok(next.flat().every((v, i) => Math.abs(v - before.flat()[i]) < .01));
  near(animation.tick(1, 1700), result);
});
test('late previews and replacement during a fade blend from the current frame', () => {
  const animation = new WaveformAnimation(input);
  const initial = copy(animation.tick(1, 100));
  animation.set(input, { progress: 1, now: 100 });
  assert.deepEqual(animation.surface, initial);
  const midway = copy(animation.tick(1, 275));
  animation.set(result, { kind: 'result', progress: 1, now: 275 });
  assert.deepEqual(animation.surface, midway);
  near(animation.tick(1, 925), result);
  animation.set(idle, { kind: 'idle', progress: 0, now: 1000 });
  assert.deepEqual(animation.tick(0, 1350), idle);
});
test('fallback retains the original clipping ceiling; reduced motion skips shape fades', () => {
  const animation = new WaveformAnimation(input);
  for (const progress of [0, .5, 1]) {
    const limit = .34 + .66 * progress;
    near(animation.tick(progress, 0), input.map(row => row.map(value => Math.max(-limit, Math.min(limit, value)))));
  }
  animation.set(input, { progress: .5, now: 0, immediate: true });
  const frozen = copy(animation.tick(.5, 0));
  assert.deepEqual(animation.tick(.5, 60000), frozen);
  assert.equal(animation.animating, false);
  animation.set(result, { kind: 'result', progress: 1, now: 60000, immediate: true });
  near(animation.surface, result);
});
test('shape transitions are time based and reuse the display buffers across frames', () => {
  const samples = [];
  for (const hz of [30, 60, 120]) {
    const animation = new WaveformAnimation(idle);
    animation.set(input, { now: 0 });
    const buffer = animation.surface, row = buffer[0];
    for (let t = 0; t < 250; t += 1000 / hz) animation.tick(.5, t);
    samples.push(copy(animation.tick(.5, 250)));
    assert.equal(animation.surface, buffer);
    assert.equal(animation.surface[0], row);
  }
  assert.deepEqual(samples[0], samples[1]);
  assert.deepEqual(samples[1], samples[2]);
});
test('resetting progress during a result blend restores the clipped height bounds', () => {
  const animation = new WaveformAnimation(idle);
  animation.set(input, { progress: 1, now: 0, immediate: true });
  animation.set(result, { kind: 'result', progress: 1, now: 1000 });
  animation.tick(1, 1200);
  const reset = animation.tick(0, 1201);
  assert.ok(reset.flat().every(value => Math.abs(value) <= .34));
  assert.equal(animation.animating, false);
});
