import { DATA } from './data.js';
import { assess, evalTest, factsIn, isKnown, nextQuestion, rank, reqStatus, trialsFor } from './engine.js';

// Typing is off unless an AI endpoint is configured (see ai/README.md).
// Set window.TRIAL_FINDER_AI = 'https://your-worker.example/understand' before this script loads.
const AI_ENDPOINT = window.TRIAL_FINDER_AI || null;
const MAX_QUESTIONS = 8;
const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

const $ = id => document.getElementById(id);
const thread = $('thread');
const choicesEl = $('choices');
const resultsEl = $('results');
const talkEl = $('talk');

let state;
// Each conversation gets a number. "Start over" bumps it, and anything still
// typing for the old conversation stops instead of appearing in the new one.
let run = 0;
class Stale extends Error {}
function reset() {
  run += 1;
  state = { condition: null, facts: {}, asked: [], filesAdded: [], offered: false, sort: 'fit', index: 0, busy: false };
  thread.innerHTML = '';
  choicesEl.innerHTML = '';
  resultsEl.hidden = true;
  talkEl.hidden = false;
  renderPanel();
  start();
}

// ---------- small helpers

const el = (tag, attrs = {}, ...kids) => {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') node.className = v;
    else if (k === 'text') node.textContent = v;
    else if (k.startsWith('on')) node.addEventListener(k.slice(2), v);
    else if (v !== false && v != null) node.setAttribute(k, v === true ? '' : v);
  }
  for (const kid of kids.flat(Infinity)) if (kid != null) node.append(kid.nodeType ? kid : document.createTextNode(kid));
  return node;
};
const wait = ms => new Promise(r => setTimeout(r, calm ? Math.min(ms, 150) : ms));
const conditionName = () => DATA.conditions.find(c => c.id === state.condition)?.name ?? 'your condition';
const fileIcon = () => {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 20 20'); svg.setAttribute('aria-hidden', 'true');
  svg.innerHTML = '<path d="M5 2h7l4 4v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1Zm7 1.5V7h3.5L12 3.5ZM7 10h6v1.5H7V10Zm0 3h6v1.5H7V13Z"/>';
  return svg;
};

// A message shown at once, with no typing dots (the opening line would be ready before anyone types).
function sayNow(...parts) {
  thread.append(el('li', { class: 'msg bot' }, el('span', { class: 'who', text: 'Trial finder' }),
    parts.map(p => (typeof p === 'string' ? el('p', { text: p }) : p))));
}

async function say(...parts) {
  const mine = run;
  const typing = el('li', { class: 'msg bot' }, el('span', { class: 'typing' }, el('span', { class: 'dots' }, el('i'), el('i'), el('i'))));
  const label = parts.find(p => p && p.typingLabel);
  if (label) typing.firstChild.append(label.typingLabel);
  thread.append(typing);
  scrollDown();
  const length = parts.filter(p => typeof p === 'string').join(' ').length;
  await wait(Math.min(1500, 600 + length * 9) + (label ? 700 : 0));
  typing.remove();
  if (mine !== run) throw new Stale();
  const msg = el('li', { class: 'msg bot' }, el('span', { class: 'who', text: 'Trial finder' }),
    parts.filter(p => !(p && p.typingLabel)).map(p => (typeof p === 'string' ? el('p', { text: p }) : p)));
  thread.append(msg);
  scrollDown();
}
function you(content) {
  thread.append(el('li', { class: 'msg user' }, content));
  scrollDown();
}
function scrollDown() {
  requestAnimationFrame(() => {
    if (!resultsEl.hidden) return;
    window.scrollTo({ top: document.body.scrollHeight, behavior: calm ? 'auto' : 'smooth' });
  });
}
function offer(options) {
  choicesEl.innerHTML = '';
  for (const o of options) {
    const b = el('button', { type: 'button', class: 'choice' + (o.quiet ? ' quiet' : '') + (o.file ? ' file' : '') }, o.file ? fileIcon() : null, o.label);
    b.addEventListener('click', async () => {
      if (state.busy) return;
      state.busy = true;
      choicesEl.innerHTML = '';
      try {
        await o.run();
      } catch (error) {
        if (!(error instanceof Stale)) throw error;
      } finally {
        state.busy = false;
      }
    });
    choicesEl.append(b);
  }
}

// ---------- facts

function display(key, fact) {
  if (!fact) return '';
  if (fact.state === 'unsure') return 'Not sure';
  if (fact.state === 'private') return 'Not shared';
  if (fact.label) return fact.label;
  const q = DATA.questions[key];
  if (fact.value !== undefined) {
    if (key === 'area') return DATA.areas.find(a => a.id === fact.value)?.label ?? fact.value;
    const opt = q?.options?.find(o => o.value === fact.value);
    return opt ? opt.label : fact.value;
  }
  if (key === 'years_dx') return `About ${Math.round((fact.lo + fact.hi) / 2)} years`;
  const unit = q?.unit ?? '';
  return fact.lo === fact.hi ? `${fact.lo}${unit}` : `${fact.lo} to ${fact.hi}${unit}`;
}
function factLabel(key) {
  if (key === 'condition') return 'Condition';
  return DATA.questions[key]?.label ?? key;
}
function setFact(key, fact) {
  state.facts[key] = fact;
}

function renderPanel() {
  const facts = $('facts');
  facts.innerHTML = '';
  const entries = Object.entries(state.facts).filter(([k, f]) => f.source !== 'condition');
  if (state.condition) entries.unshift(['condition', { label: DATA.conditions.find(c => c.id === state.condition).label, source: 'You said' }]);
  $('known-count').textContent = entries.length;
  if (!entries.length) {
    facts.append(el('div', { class: 'empty', text: 'Nothing yet. Answers and file details show up here, with where each one came from.' }));
  }
  for (const [key, fact] of entries) {
    facts.append(el('div', { class: 'fact' + (fact.state ? ' ' + fact.state : '') },
      el('dt', { text: factLabel(key) }), el('dd', { text: display(key, fact) }),
      el('span', { class: 'src' + (fact.file ? ' file' : ''), text: fact.source })));
  }
  const narrow = $('narrow');
  if (!state.condition) { narrow.hidden = true; return; }
  const trials = trialsFor(DATA, state.condition);
  const live = trials.filter(t => assess(t, state.facts).notmet === 0);
  narrow.hidden = false;
  $('narrow-text').textContent = `${live.length} of ${trials.length} ${conditionName()} ${trials.length === 1 ? 'trial' : 'trials'} in Vancouver still possible`;
  const tubes = $('tubes');
  tubes.innerHTML = '';
  for (const t of trials) {
    const r = assess(t, state.facts);
    const tube = el('span', { class: 'tube' + (r.notmet ? ' out' : ''), title: t.title });
    tube.style.setProperty('--fill', `${r.percent}%`);
    tubes.append(tube);
  }
}

// ---------- the conversation

async function start() {
  sayNow('Hi. I can help you find clinical trials that are recruiting in Vancouver.',
    'Tell me about yourself, and add any medical files you have. Let\'s start with your condition. What are you living with?');
  offerConditions();
}

function offerConditions(only) {
  const list = DATA.conditions.filter(c => !only || only.includes(c.id));
  offer([...list.map(c => ({ label: c.label, run: () => chooseCondition(c) })),
    ...(only ? [] : [{ label: 'Something else', quiet: true, run: somethingElse }])]);
}

async function somethingElse() {
  you('Something else');
  await say('This demo covers type 2 diabetes, atrial fibrillation, heart failure and lupus. Pick one to try it with made-up answers.');
  offerConditions();
}

async function chooseCondition(c) {
  you(c.label);
  state.condition = c.id;
  for (const [k, v] of Object.entries(c.facts || {})) if (!state.facts[k]) setFact(k, { value: v, source: 'condition' });
  renderPanel();
  if (state.filesAdded.length) return askArea();
  await ask('years_dx');
}

async function askFiles(again = false) {
  const remaining = DATA.files.filter(f => f.conditions.includes(state.condition) && !state.filesAdded.includes(f.id));
  if (!remaining.length) return askArea();
  if (!again) {
    await say('Do you have any medical files, like a doctor\'s letter or blood test results? Adding one means fewer questions.',
      el('p', { class: 'help', text: 'These are sample files with made-up details, so you can see how it works.' }));
  } else {
    await say('Anything else to add?');
  }
  offer([...remaining.map(f => ({ label: f.name, file: true, run: () => addFile(f) })),
    { label: again ? 'That\'s all' : 'Skip this', quiet: true, run: async () => { you(again ? 'That\'s all' : 'Skip this'); await askArea(); } }]);
}

async function addFile(file) {
  you(el('span', { class: 'filechip' }, fileIcon(), file.file));
  state.filesAdded.push(file.id);
  const found = [];
  for (const [key, v] of Object.entries(file.facts)) {
    if (state.facts[key] && isKnown(state.facts[key]) && state.facts[key].source !== 'condition') continue;
    const fact = typeof v === 'object' ? { ...v } : { value: v };
    setFact(key, { ...fact, source: file.name, file: true });
    found.push(`${factLabel(key)}: ${display(key, state.facts[key])}`);
  }
  await say({ typingLabel: `Reading ${file.file}` },
    el('div', { class: 'doc' }, el('h4', {}, file.name, el('span', { class: 'sample', text: 'Sample, made up' })),
      file.lines.map(line => el('p', { text: line }))),
    found.length ? `I found ${found.length} ${found.length === 1 ? 'thing' : 'things'} trials ask about:` : 'Nothing new in this one.',
    found.length ? el('ul', { class: 'found' }, found.map(f => el('li', { text: f }))) : null);
  renderPanel();
  await askFiles(true);
}

async function askArea() {
  if (state.facts.area) return askNext();
  await ask('area');
}

async function ask(key, { forTrial = false } = {}) {
  const q = DATA.questions[key];
  const text = q.ask.replace('{condition}', conditionName());
  await say(text, q.help ? el('details', { class: 'help' }, el('summary', { text: 'How do I find this?' }), el('p', { text: q.help })) : null);
  const answer = async (label, fact) => {
    you(label);
    setFact(key, { ...fact, source: 'You said' });
    state.asked.push(key);
    renderPanel();
    if (key === 'years_dx') return askFiles();
    if (forTrial) return askOpen(forTrial);
    return askNext();
  };
  offer([
    ...q.options.map(o => ({ label: o.label, run: () => answer(o.label, o.value !== undefined ? { value: o.value } : { lo: o.lo, hi: o.hi, label: o.label }) })),
    { label: 'I don\'t know', quiet: true, run: () => answer('I don\'t know', { state: 'unsure' }) },
    { label: 'I\'d rather not say', quiet: true, run: () => answer('I\'d rather not say', { state: 'private' }) },
  ]);
}

async function askNext() {
  const adaptive = state.asked.filter(k => k !== 'years_dx' && k !== 'area').length;
  const { fits } = rank(DATA, state.facts, state.condition);
  const ready = fits.filter(x => x.result.fit === 'strong' && x.result.ask === 0);
  const next = nextQuestion(DATA, state.facts, state.condition);
  if (!next || adaptive >= MAX_QUESTIONS) return finish();
  if (ready.length && !state.offered) {
    state.offered = true;
    await say(`Everything you could check already matches for ${ready.length} ${ready.length === 1 ? 'trial' : 'trials'}. I can show you now, or ask a few more questions to check the others.`);
    offer([{ label: 'Show my matches', run: async () => { you('Show my matches'); await finish(); } },
      { label: 'Ask more questions', quiet: true, run: async () => { you('Ask more questions'); await ask(next.fact); } }]);
    return;
  }
  await ask(next.fact);
}

async function finish() {
  const { fits } = rank(DATA, state.facts, state.condition);
  await say(fits.length ? 'That\'s everything I need for now. Here\'s what I found.' : 'I\'ve checked every trial I know about for you.');
  offer([]);
  state.index = 0;
  showResults();
}

// Questions for one trial's open lines, asked from its match card.
async function askOpen(trial, first) {
  // Only lines still waiting on an answer, so settled lines don't bring up extra questions.
  const waiting = trial.reqs.filter(r => reqStatus(r, state.facts) === 'ask');
  let open = [...new Set(waiting.flatMap(r => [...factsIn(r.test)]).filter(f => !state.facts[f] && DATA.questions[f]))];
  if (first && open.includes(first)) open = [first, ...open.filter(f => f !== first)];
  if (!open.length) { state.index = 0; return showResults(trial.id); }
  await ask(open[0], { forTrial: trial });
}

// ---------- plain sentences

const join = list => (list.length < 2 ? list[0] || '' : list.slice(0, -1).join(', ') + ' and ' + list[list.length - 1]);
const isClause = topic => /^(whether|how|what|where)\b/.test(topic);

// How an answer reads in a sentence: "you're not on dialysis", "your HbA1c is 8.1%".
function phrase(key, fact) {
  const p = DATA.phrases[key];
  if (!p || !isKnown(fact)) return null;
  if (fact.value === undefined && typeof p.v === 'string') {
    // Tile labels start with a capital ("Under 18"), which reads wrong mid-sentence.
    const value = display(key, fact);
    return p.v.replace('{v}', /^[A-Z][a-z]/.test(value) ? value.charAt(0).toLowerCase() + value.slice(1) : value);
  }
  if (fact.value === undefined) return p.v[String(fact.lo)] ?? null;
  return p[fact.value] ?? null;
}

function sourceLead(source) {
  if (source === 'You said') return 'You said';
  if (source === 'You wrote') return 'You wrote that';
  return DATA.files.find(f => f.name === source)?.says ?? `Your ${source.toLowerCase()} says`;
}

// The facts behind a failed check, leaving out the parts that passed.
function failing(test, out = new Set()) {
  if (!test || test[0] === 'team') return out;
  if (test[0] === 'all' || test[0] === 'any') {
    for (const part of test[1]) if (evalTest(part, state.facts) === false) failing(part, out);
    return out;
  }
  if (evalTest(test, state.facts) === false) out.add(test[0]);
  return out;
}

// "You said you're not on dialysis. Your blood test results show your HbA1c is 8.1%."
function evidence(req, only) {
  const bySource = new Map();
  for (const key of only || factsIn(req.test)) {
    const fact = state.facts[key];
    if (!fact || fact.source === 'condition') continue;
    const words = phrase(key, fact);
    if (!words) continue;
    if (!bySource.has(fact.source)) bySource.set(fact.source, []);
    bySource.get(fact.source).push(words);
  }
  return [...bySource.entries()].map(([source, words]) => `${sourceLead(source)} ${join(words)}.`).join(' ');
}

function topics(req, test) {
  return [...factsIn(req.test)].filter(test).map(k => DATA.phrases[k]?.topic).filter(Boolean);
}

function explain({ req, status }) {
  const said = evidence(req);
  if (status === 'met') return said || 'Confirmed.';
  if (status === 'notmet') return [evidence(req, failing(req.test)), req.rule].filter(Boolean).join(' ');
  if (status === 'ask') {
    const open = topics(req, k => !state.facts[k]);
    return isClause(open[0] || '') ? `I haven't asked ${open.join(' or ')} yet.` : `I haven't asked about ${join(open)} yet.`;
  }
  const kept = topics(req, k => state.facts[k]?.state === 'private');
  if (kept.length) return [`You chose not to share ${kept.join(' or ')}.`, req.rule, 'The study team will ask you about it at screening.'].filter(Boolean).join(' ');
  const unsure = topics(req, k => state.facts[k]?.state === 'unsure');
  if (unsure.length) {
    const lead = isClause(unsure[0]) ? `You weren't sure ${unsure.join(' or ')}.` : `You didn't know ${join(unsure)}.`;
    return [lead, req.rule, 'The study team can check this at screening.'].filter(Boolean).join(' ');
  }
  if (said) return `${said} The study team checks the rest at screening.`;
  return 'Only the study team can check this, at your screening visit.';
}

// Why a trial is ruled out: the rule first, then what you told me.
function reason(req) {
  return [req.rule, evidence(req, failing(req.test))].filter(Boolean).join(' ');
}

const MARKS = { met: '✓', notmet: '✕', ask: '?', team: '·' };

// ---------- results

function showResults(focusId) {
  const { fits, notFits } = rank(DATA, state.facts, state.condition, state.sort);
  if (focusId) state.index = Math.max(0, fits.findIndex(x => x.trial.id === focusId));
  talkEl.hidden = true;
  resultsEl.hidden = false;
  resultsEl.innerHTML = '';
  const head = el('div', { class: 'results-head' }, el('h2', { text: 'Your matches' }),
    el('div', { class: 'sort', role: 'group', 'aria-label': 'Sort matches' },
      el('button', { type: 'button', 'aria-pressed': String(state.sort === 'fit'), onclick: () => { state.sort = 'fit'; state.index = 0; showResults(); }, text: 'Best match' }),
      el('button', { type: 'button', 'aria-pressed': String(state.sort === 'distance'), onclick: () => { state.sort = 'distance'; state.index = 0; showResults(); }, text: 'Closest' })));
  resultsEl.append(head);

  if (!fits.length) {
    resultsEl.append(el('div', { class: 'nomatch' }, el('h3', { text: 'No trial fits right now' }),
      el('p', { text: `None of the ${conditionName()} trials recruiting in Vancouver today fit what you told me. Trials open and close every week, so this changes.` }),
      el('p', { text: 'This demo only covers trials with a Vancouver site.' }),
      el('div', { class: 'actions' }, el('button', { type: 'button', class: 'btn', onclick: reset, text: 'Start over' }))));
  } else {
    resultsEl.append(card(fits[state.index], state.index, fits.length));
  }
  if (notFits.length) {
    resultsEl.append(el('details', { class: 'others' }, el('summary', { text: `Not a fit right now (${notFits.length})` }),
      el('ul', {}, notFits.map(x => el('li', {}, el('a', { href: x.trial.url, target: '_blank', rel: 'noopener', text: x.trial.title }), el('br'),
        el('span', { class: 'reason', text: reason(x.result.rows.find(r => r.status === 'notmet').req) }))))));
  }
  window.scrollTo({ top: 0, behavior: 'auto' });
  requestAnimationFrame(() => window.scrollTo({ top: 0, behavior: 'auto' }));
}

function card({ trial, result: r, km }, i, n) {
  const fitText = { strong: 'Everything you could check is met', worth: 'Worth asking about', notfit: 'Not a fit right now' }[r.fit];
  const area = DATA.areas.find(a => a.id === state.facts.area?.value);
  const where = !trial.named_site ? `${trial.site}, Vancouver. The listing doesn't name the exact site.`
    : km != null && area?.place ? `${trial.site}, about ${Math.max(1, Math.round(km))} km from ${area.place}` : trial.site;
  const pct = v => `${(100 * v) / r.total}%`;
  const fill = el('div', { class: 'fill grow', role: 'img', 'aria-label': `${r.met} confirmed, ${r.ask} you could answer, ${r.team} checked by the study team, ${r.notmet} not met` },
    el('span', { class: 'met', style: `width:${pct(r.met)}` }), el('span', { class: 'ask', style: `width:${pct(r.ask)}` }),
    el('span', { class: 'team', style: `width:${pct(r.team)}` }), el('span', { class: 'notmet', style: `width:${pct(r.notmet)}` }));
  const groups = [['need', 'What you need'], ['cant', 'What you can\'t have']];
  return el('article', { class: 'card' },
    el('div', { class: 'card-top' },
      el('span', { class: 'fitlabel ' + r.fit, text: fitText }),
      el('span', { class: 'pager' },
        el('button', { type: 'button', 'aria-label': 'Previous match', disabled: i === 0, onclick: () => { state.index--; showResults(); }, text: '‹' }),
        `${i + 1} of ${n}`,
        el('button', { type: 'button', 'aria-label': 'Next closest match', disabled: i === n - 1, onclick: () => { state.index++; showResults(); }, text: '›' }))),
    el('h3', {}, el('a', { href: trial.url, target: '_blank', rel: 'noopener', text: trial.title })),
    el('p', { class: 'site', text: where }),
    el('div', { class: 'score' },
      el('div', { class: 'big' }, String(r.percent), el('small', { text: '%' })),
      el('p', { class: 'score-say', text: `of the ${r.total} requirements listed below confirmed. ${r.team ? `${r.team} can only be checked by the study team at screening.` : ''}` }),
      fill,
      el('ul', { class: 'legend' },
        el('li', { class: 'met' }, el('i'), `${r.met} confirmed`),
        r.ask ? el('li', { class: 'ask' }, el('i'), `${r.ask} you could answer`) : null,
        el('li', { class: 'team' }, el('i'), `${r.team} for the study team`),
        r.notmet ? el('li', { class: 'notmet' }, el('i'), `${r.notmet} not met`) : null)),
    el('dl', { class: 'about' },
      el('dt', { text: 'What it is' }), el('dd', { text: trial.summary }),
      el('dt', { text: 'Kind of study' }), el('dd', { text: trial.kind }),
      el('dt', { text: 'Stage' }), el('dd', { text: trial.phase }),
      el('dt', { text: 'Groups' }), el('dd', { text: [trial.comparison, trial.blinding].filter(Boolean).join(' ') }),
      el('dt', { text: 'Size' }), el('dd', { text: trial.enrollment ? `About ${trial.enrollment.toLocaleString('en-CA')} people in total` : 'Not listed' }),
      el('dt', { text: 'Payment' }), el('dd', { text: 'Not listed. Ask the study team about pay and travel costs.' })),
    groups.map(([kind, title]) => [el('h4', { text: title }),
      el('ul', { class: 'reqs' }, r.rows.filter(x => x.req.kind === kind).map(({ req, status }) =>
        el('li', { class: 'req ' + status },
          el('span', { class: 'ico', 'aria-label': { met: 'Met', notmet: 'Not met', ask: 'Open question', team: 'Study team checks' }[status], text: MARKS[status] }),
          el('div', {}, el('p', { class: 'what', text: req.text }), el('p', { class: 'why', text: explain({ req, status }) }),
            status === 'ask' ? el('button', { type: 'button', class: 'linkish', onclick: () => backToTalk(trial, [...factsIn(req.test)].find(k => !state.facts[k])), text: 'Answer now' }) : null,
            el('details', {}, el('summary', { text: 'The trial\'s wording' }), el('blockquote', { text: req.quote }))))))]),
    el('div', { class: 'actions' },
      el('button', { type: 'button', class: 'btn primary', onclick: () => openHandoff(trial, r), text: 'See what the study team would get' }),
      r.ask ? el('button', { type: 'button', class: 'btn', onclick: () => backToTalk(trial), text: `Answer ${r.ask} open ${r.ask === 1 ? 'question' : 'questions'}` }) : null,
      el('a', { class: 'btn', href: trial.url, target: '_blank', rel: 'noopener', text: 'Official listing' })));
}

async function backToTalk(trial, first) {
  resultsEl.hidden = true;
  talkEl.hidden = false;
  try {
    await askOpen(trial, first);
  } catch (error) {
    if (!(error instanceof Stale)) throw error;
  }
}

// The same facts, written for the study team: "HbA1c: 8.1% (blood test results)".
function teamEvidence(req) {
  return [...factsIn(req.test)].filter(k => isKnown(state.facts[k]) && state.facts[k].source !== 'condition')
    .map(k => `${factLabel(k)}: ${display(k, state.facts[k])} (${state.facts[k].source === 'You said' ? 'they said' : state.facts[k].source.toLowerCase()})`)
    .join('; ');
}

function openHandoff(trial, r) {
  const dialog = $('handoff');
  const list = status => r.rows.filter(x => x.status === status);
  const about = ['age', 'area'].filter(k => state.facts[k]).map(k => `${factLabel(k)}: ${display(k, state.facts[k])}`);
  dialog.innerHTML = '';
  dialog.append(el('div', { class: 'inner' },
    el('button', { type: 'button', class: 'btn close', onclick: () => dialog.close(), text: 'Close' }),
    el('h3', { id: 'handoff-title', text: `New possible participant for ${trial.id}` }),
    el('p', { class: 'note', text: 'This is what the study team would see if you chose to share. In this demo nothing is sent.' }),
    el('p', {}, `${trial.title}. ${r.met} of ${r.total} requirements confirmed, ${r.notmet} not met.`),
    about.length ? el('p', { text: about.join('. ') + '.' }) : null,
    el('h4', { text: `To check at screening (${list('team').length + list('ask').length})` }),
    el('ul', {}, [...list('ask'), ...list('team')].map(x => {
      const facts = [...factsIn(x.req.test)].map(k => state.facts[k]);
      const note = x.status === 'ask' ? ' (not asked yet)' : facts.some(f => f?.state === 'private') ? ' (they chose not to share this)'
        : facts.some(f => f?.state === 'unsure') ? ' (they weren\'t sure)' : '';
      return el('li', { text: (x.req.kind === 'cant' ? 'Check for: ' + x.req.text.charAt(0).toLowerCase() + x.req.text.slice(1) : x.req.text) + note });
    })),
    el('h4', { text: `Already confirmed (${list('met').length})` }),
    el('ul', {}, list('met').map(x => el('li', { text: `${x.req.kind === 'cant' ? 'Clear of: ' + x.req.text.charAt(0).toLowerCase() + x.req.text.slice(1) : x.req.text}. ${teamEvidence(x.req)}` })))));
  dialog.showModal();
}

// ---------- optional typing, only when an AI endpoint is configured

if (AI_ENDPOINT) {
  const box = $('typebox');
  const input = $('say');
  box.classList.add('on');
  input.disabled = false;
  box.querySelector('button').disabled = false;
  input.placeholder = 'Describe yourself, or pick an answer above';
  $('typenote').textContent = 'What you type is sent to the AI model only to pull out facts. Nothing is stored.';
  box.addEventListener('submit', async event => {
    event.preventDefault();
    const text = input.value.trim();
    if (!text || state.busy) return;
    input.value = '';
    you(text);
    state.busy = true;
    try {
      const reply = await fetch(AI_ENDPOINT, { method: 'POST', headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ text, condition: state.condition }) }).then(r => r.json());
      if (reply.condition && !state.condition) state.condition = reply.condition;
      for (const [key, fact] of Object.entries(reply.facts || {})) {
        if (DATA.questions[key] && !state.facts[key]) setFact(key, { ...fact, source: 'You wrote' });
      }
      renderPanel();
    } catch {
      await say('I couldn\'t read that just now. Pick an answer above instead.').catch(() => {});
    } finally {
      state.busy = false;
    }
    if (!state.condition) offerConditions();
    else if (!state.facts.years_dx) await ask('years_dx');
    else await askNext();
  });
}

$('restart').addEventListener('click', reset);
// On a phone the facts start folded so the conversation stays in view.
if (matchMedia('(max-width: 980px)').matches) $('panel-fold').open = false;
$('retrieved').textContent = 'checked ' + new Date(DATA.retrieved + 'T12:00:00').toLocaleDateString('en-CA', { month: 'long', day: 'numeric', year: 'numeric' });
reset();
