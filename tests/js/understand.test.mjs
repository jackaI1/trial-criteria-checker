import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DATA } from '../../web/trial-finder/data.js';
import { buildRequest, factSchema, readFacts, understand } from '../../web/trial-finder-ai/understand.js';

const reply = obj => ({ stop_reason: 'end_turn', content: [{ type: 'text', text: JSON.stringify(obj) }] });

test('the schema has one nullable field per question and nothing else', () => {
  const schema = factSchema(DATA);
  assert.equal(schema.additionalProperties, false);
  assert.deepEqual(new Set(schema.required), new Set(['condition', ...Object.keys(DATA.questions)]));
  assert.deepEqual(schema.properties.insulin.anyOf[0].enum, ['yes', 'no']);
});

test('the request uses structured output, low effort and a refusal fallback only where supported', () => {
  const req = buildRequest(DATA, 'x'.repeat(5000), { model: 'claude-opus-5-5' });
  assert.equal(req.output_config.format.type, 'json_schema');
  assert.equal(req.output_config.effort, 'low');
  assert.equal(req.fallbacks, 'default');
  assert.equal(req.messages[0].content.length, 2000);
  assert.equal(buildRequest(DATA, 'x', { model: 'claude-haiku-5-5' }).fallbacks, undefined);
});

test('facts are read back and anything outside the options is dropped', () => {
  const out = readFacts(DATA, reply({ condition: 't2d', age: 58, hba1c: 8.1, insulin: 'no', glp1: 'sometimes', bmi: -3, pancreatitis: null }));
  assert.equal(out.condition, 't2d');
  assert.deepEqual(out.facts.age, { lo: 58, hi: 58 });
  assert.deepEqual(out.facts.insulin, { value: 'no' });
  assert.equal(out.facts.glp1, undefined);
  assert.equal(out.facts.bmi, undefined);
  assert.equal(out.facts.pancreatitis, undefined);
});

test('a refusal or broken output gives no facts instead of an error', () => {
  assert.deepEqual(readFacts(DATA, { stop_reason: 'refusal', content: [] }), { condition: null, facts: {}, refused: true });
  assert.deepEqual(readFacts(DATA, { stop_reason: 'end_turn', content: [{ type: 'text', text: 'not json' }] }), { condition: null, facts: {} });
});

test('understand sends one request through the client it is given', async () => {
  const calls = [];
  const client = { beta: { messages: { create: async params => { calls.push(params); return reply({ condition: 'af', af_type: 'persistent' }); } } } };
  const out = await understand(client, DATA, 'I have persistent AF', { model: 'claude-opus-5-5' });
  assert.equal(calls.length, 1);
  assert.equal(out.condition, 'af');
  assert.deepEqual(out.facts.af_type, { value: 'persistent' });
});
