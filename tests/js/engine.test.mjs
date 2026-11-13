import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DATA } from '../../web/trial-finder/data.js';
import { assess, evalTest, nextQuestion, rank, reqStatus } from '../../web/trial-finder/engine.js';

const fact = (value, source = 'You said') => (typeof value === 'object' ? { ...value, source } : { value, source });

test('ranges settle a limit only when the whole range is on one side', () => {
  const t = ['hba1c', 'between', [7, 10.5]];
  assert.equal(evalTest(t, { hba1c: { lo: 8, hi: 8.99 } }), true);
  assert.equal(evalTest(t, { hba1c: { lo: 10.51, hi: 25 } }), false);
  assert.equal(evalTest(['hba1c', '>=', 7.5], { hba1c: { lo: 7, hi: 7.99 } }), null);
  assert.equal(evalTest(['age', '>', 40], { age: { lo: 40, hi: 54.99 } }), null);
  assert.equal(evalTest(['age', '>', 40], { age: { lo: 41, hi: 41 } }), true);
});

test('unsure and private answers never pass or fail a line', () => {
  for (const state of ['unsure', 'private']) {
    assert.equal(evalTest(['pancreatitis', 'is', 'no'], { pancreatitis: { state } }), null);
  }
  const req = { test: ['pancreatitis', 'is', 'no'] };
  assert.equal(reqStatus(req, {}), 'ask');
  assert.equal(reqStatus(req, { pancreatitis: { state: 'unsure' } }), 'team');
});

test('all, any, map and team combine with three-valued logic', () => {
  const t = ['any', [['bmi', '>=', 30], ['all', [['bmi', '>=', 27], ['team']]]]];
  assert.equal(evalTest(t, { bmi: { lo: 31, hi: 31 } }), true);
  assert.equal(evalTest(t, { bmi: { lo: 28, hi: 28 } }), null);
  assert.equal(evalTest(t, { bmi: { lo: 25, hi: 25 } }), false);
  const m = ['glp1', 'map', { no: true, now: false }];
  assert.equal(evalTest(m, { glp1: fact('recent') }), null);
  assert.equal(evalTest(m, { glp1: fact('now') }), false);
});

test('the match number counts study-team lines as not confirmed', () => {
  const trial = DATA.trials.find(t => t.id === 'NCT07351058');
  const facts = { age: { lo: 58, hi: 58 }, hba1c: { lo: 8.1, hi: 8.1 }, treatment_stable: fact('yes'), insulin: fact('no'),
    bmi: { lo: 31.4, hi: 31.4 }, weight_attempt: fact('yes'), t1d_dka: fact('no'), severe_hypo: fact('no'),
    weight_stable: fact('under3'), obesity_surgery: fact('no'), recent_cv: fact('no'), glp1: fact('no') };
  const r = assess(trial, facts);
  assert.equal(r.notmet, 0);
  assert.equal(r.met, r.canCheck);
  assert.ok(r.team > 0);
  assert.equal(r.percent, Math.round((100 * r.met) / r.total));
  assert.ok(r.percent < 100);
});

test('the next question is the one that settles lines in the most live trials', () => {
  const facts = { area: fact('east_van'), years_dx: { lo: 5, hi: 9.99 } };
  const q = nextQuestion(DATA, facts, 't2d');
  assert.ok(q);
  for (const key of Object.keys(DATA.questions)) {
    if (facts[key] || key === q.fact) continue;
    const other = nextQuestion(DATA, facts, 't2d', [q.fact]);
    assert.ok(!other || other.trials <= q.trials);
    break;
  }
  facts[q.fact] = { state: 'private' };
  assert.notEqual(nextQuestion(DATA, facts, 't2d')?.fact, q.fact);
});

test('a failed line moves a trial to not a fit, and distance sorting works', () => {
  const facts = { area: fact('fraser_valley'), insulin: fact('no'), glp1: fact('no') };
  const { fits, notFits } = rank(DATA, facts, 't2d');
  assert.ok(notFits.some(x => x.trial.id === 'NCT07664553'));
  assert.ok(notFits.some(x => x.trial.id === 'NCT07776509'));
  const byDistance = rank(DATA, facts, 't2d', 'distance').fits.map(x => x.km);
  const known = byDistance.filter(k => k != null);
  assert.deepEqual([...known].sort((a, b) => a - b), known);
  assert.deepEqual(byDistance.slice(known.length).filter(k => k != null), []);
  assert.ok(fits.every(x => (x.trial.named_site ? x.km > 40 : x.km === null)));
});

test('location can rule a trial out: the urine salt study is only for the VCH and Providence area', () => {
  const trial = DATA.trials.find(t => t.id === 'NCT07369856');
  assert.equal(assess(trial, { area: fact('surrey') }).notmet, 1);
  assert.equal(assess(trial, { area: fact('north_shore') }).notmet, 0);
});

test('every requirement quotes its source and every trial belongs to a condition', () => {
  for (const t of DATA.trials) {
    assert.ok(t.groups.every(g => DATA.conditions.some(c => c.id === g)));
    for (const r of t.reqs) assert.ok(r.quote.length > 5, `${t.id}: ${r.text}`);
  }
});

test('every requirement a person can check has a plain sentence, and every answer has a phrase', () => {
  for (const t of DATA.trials) {
    for (const r of t.reqs) {
      const checkable = JSON.stringify(r.test || []).match(/"[a-z_0-9]+","(>=|>|<=|<|between|is|map)"/);
      if (checkable) assert.ok(r.rule && /^[A-Z].*\.$/.test(r.rule), `${t.id}: ${r.text}`);
    }
  }
  for (const [key, q] of Object.entries(DATA.questions)) {
    const p = DATA.phrases[key];
    assert.ok(p && p.topic, key);
    if (q.type === 'choice' && key !== 'area') for (const o of q.options) assert.ok(p[o.value], `${key}: ${o.value}`);
  }
});

test('a match is labelled strong only when everything a person could check is confirmed', () => {
  const trial = DATA.trials.find(t => t.id === 'NCT05963698');
  const facts = { af_type: fact('persistent'), anticoag: fact('yes'), age: { lo: 69, hi: 69 }, prior_ablation: fact('no') };
  const r = assess(trial, facts);
  assert.equal(r.met, r.canCheck);
  assert.equal(r.fit, 'strong');
  assert.ok(r.percent < 50);
  assert.equal(assess(trial, { ...facts, prior_ablation: fact('yes') }).fit, 'worth');
});
