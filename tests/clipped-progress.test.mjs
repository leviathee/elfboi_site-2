import { test } from 'node:test';
import assert from 'node:assert/strict';
import { OverallProgress } from '../src/clipped-progress.mjs';

const view = (phase, value, state = 'processing') => ({ busy: true, phase, value, job: { state } });

test('one monotonic bar spans upload, preparation, queue, inference and saving', () => {
  const p = new OverallProgress(); p.reset(0);
  let now = 0, previous = 0;
  const advance = (v, seconds = 2) => {
    p.update(v, now);
    for (let i = 0; i < seconds * 60; i++) {
      now += 1000 / 60;
      const value = p.tick(now);
      assert.ok(value >= previous && value < 1);
      assert.equal(p.text, 'Restoring your audio…');
      previous = value;
    }
  };
  advance({ busy: true }); assert.ok(p.value > 0);
  advance(view('upload', 0.5, 'created'));
  advance(view('upload', 1, 'created')); assert.ok(p.value <= 0.20);
  advance(view('inspecting', null, 'created'));
  advance(view('waiting', null, 'queued'));
  advance(view('downloading', null));
  advance(view('processing', 0.5));
  advance(view('processing', 1)); assert.ok(p.value <= 0.93);
  advance(view('encoding', null));
  advance(view('uploading', null));
  p.update(view('completed', 1, 'completed'), now);
  assert.equal(p.value, 1); assert.equal(p.active, false); assert.equal(p.text, 'Done');
});

test('unknown work stays bounded even during very long waits and never finishes early', () => {
  const p = new OverallProgress(); p.reset(0);
  p.update(view('waiting', null, 'queued'), 0);
  p.tick(3600000); assert.ok(p.value <= 0.40);
  p.update(view('processing', 0.1), 3600000);
  p.tick(7200000); assert.ok(p.value <= 0.50);
  p.update(view('uploading', null), 7200000);
  p.tick(10800000); assert.ok(p.value <= 0.99);
});

test('errors, reconnection and file reselection freeze progress; retries cannot rewind it', () => {
  const p = new OverallProgress(); p.reset(0);
  p.update(view('processing', 0.7), 0); p.tick(5000);
  let now = 5000;
  for (const pause of [
    { phase: 'reconnecting', text: 'Reconnecting' },
    { error: true, text: 'Upload interrupted' },
    { needsFile: true, text: 'Choose the same file to finish uploading' },
  ]) {
    p.update({ busy: true, ...pause }, now);
    const frozen = p.value;
    now += 60000; assert.equal(p.tick(now), frozen);
    assert.equal(p.text, pause.text); assert.equal(p.active, false);
    p.update(view('upload', 0, 'created'), now);
    now += 1000; assert.ok(p.tick(now) >= frozen);
  }
});

test('progress eases toward measurements, catches up after hidden tabs, and resets for a new file', () => {
  const p = new OverallProgress(); p.reset(0);
  p.update(view('processing', 0.5), 0);
  const first = p.tick(16);
  assert.ok(first > 0 && first < p.target);
  assert.ok(p.tick(1000) > first);
  p.update(view('completed', 1, 'completed'), 1000);
  assert.equal(p.value, 1);
  p.reset(2000); p.update({ busy: true }, 2000);
  assert.ok(p.tick(2016) < 0.01);
  p.update({ busy: false, text: 'Waiting for a file' }, 3000);
  assert.equal(p.value, 0); assert.equal(p.active, false);
});

test('refresh can initialize the overall bar directly from a running or completed job', () => {
  const p = new OverallProgress(); p.reset(0);
  p.update(view('processing', 0.8), 0);
  assert.ok(p.tick(2000) > 0.8);
  p.update({ busy: false, phase: 'completed', job: { state: 'completed' } }, 2000);
  assert.equal(p.value, 1);
});
