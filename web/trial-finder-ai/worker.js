// Optional Cloudflare Worker that lets people type in the trial finder.
// It only extracts facts from the text and sends them back. It stores nothing
// and never logs what people write. Setup steps are in README.md.
import Anthropic from '@anthropic-ai/sdk';
import { DATA } from '../trial-finder/data.js';
import { understand } from './understand.js';

const json = (body, status, origin) => new Response(JSON.stringify(body), {
  status,
  headers: {
    'content-type': 'application/json',
    'access-control-allow-origin': origin,
    'access-control-allow-methods': 'POST, OPTIONS',
    'access-control-allow-headers': 'content-type',
    'cache-control': 'no-store',
  },
});

export default {
  async fetch(request, env) {
    const origin = env.ALLOWED_ORIGIN || 'https://jacklai.ca';
    if (request.method === 'OPTIONS') return json({}, 204, origin);
    if (request.method !== 'POST') return json({ error: 'Send a POST with {"text": "..."}' }, 405, origin);
    let body;
    try { body = await request.json(); } catch { return json({ error: 'The body must be JSON' }, 400, origin); }
    const text = typeof body.text === 'string' ? body.text.trim() : '';
    if (!text) return json({ error: 'Add some text to read' }, 400, origin);
    const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
    try {
      const result = await understand(client, DATA, text, { model: env.MODEL || 'claude-opus-5-5' });
      return json(result, 200, origin);
    } catch (error) {
      const status = error instanceof Anthropic.RateLimitError ? 429 : 502;
      return json({ error: 'The model could not read that just now' }, status, origin);
    }
  },
};
