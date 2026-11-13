# Typing for the trial finder

The live trial finder only takes tapped answers, because reading what people type needs an AI model and every message would cost money. This folder is what turns typing on: a small Cloudflare Worker that reads a description like "I'm 58, type 2 diabetes for about 6 years, on metformin, last A1C was 8.1" and sends back the same facts the tiles would.

It sends the text to Anthropic's Claude API with a JSON schema that has one field per fact the finder knows (age, HbA1c, "do you use insulin" and so on). Every field can be empty, and the instructions say to fill one only when the text clearly states it. [`understand.js`](understand.js) then drops anything outside the allowed answers, so a strange reply can't add a fact the page doesn't understand. The worker doesn't store or log anything people write.

## Turning it on

You need a Cloudflare account and an Anthropic API key.

```sh
cd web/trial-finder-ai
npm install
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler deploy
```

Then add one line to `web/trial-finder/index.html`, before the `app.js` script, using the address `wrangler deploy` printed:

```html
<script>window.TRIAL_FINDER_AI = 'https://trial-finder-ai.<your-subdomain>.workers.dev';</script>
```

The text box switches on by itself when that address is set. `ALLOWED_ORIGIN` in [`wrangler.jsonc`](wrangler.jsonc) limits which website can call the worker, and `MODEL` picks the model (`claude-opus-5-5` by default; `claude-haiku-5-5` is much cheaper for a job this small).

## Testing

`node --test tests/js/understand.test.mjs` (from the repository root) checks the schema, the request and how replies are read, using a fake client, so it never calls the API.
