// Matching logic for the trial finder. No network, no storage: everything here
// works on the facts held in memory by app.js.
//
// A fact is one of:
//   {lo, hi, source}            a number, or a range like "8 to 9%"
//   {value, source}             a choice like "yes" or "persistent"
//   {state: 'unsure' | 'private', source}   "I don't know" or "I'd rather not say"
// A missing fact hasn't been asked yet.

export function isKnown(fact) {
  return Boolean(fact) && !fact.state;
}

// true = passes, false = fails, null = can't tell yet.
export function evalTest(test, facts) {
  if (!test) return null;
  const [head, op, value] = test;
  if (head === 'team') return null;
  if (head === 'all' || head === 'any') {
    const parts = op.map(t => evalTest(t, facts));
    if (head === 'all') {
      if (parts.includes(false)) return false;
      return parts.every(p => p === true) ? true : null;
    }
    if (parts.includes(true)) return true;
    return parts.every(p => p === false) ? false : null;
  }
  const fact = facts[head];
  if (!isKnown(fact)) return null;
  if (op === 'is') return fact.value === value;
  if (op === 'map') {
    const out = Object.prototype.hasOwnProperty.call(value, fact.value) ? value[fact.value] : null;
    return out === undefined ? null : out;
  }
  const { lo, hi } = fact;
  switch (op) {
    case '>=': return lo >= value ? true : hi < value ? false : null;
    case '>': return lo > value ? true : hi <= value ? false : null;
    case '<=': return hi <= value ? true : lo > value ? false : null;
    case '<': return hi < value ? true : lo >= value ? false : null;
    case 'between': return lo >= value[0] && hi <= value[1] ? true : hi < value[0] || lo > value[1] ? false : null;
    default: return null;
  }
}

export function factsIn(test, out = new Set()) {
  if (!test) return out;
  if (test[0] === 'all' || test[0] === 'any') test[1].forEach(t => factsIn(t, out));
  else if (test[0] !== 'team') out.add(test[0]);
  return out;
}

// met, notmet, ask (a question would help) or team (the study team checks it).
export function reqStatus(req, facts) {
  const result = evalTest(req.test, facts);
  if (result === true) return 'met';
  if (result === false) return 'notmet';
  const open = [...factsIn(req.test)].filter(f => !facts[f]);
  return open.length ? 'ask' : 'team';
}

export function checkable(req) {
  return factsIn(req.test).size > 0;
}

export function assess(trial, facts) {
  const rows = trial.reqs.map(req => ({ req, status: reqStatus(req, facts) }));
  const count = s => rows.filter(r => r.status === s).length;
  const canCheck = trial.reqs.filter(checkable).length;
  const met = count('met');
  const notmet = count('notmet');
  // Share of the whole list confirmed. Lines only the study team can check
  // count as not confirmed yet, so a trial that checks a lot at screening
  // can't look like a sure thing.
  const percent = trial.reqs.length ? Math.round((100 * met) / trial.reqs.length) : 0;
  let fit = 'worth';
  if (notmet) fit = 'notfit';
  else if (percent >= 70) fit = 'strong';
  return {
    rows, met, notmet, ask: count('ask'), team: count('team'), canCheck, total: trial.reqs.length,
    percent, fit, sureness: canCheck / trial.reqs.length,
    firstProblem: rows.find(r => r.status === 'notmet')?.req.text ?? null,
  };
}

export function trialsFor(data, condition) {
  return data.trials.filter(t => t.groups.includes(condition));
}

// The unanswered question that would settle lines in the most trials that are
// still possible. Ties go to the order in data.priority.
export function nextQuestion(data, facts, condition, skip = []) {
  const live = trialsFor(data, condition).filter(t => assess(t, facts).notmet === 0);
  const score = new Map();
  for (const trial of live) {
    const touched = new Set();
    for (const req of trial.reqs) {
      if (reqStatus(req, facts) !== 'ask') continue;
      for (const f of factsIn(req.test)) if (!facts[f] && data.questions[f]) touched.add(f);
    }
    for (const f of touched) score.set(f, (score.get(f) || 0) + 1);
  }
  const order = f => { const i = data.priority.indexOf(f); return i === -1 ? 999 : i; };
  const best = [...score.entries()]
    .filter(([f]) => !skip.includes(f))
    .sort((a, b) => b[1] - a[1] || order(a[0]) - order(b[0]));
  return best.length ? { fact: best[0][0], trials: best[0][1] } : null;
}

export function distanceKm(a, b) {
  if (!a || !b) return null;
  const rad = d => (d * Math.PI) / 180;
  const dLat = rad(b[0] - a[0]);
  const dLon = rad(b[1] - a[1]);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a[0])) * Math.cos(rad(b[0])) * Math.sin(dLon / 2) ** 2;
  return 2 * 6371 * Math.asin(Math.sqrt(h));
}

// Matches first (best fit, then most of the trial we could check, then
// closest), and trials that are not a fit right now last.
export function rank(data, facts, condition, sort = 'fit') {
  const area = data.areas.find(a => a.id === facts.area?.value);
  const list = trialsFor(data, condition).map(trial => ({
    trial, result: assess(trial, facts), km: distanceKm(area?.at, trial.at),
  }));
  const byFit = (a, b) => b.result.percent - a.result.percent || a.result.ask - b.result.ask || (a.km ?? 0) - (b.km ?? 0);
  const byDistance = (a, b) => (a.km ?? 0) - (b.km ?? 0) || byFit(a, b);
  const fits = list.filter(x => x.result.fit !== 'notfit').sort(sort === 'distance' ? byDistance : byFit);
  const notFits = list.filter(x => x.result.fit === 'notfit').sort(byFit);
  return { fits, notFits };
}
