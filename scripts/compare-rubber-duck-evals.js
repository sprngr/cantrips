#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function fail(message) {
  console.error(`error: ${message}`);
  process.exit(1);
}

function readJson(filePath) {
  const full = path.resolve(filePath);
  if (!fs.existsSync(full)) fail(`file not found: ${full}`);
  try {
    return { path: full, data: JSON.parse(fs.readFileSync(full, 'utf8')) };
  } catch (err) {
    fail(`invalid JSON at ${full}: ${err.message}`);
  }
}

function toNumberOrNull(v) {
  return typeof v === 'number' && Number.isFinite(v) ? v : null;
}

function get(obj, dotted, fallback = null) {
  const parts = dotted.split('.');
  let cur = obj;
  for (const p of parts) {
    if (cur == null || typeof cur !== 'object' || !(p in cur)) return fallback;
    cur = cur[p];
  }
  return cur;
}

function diffNum(base, cand) {
  if (base == null || cand == null) return null;
  return cand - base;
}

function stringifyDelta(n) {
  if (n == null) return 'n/a';
  const sign = n > 0 ? '+' : '';
  return `${sign}${n}`;
}

function formatCategoryCounts(counts) {
  if (!counts || typeof counts !== 'object') return '(none)';
  const keys = Object.keys(counts).sort();
  if (!keys.length) return '(none)';
  return keys.map((k) => `${k}:${counts[k]}`).join(', ');
}

function markdownReport(result) {
  const b = result.baseline;
  const c = result.candidate;
  const d = result.delta;
  const scoreRows = result.scored_fields.rows;

  const scoredTable = scoreRows.length
    ? scoreRows
        .map((row) => `| ${row.field} | ${row.baseline ?? 'n/a'} | ${row.candidate ?? 'n/a'} | ${row.delta_display} |`)
        .join('\n')
    : '| (none found) | n/a | n/a | n/a |';

  return [
    '# Rubber Duck Eval Compare Summary',
    '',
    `Generated: ${result.generated_at}`,
    '',
    '## Inputs',
    '',
    '- Baseline: `' + result.input.baseline + '`',
    '- Candidate: `' + result.input.candidate + '`',
    '',
    '## Validation Summary',
    '',
    '| Metric | Baseline | Candidate | Delta (cand-base) |',
    '|---|---:|---:|---:|',
    `| ok | ${b.ok} | ${c.ok} | n/a |`,
    `| case_count | ${b.case_count} | ${c.case_count} | ${d.case_count_display} |`,
    `| error_count | ${b.error_count} | ${c.error_count} | ${d.error_count_display} |`,
    '',
    `- Baseline categories: ${b.category_counts_text}`,
    `- Candidate categories: ${c.category_counts_text}`,
    '',
    '## Optional Scored Fields',
    '',
    '| Field | Baseline | Candidate | Delta (cand-base) |',
    '|---|---:|---:|---:|',
    scoredTable,
    '',
    '## Notes',
    '',
    '- Compare script is report-only and always exits 0.',
    '- Missing scored fields are treated as optional and shown as `n/a`.',
    ''
  ].join('\n');
}

function main() {
  const args = parseArgs(process.argv);
  if (!args.baseline || !args.candidate || !args.out) {
    fail('usage: node scripts/compare-rubber-duck-evals.js --baseline <json> --candidate <json> --out <json> [--summary <md>]');
  }

  const baseline = readJson(args.baseline);
  const candidate = readJson(args.candidate);
  const outJsonPath = path.resolve(args.out);
  const outMdPath = path.resolve(args.summary || outJsonPath.replace(/\.json$/i, '.md'));

  const bData = baseline.data || {};
  const cData = candidate.data || {};

  const bCaseCount = toNumberOrNull(get(bData, 'summary.case_count'));
  const cCaseCount = toNumberOrNull(get(cData, 'summary.case_count'));
  const bErrCount = toNumberOrNull(get(bData, 'summary.error_count'));
  const cErrCount = toNumberOrNull(get(cData, 'summary.error_count'));

  const candidateScoreFields = [
    'summary.weighted_total',
    'summary.safety_score',
    'summary.routing_score',
    'summary.contract_score',
    'summary.root_cause_score',
    'summary.patch_discipline_score',
    'summary.review_signal_score',
    'summary.efficiency_score'
  ];

  const scoredRows = candidateScoreFields
    .map((field) => {
      const bv = toNumberOrNull(get(bData, field));
      const cv = toNumberOrNull(get(cData, field));
      if (bv == null && cv == null) return null;
      const dv = diffNum(bv, cv);
      return {
        field,
        baseline: bv,
        candidate: cv,
        delta: dv,
        delta_display: stringifyDelta(dv)
      };
    })
    .filter(Boolean);

  const report = {
    generated_at: new Date().toISOString(),
    mode: 'report-only',
    input: {
      baseline: baseline.path,
      candidate: candidate.path
    },
    baseline: {
      ok: Boolean(bData.ok),
      case_count: bCaseCount,
      error_count: bErrCount,
      category_counts: get(bData, 'summary.category_counts', {}),
      category_counts_text: formatCategoryCounts(get(bData, 'summary.category_counts', {}))
    },
    candidate: {
      ok: Boolean(cData.ok),
      case_count: cCaseCount,
      error_count: cErrCount,
      category_counts: get(cData, 'summary.category_counts', {}),
      category_counts_text: formatCategoryCounts(get(cData, 'summary.category_counts', {}))
    },
    delta: {
      case_count: diffNum(bCaseCount, cCaseCount),
      case_count_display: stringifyDelta(diffNum(bCaseCount, cCaseCount)),
      error_count: diffNum(bErrCount, cErrCount),
      error_count_display: stringifyDelta(diffNum(bErrCount, cErrCount))
    },
    scored_fields: {
      rows: scoredRows
    }
  };

  fs.mkdirSync(path.dirname(outJsonPath), { recursive: true });
  fs.mkdirSync(path.dirname(outMdPath), { recursive: true });
  fs.writeFileSync(outJsonPath, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  fs.writeFileSync(outMdPath, `${markdownReport(report)}\n`, 'utf8');

  console.log('rubber-duck eval compare');
  console.log(`- baseline: ${baseline.path}`);
  console.log(`- candidate: ${candidate.path}`);
  console.log(`- baseline errors: ${report.baseline.error_count ?? 'n/a'}`);
  console.log(`- candidate errors: ${report.candidate.error_count ?? 'n/a'}`);
  console.log(`- delta errors: ${report.delta.error_count_display}`);
  console.log(`- scored fields found: ${scoredRows.length}`);
  console.log(`- out json: ${outJsonPath}`);
  console.log(`- out md: ${outMdPath}`);
  console.log('status: REPORT');

  process.exit(0);
}

main();
