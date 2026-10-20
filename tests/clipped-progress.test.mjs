import { test } from 'node:test';
import assert from 'node:assert/strict';
import { OverallProgress } from '../src/clipped-progress.mjs';

function fixture(duration = 12, fps = 60) {
  const p = new OverallProgress(); p.reset(0);
  let now = 0;
  function update(phase, value = null, extra = {}) {
    const state = ['upload','inspecting','starting'].includes(phase) ? 'created' : phase === 'waiting' ? 'queued' : 'processing';
    p.update({ busy: true, phase, value, durationSeconds: duration,
      job: { state, queue: { jobs_ahead: 1 } }, ...extra }, now);
  }
  function advance(seconds, progress) {
    const start = now, end = now + seconds * 1000;
    let nextPoll = start + 1000;
    while (now < end - 0.00001) {
      const previous = p.value, before = now;
      now = Math.min(end, now + 1000 / fps);
      if (progress && now >= nextPoll) { progress((now - start) / (end - start)); nextPoll += 1000; }
      p.tick(now);
      assert.ok(p.value >= previous - 1e-10, 'bar never rewinds');
      if (!p.finished) {
        assert.ok(p.value < 1, 'unfinished work cannot reach 100%');
        assert.ok(p.value - previous <= 0.08 * (now - before) / 1000 + 1e-9, 'no stage or poll jumps');
      }
    }
  }
  return { p, update, advance, now: () => now };
}

// Saved shared-worker production runs, with representative one-second polling.
// Cold/startup is included in inspection wall time, not GPU inference time.
test('saved cold-run timings keep moving through startup instead of parking near 30%', () => {
  for (const [duration, upload, preparation, inference, saving] of [
    [12, 2.10, 20.38, 1.42, 1.49],
    [180, 30.14, 27.28, 6.20, 3.32],
  ]) {
    const f = fixture(duration);
    f.update('upload', 0); f.advance(upload, value => f.update('upload', value));
    const before = f.p.value;
    f.update('inspecting');
    f.advance(preparation / 2); const halfway = f.p.value;
    f.advance(preparation / 2);
    assert.ok(halfway - before > 0.12);
    assert.ok(f.p.value - halfway > 0.12);
    assert.ok(f.p.value > 0.60 && f.p.value < 0.90);
    f.update('downloading'); f.advance(1);
    f.update('processing', 0); f.advance(inference, value => f.update('processing', value));
    f.update('uploading'); f.advance(saving);
    assert.equal(f.p.text, 'Restoring your audio…');
    f.update('completed', 1, { busy: false, job: { state: 'completed' } });
    f.advance(0.61); assert.equal(f.p.value, 1);
  }
});

test('a long queue continues moving without fixed stage ceilings or a jump on dispatch', () => {
  const f = fixture(); f.update('waiting');
  f.advance(30); const a = f.p.value;
  f.advance(30); const b = f.p.value;
  f.advance(30); const c = f.p.value;
  assert.ok(b - a > 0.05 && c - b > 0.025);
  assert.ok(c > 0.70 && c < 0.94);
  f.update('processing', 0.8);
  assert.equal(f.p.value, c, 'a stage/fraction update only changes the speed');
  f.advance(0.25); assert.ok(f.p.value - c <= 0.02);
  f.advance(3600); assert.ok(f.p.value <= 0.99);
});

test('long audio reserves time for inference and saving; verified duration overrides metadata', () => {
  const short = fixture(12), long = fixture(7200);
  for (const f of [short, long]) { f.update('inspecting'); f.advance(20); }
  assert.ok(short.p.value > long.p.value + 0.35);
  short.update('processing', 0, { durationSeconds: 12, job: { state: 'processing', inspection: { source: { duration_seconds: 7200 } } } });
  assert.equal(short.p.duration, 7200);
  short.advance(10); short.update('processing', 0.02, { durationSeconds: 7200 });
  assert.ok(short.p.remainingSeconds() > 500, 'slow observed chunks replace the faster default throughput');
});

test('measured upload speed changes the remaining estimate without changing the bar position', () => {
  const slow = fixture(), fast = fixture();
  slow.update('upload', 0); fast.update('upload', 0);
  slow.advance(20); fast.advance(2);
  const before = slow.p.value;
  slow.update('upload', 0.25); fast.update('upload', 0.25);
  assert.equal(slow.p.value, before);
  assert.ok(slow.p.remainingSeconds() > fast.p.remainingSeconds() + 40);
  slow.update('upload', 0.1);
  assert.equal(slow.p.fraction, 0.25, 'an older sample does not undo measured progress');
});

test('errors, reconnecting and file reselection freeze both the estimate and its animation', () => {
  const f = fixture(); f.update('inspecting'); f.advance(12);
  for (const pause of [
    { phase: 'reconnecting', text: 'Reconnecting' },
    { error: true, text: 'Upload interrupted' },
    { needsFile: true, text: 'Choose the same file to finish uploading' },
  ]) {
    f.p.update({ busy: true, ...pause }, f.now());
    const frozen = f.p.value, age = f.p.phaseElapsed;
    f.advance(60);
    assert.equal(f.p.value, frozen); assert.equal(f.p.phaseElapsed, age);
    assert.equal(f.p.text, pause.text); assert.equal(f.p.animating, false);
    f.update('inspecting'); f.advance(1);
    assert.ok(f.p.value > frozen);
  }
});

test('fast warm runs and skipped stages finish smoothly without holding the completed result', () => {
  const f = fixture(); f.update('inspecting'); f.advance(2);
  const before = f.p.value;
  f.update('completed', 1, { busy: false, job: { state: 'completed' } });
  assert.equal(f.p.active, false); assert.equal(f.p.text, 'Done');
  assert.equal(f.p.value, before, 'completion starts the final visual fill instead of snapping');
  f.advance(0.3); assert.ok(f.p.value > before && f.p.value < 1);
  // The client emits completion twice; this must not restart the animation.
  f.update('completed', 1, { busy: false, job: { state: 'completed' } });
  f.advance(0.31); assert.equal(f.p.value, 1); assert.equal(f.p.animating, false);
  f.p.reset(f.now()); f.update('starting'); f.advance(0.1);
  assert.ok(f.p.value > 0 && f.p.value < 0.01);
});

test('animation is frame-rate independent and returning from a hidden tab does not jump', () => {
  const values = [30, 60, 144].map(fps => {
    const f = fixture(180, fps); f.update('inspecting'); f.advance(20); return f.p.value;
  });
  assert.ok(Math.max(...values) - Math.min(...values) < 0.002);
  const f = fixture(); f.update('waiting'); f.advance(2);
  const before = f.p.value;
  f.p.tick(f.now() + 120000);
  assert.ok(f.p.value - before <= 0.02);
});
