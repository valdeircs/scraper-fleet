import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const read = name => JSON.parse(fs.readFileSync(new URL(name, root), 'utf8'));
const workflow = read('n8n/website-to-source-packets.json');
const pages = read('examples/sample-pages.json');
const report = read('examples/sample-run-summary.json');
const clone = value => JSON.parse(JSON.stringify(value));
const node = name => workflow.nodes.find(item => item.name === name);
const data = new Map();

function run(name, input, { runIndex = 0, now = Date.now(), source } = {}) {
  const items = (Array.isArray(input) ? input : [input]).map(json => ({ json: clone(json) }));
  const context = vm.createContext({
    Date: class extends Date { static now() { return now; } },
    $runIndex: runIndex,
    $input: { first: () => items[0], all: () => items },
    $: title => ({ first: () => ({ json: clone(data.get(title)) }) }),
  });
  const output = new vm.Script(`(function () { ${source ?? node(name).parameters.jsCode}\n})()`).runInContext(context, { timeout: 2000 });
  return clone(output);
}

let count = 0;
function test(name, callback) { callback(); count += 1; process.stdout.write(`PASS ${name}\n`); }
const configured = run('Configure crawl', {})[0].json;
data.set('Configure crawl', configured);
const started = { id: 'exampleRunId', status: 'RUNNING', defaultDatasetId: 'exampleDataset', defaultKeyValueStoreId: 'exampleStore' };
data.set('Start bounded crawl', { data: started });

test('public export is inactive, manual and contains no credential data', () => {
  assert.equal(workflow.active, false);
  assert.deepEqual(workflow.pinData, {});
  assert.equal(workflow.nodes.filter(n => /Trigger$/.test(n.type)).length, 1);
  assert.equal(workflow.nodes.filter(n => n.type.endsWith('.httpRequest')).length, 5);
  assert(workflow.nodes.every(n => !n.credentials));
  for (const n of workflow.nodes.filter(n => n.type.endsWith('.httpRequest'))) {
    assert.equal(n.parameters.genericAuthType, 'httpHeaderAuth');
    assert.equal(n.retryOnFail, false);
    assert(n.parameters.url.includes('https://api.apify.com/v2/'));
  }
  assert(!JSON.stringify(workflow).match(/apify_api_|\/Users\/|\/private\/|token=/i));
});

test('configured input matches real sample input with bounded run options', () => {
  assert.deepEqual(configured.input, read('examples/input.json'));
  assert.deepEqual(configured.runOptions, { build: '0.2.2', memory: 512, timeout: 180, maxTotalChargeUsd: 0.10 });
});
test('Code configuration works without URL global and rejects malformed URL shapes', () => {
  for (const invalid of ['javascript:alert(1)', 'https://user:pass@example.org/', 'https://example.org/with space', 'https://', 'https://example.org\\path']) {
    const source = node('Configure crawl').parameters.jsCode.replace("'https://makorev.com/'", JSON.stringify(invalid));
    assert.throws(() => run('Configure crawl', {}, { source }), invalid);
  }
});
test('running crawl polls and successful crawl finishes', () => {
  assert.equal(run('Inspect run', { data: started })[0].json.finished, false);
  assert.equal(run('Inspect run', { data: { ...started, status: 'SUCCEEDED' } })[0].json.finished, true);
});
test('poll timeout, unknown status and malformed status request an abort', () => {
  assert.equal(run('Inspect run', { data: started }, { runIndex: 80 })[0].json.stopPolling, true);
  assert.equal(run('Inspect run', { data: started }, { now: configured.pollingDeadline + 1 })[0].json.stopPolling, true);
  assert.equal(run('Inspect run', { error: 'network error' })[0].json.stopPolling, true);
  assert.equal(run('Inspect run', { data: { ...started, status: 'UNKNOWN' } })[0].json.stopPolling, true);
  assert.equal(run('Inspect run', { data: { ...started, id: 'differentRun' } })[0].json.stopPolling, true);
});
test('failed runs and invalid storage IDs do not advance', () => {
  assert.throws(() => run('Require successful run', { run: { ...started, status: 'FAILED' } }));
  assert.throws(() => run('Require successful run', { run: { ...started, status: 'SUCCEEDED', defaultDatasetId: '../bad' } }));
});
test('complete exact-seed run passes despite pageLimitReached', () => {
  assert.equal(report.pageLimitReached, true);
  data.set('Check crawl coverage', run('Check crawl coverage', report)[0].json);
});
test('incomplete, failed, empty and truncated coverage all stop', () => {
  for (const key of ['failedRequestCount', 'unprocessedInputCount', 'skippedDueToLimitCount', 'pendingRequestCount', 'truncatedPageCount']) {
    assert.throws(() => run('Check crawl coverage', { ...report, [key]: 1 }), key);
  }
  for (const key of ['markdownTruncatedPageCount', 'emptyMarkdownPageCount']) {
    assert.throws(() => run('Check crawl coverage', { ...report, aiExport: { ...report.aiExport, [key]: 1 } }), key);
  }
  assert.throws(() => run('Check crawl coverage', { ...report, outcome: 'failed' }));
  assert.throws(() => run('Check crawl coverage', { ...report, returnedPageCount: 0 }));
  assert.throws(() => run('Check crawl coverage', { ...report, fatalError: {} }));
});
const actual = run('Validate pages and build packets', pages)[0].json;
test('real owned-page evidence yields 2 pages and 33 source packets', () => {
  assert.equal(actual.coverage.pageCount, 2);
  assert.equal(actual.sourcePackets.length, 33);
  assert.equal(actual.coverage.oversizedChunkCount, 0);
  assert(actual.sourcePackets.every(p => p.sourceUrl.startsWith('https://makorev.com/')));
  assert.equal(run('Source packets', actual).length, 33);
});
test('missing pages, modified chunk counts, missing source and duplicate IDs stop', () => {
  assert.throws(() => run('Validate pages and build packets', pages.slice(0, 1)));
  const badCount = clone(pages); badCount[0].chunks[0].characterCount += 1;
  assert.throws(() => run('Validate pages and build packets', badCount));
  const badSource = clone(pages); badSource[0].chunks[0].sourceUrl = 'https://example.org/';
  assert.throws(() => run('Validate pages and build packets', badSource));
  const duplicate = clone(pages); duplicate[0].chunks[1].id = duplicate[0].chunks[0].id;
  assert.throws(() => run('Validate pages and build packets', duplicate));
  const truncated = clone(pages); truncated[0].markdownTruncated = true;
  assert.throws(() => run('Validate pages and build packets', truncated));
});
test('oversized content stays intact with a visible flag', () => {
  const large = clone(pages); large[0].chunks[0].oversized = true;
  data.set('Check crawl coverage', { report: { ...report, aiExport: { ...report.aiExport, oversizedChunkCount: 1 } } });
  const out = run('Validate pages and build packets', large)[0].json;
  assert.equal(out.coverage.oversizedChunkCount, 1);
  assert.equal(out.sourcePackets[0].oversized, true);
  assert.equal(out.sourcePackets[0].content, pages[0].chunks[0].content);
  data.set('Check crawl coverage', { report });
});

fs.writeFileSync(new URL('examples/sample-source-packets.json', root), JSON.stringify(actual, null, 2) + '\n');
process.stdout.write(`${count} checks passed. Regenerated sample-source-packets.json from the observed dataset.\n`);
