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

function isNonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function isStringArray(value) {
  return Array.isArray(value) && value.every((v) => typeof v === 'string');
}

function validateCaseShape(testCase, index) {
  const errors = [];
  const prefix = `cases[${index}]`;

  if (!isNonEmptyString(testCase?.id)) errors.push(`${prefix}.id missing/empty`);
  if (!isNonEmptyString(testCase?.category)) errors.push(`${prefix}.category missing/empty`);
  if (!isNonEmptyString(testCase?.title)) errors.push(`${prefix}.title missing/empty`);
  if (!isNonEmptyString(testCase?.prompt)) errors.push(`${prefix}.prompt missing/empty`);
  if (!isStringArray(testCase?.input_artifacts)) errors.push(`${prefix}.input_artifacts must be string[]`);

  const expected = testCase?.expected;
  if (!expected || typeof expected !== 'object') {
    errors.push(`${prefix}.expected missing/object required`);
    return errors;
  }

  if (!isNonEmptyString(expected.primary_route)) errors.push(`${prefix}.expected.primary_route missing/empty`);
  if (!Array.isArray(expected.chain) || !expected.chain.every((x) => typeof x === 'string')) {
    errors.push(`${prefix}.expected.chain must be string[]`);
  }
  if (!isStringArray(expected.must_have)) errors.push(`${prefix}.expected.must_have must be string[]`);
  if (!isStringArray(expected.must_not)) errors.push(`${prefix}.expected.must_not must be string[]`);

  const assertions = expected.assertions;
  if (!assertions || typeof assertions !== 'object') {
    errors.push(`${prefix}.expected.assertions missing/object required`);
    return errors;
  }
  if (!isStringArray(assertions.must_match)) errors.push(`${prefix}.expected.assertions.must_match must be string[]`);
  if (!isStringArray(assertions.must_not_match)) errors.push(`${prefix}.expected.assertions.must_not_match must be string[]`);

  return errors;
}

function main() {
  const args = parseArgs(process.argv);
  const casesPathArg = args.cases;
  const outPathArg = args.out;

  if (!casesPathArg || !outPathArg) {
    fail('usage: node scripts/run-rubber-duck-evals.js --cases <path> --out <path>');
  }

  const casesPath = path.resolve(casesPathArg);
  const outPath = path.resolve(outPathArg);

  if (!fs.existsSync(casesPath)) {
    fail(`cases file not found: ${casesPath}`);
  }

  let doc;
  try {
    doc = JSON.parse(fs.readFileSync(casesPath, 'utf8'));
  } catch (err) {
    fail(`invalid JSON in cases file: ${err.message}`);
  }

  const errors = [];
  if (!doc || typeof doc !== 'object') errors.push('root must be object');
  if (!doc.metadata || typeof doc.metadata !== 'object') errors.push('metadata missing/object required');
  if (!Array.isArray(doc.cases)) errors.push('cases missing/array required');

  const ids = new Set();
  const categoryCounts = {};

  if (Array.isArray(doc.cases)) {
    doc.cases.forEach((testCase, index) => {
      errors.push(...validateCaseShape(testCase, index));
      if (isNonEmptyString(testCase?.id)) {
        if (ids.has(testCase.id)) {
          errors.push(`duplicate case id: ${testCase.id}`);
        }
        ids.add(testCase.id);
      }
      if (isNonEmptyString(testCase?.category)) {
        categoryCounts[testCase.category] = (categoryCounts[testCase.category] || 0) + 1;
      }
    });
  }

  const result = {
    ok: errors.length === 0,
    generated_at: new Date().toISOString(),
    input: {
      cases: casesPath,
    },
    summary: {
      case_count: Array.isArray(doc?.cases) ? doc.cases.length : 0,
      category_counts: categoryCounts,
      error_count: errors.length,
    },
    errors,
  };

  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, `${JSON.stringify(result, null, 2)}\n`, 'utf8');

  const categories = Object.keys(categoryCounts)
    .sort()
    .map((k) => `${k}:${categoryCounts[k]}`)
    .join(', ');

  console.log('rubber-duck eval schema validation');
  console.log(`- cases: ${result.summary.case_count}`);
  console.log(`- categories: ${categories || '(none)'}`);
  console.log(`- errors: ${result.summary.error_count}`);
  console.log(`- out: ${outPath}`);

  if (!result.ok) {
    console.log('status: FAIL');
    process.exit(2);
  }

  console.log('status: PASS');
}

main();
