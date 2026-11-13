// Turns what someone types into the same facts the tiles produce.
// Kept free of network code so it can be tested with a fake client.

const MAX_TEXT = 2000;

// One JSON schema with a nullable field per question. The model fills only what
// the person actually said; everything else stays null, so it can't invent facts.
export function factSchema(data) {
  const properties = {
    condition: { anyOf: [{ type: 'string', enum: data.conditions.map(c => c.id) }, { type: 'null' }] },
  };
  for (const [key, q] of Object.entries(data.questions)) {
    properties[key] = q.type === 'range'
      ? { anyOf: [{ type: 'number' }, { type: 'null' }] }
      : { anyOf: [{ type: 'string', enum: q.options.map(o => o.value) }, { type: 'null' }] };
  }
  return { type: 'object', properties, required: Object.keys(properties), additionalProperties: false };
}

export function instructions(data) {
  const lines = Object.entries(data.questions).map(([key, q]) => {
    const kind = q.type === 'range'
      ? `a number${q.unit ? ' in ' + q.unit : ''}${key === 'years_dx' ? ' of years' : ''}`
      : `one of: ${q.options.map(o => `"${o.value}" (${o.label})`).join(', ')}`;
    return `- ${key}: ${q.label}. ${kind}`;
  });
  return [
    'You read a short description a person wrote about their own health, for a clinical trial finder.',
    'Fill in a field only when the text clearly states it. Never guess, infer from typical cases, or fill a field from something the person only might have.',
    'Leave every other field null. A field the person says they don\'t know is also null.',
    `condition is one of ${data.conditions.map(c => `"${c.id}" (${c.label})`).join(', ')}, or null.`,
    'Fields:',
    ...lines,
  ].join('\n');
}

// Models that accept server-side refusal fallbacks. Others just get no fallback.
const FALLBACK_MODELS = new Set(['claude-opus-5-5', 'claude-opus-5', 'claude-sonnet-5-5', 'claude-fable-5-2', 'claude-fable-5-1']);

export function buildRequest(data, text, { model }) {
  const fallback = FALLBACK_MODELS.has(model) ? { betas: ['server-side-fallback-2026-07-01'], fallbacks: 'default' } : {};
  return {
    model,
    max_tokens: 2000,
    system: instructions(data),
    messages: [{ role: 'user', content: String(text).slice(0, MAX_TEXT) }],
    // Pulling facts out of a few sentences is a simple task.
    output_config: { effort: 'low', format: { type: 'json_schema', schema: factSchema(data) } },
    ...fallback,
  };
}

// Converts the model's JSON into facts, dropping anything outside the known options.
export function readFacts(data, response) {
  if (response.stop_reason === 'refusal') return { condition: null, facts: {}, refused: true };
  const block = (response.content || []).find(b => b.type === 'text');
  if (!block) return { condition: null, facts: {} };
  let raw;
  try { raw = JSON.parse(block.text); } catch { return { condition: null, facts: {} }; }
  const facts = {};
  for (const [key, q] of Object.entries(data.questions)) {
    const value = raw[key];
    if (value === null || value === undefined) continue;
    if (q.type === 'range') {
      if (typeof value === 'number' && Number.isFinite(value) && value >= 0) facts[key] = { lo: value, hi: value };
    } else if (q.options.some(o => o.value === value)) {
      facts[key] = { value };
    }
  }
  const condition = data.conditions.some(c => c.id === raw.condition) ? raw.condition : null;
  return { condition, facts };
}

export async function understand(client, data, text, options) {
  const response = await client.beta.messages.create(buildRequest(data, text, options));
  return readFacts(data, response);
}
