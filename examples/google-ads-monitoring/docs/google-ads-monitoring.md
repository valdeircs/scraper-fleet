# A weekly Google Ads creative review

The job is simple: inspect public creatives from a competitor account, then return to the same monitor to see what it observes for the first time or finds changed. This guide uses [Mako’s Google Ads Competitor Tracker](https://apify.com/agency-shift/google-ads-competitor-tracker), published as `agency-shift/google-ads-competitor-tracker`.

## 1. Select a target and country

Open [Google Ads Transparency Center](https://adstransparency.google.com/) and identify the advertiser account you want to follow. Copy its advertiser ID or advertiser-page URL. For example, the bundled input uses `AR10888897372843147265`, the public Notion Labs Japan advertiser account, and `JP` for ads shown in Japan. The example does not imply endorsement or a customer relationship.

Use a domain when discovery is the goal, and an advertiser ID when you want a particular account. A domain search can return agencies and other advertisers associated with that domain. The Actor accepts up to ten targets combined. Filters inside pasted Google URLs are not imported: set `region` and `format` explicitly.

The country filter describes **where the ads were shown**, not where the advertiser is registered. No platform or date-range filter is available in the verified 0.2.2 input schema.

## 2. Inspect a small snapshot

Use [snapshot-input.json](../examples/snapshot-input.json). It requests at most 20 records and 20 observations for the target. Optional preview extraction is enabled with at most 20 preview requests across the run; usable text is not guaranteed.

In Apify Console, set a **$0.05 maximum charge** and a **180-second timeout** before starting. Open the dataset and follow a `creativeUrl` to the public source. Some text or image fields may be null. Enabling `includeCreativeDetails` can recover more available copy or images, but supported previews may still be empty or unavailable. It does not run OCR, execute scripts, or transcribe video.

Check **SUMMARY** in the run’s key-value store. Do not equate the platform run status `SUCCEEDED` with exhaustive data coverage: the Actor separately reports source coverage, limits, errors, and targets it did not reach.

## 3. Establish the comparison baseline

Duplicate the public [Track Notion Japan Google ad creatives task](https://apify.com/agency-shift/google-ads-competitor-tracker/examples/track-notion-japan-google-ad-creatives) into your account, or switch to [monitor-input.json](../examples/monitor-input.json):

```json
{
  "advertiserIds": ["AR10888897372843147265"],
  "region": "JP",
  "format": "ALL",
  "mode": "changes",
  "monitorName": "mako-notion-japan-example-20261002",
  "emitInitialSnapshot": true,
  "maxResults": 20,
  "maxAdsPerDomain": 20,
  "includeCreativeDetails": true,
  "maxCreativeDetails": 20
}
```

A Snapshot run does not establish a Changes baseline. On the first Changes run, `emitInitialSnapshot: true` returns `initial` records while creating history. Set it to `false` if you want to seed history without paying for initial output records; startup still applies. Budget and timeout belong to the run configuration, not this JSON object.

For a different advertiser, replace the ID and choose your country. Use a descriptive monitor name. History belongs to the Apify account and Actor; another user does not inherit your baseline.

The [dated example](../examples/evidence-2026-10-02.json) used this input on 2 October 2026: 13 initial records, then zero new or changed records from an immediate repeat that freshly observed the same 13 creatives. This verifies that small example at that time, not what another run will return next week. All observed text fields were null despite optional preview extraction; the one attempted preview failed.

## 4. Repeat and interpret the difference

Run the same Changes input next week. Keep the monitor name, target, region, format, and detail settings consistent. Country and format have separate histories; a new monitor name creates a separate baseline. Turning preview extraction on later can reveal previously missing text, which may register as a change.

| Event | What it means | What it does not establish |
| --- | --- | --- |
| `initial` | Observation delivered while establishing this baseline | A new campaign |
| `new` | First observation of this creative in this monitor | The actual launch date |
| `changed` | Tracked values differ; review `changedFields`, `before`, and `after` | A performance improvement |
| No records | No events were delivered | No ads exist, no changes happened, or coverage was complete |

Review SUMMARY before interpreting an empty result. `scannedTargets` counts fresh source scans; delivery of queued records does not count as a new scan. The per-target details distinguish complete, empty, capped, and failed responses. `sourceQuality` separately describes available text/images and optional preview attempts. A complete response for a query does not prove that Google exposes every ad or all its copy.

The comparison uses advertiser name, matched domain, format, available text, image, and a stable preview fingerprint. Routine `lastShown` updates do not create change events. Missing later values do not erase known comparison values. Missing ads do not produce “stopped” or retirement events.

For a weekly review, group records by advertiser and event type; inspect source links; summarize only supported differences. Keep `observedAt` with the evidence. Deduplicate downstream by `eventId` because interrupted delivery can repeat the same event and charge again.

## 5. Schedule only after the first two runs make sense

Save the working input as an Apify task and attach a weekly [Apify Schedule](https://docs.apify.com/platform/schedules) using the same input and bounded run settings. Review your timezone and account budget. The Actor itself does not send alerts; use Apify integrations or webhooks for delivery.

With multiple targets and a small output cap, one run may not scan every target. Changes mode rotates the starting target across runs; SUMMARY remains the source of truth about what was reached. Avoid overlapping runs of the same monitor.

## Use the Python starter

Set your own `APIFY_TOKEN` in the environment. From this starter directory:

```sh
python3 examples/run_tracker.py --input examples/monitor-input.json \
  --max-usd 0.05 --timeout 180 --output first-review.json
```

On the next run, choose a new output name such as `second-review.json`. The client saves dataset records and SUMMARY together. It sends server-side charge/time limits, polls the single created run, and makes a best-effort abort request if polling fails or is interrupted. There is no automatic retry of paid run creation. If creation times out, check Apify Console before invoking it again: the server may have accepted the first request.

The script uses Python’s standard library and does not install dependencies. Mocked tests run without an Apify token or network:

```sh
python3 -m unittest discover -s tests -v
```

These tests validate client behavior, not current Google availability or live account billing. The starter has not completed an end-to-end paid client run.

## Use curl

These examples require `curl`, `jq`, and an environment variable `APIFY_TOKEN` containing your own token. Run them from this starter directory. The following request creates **one chargeable run**. Do not retry it automatically if the response is lost.

```sh
curl --fail --silent --show-error --max-time 45 \
  --request POST \
  --header "Authorization: Bearer ${APIFY_TOKEN}" \
  --header 'Content-Type: application/json' \
  --data-binary @examples/monitor-input.json \
  'https://api.apify.com/v2/actors/agency-shift~google-ads-competitor-tracker/runs?maxTotalChargeUsd=0.05&timeout=180&restartOnError=false' \
  --output run.json
```

Read its status using the run ID in `run.json`. Repeat this read-only request every few seconds until status is `SUCCEEDED`, `FAILED`, `ABORTED`, or `TIMED-OUT`:

```sh
RUN_ID=$(jq -er '.data.id' run.json)
curl --fail --silent --show-error --max-time 45 \
  --header "Authorization: Bearer ${APIFY_TOKEN}" \
  "https://api.apify.com/v2/actor-runs/${RUN_ID}" \
  --output run-status.json
jq -r '.data.status' run-status.json
```

Then fetch that run’s dataset and coverage:

```sh
DATASET_ID=$(jq -er '.data.defaultDatasetId' run-status.json)
STORE_ID=$(jq -er '.data.defaultKeyValueStoreId' run-status.json)
curl --fail --silent --show-error --max-time 45 \
  --header "Authorization: Bearer ${APIFY_TOKEN}" \
  "https://api.apify.com/v2/datasets/${DATASET_ID}/items?format=json&limit=20" \
  --output records.json
curl --fail --silent --show-error --max-time 45 \
  --header "Authorization: Bearer ${APIFY_TOKEN}" \
  "https://api.apify.com/v2/key-value-stores/${STORE_ID}/records/SUMMARY" \
  --output summary.json
```

The 20-row fetch matches this example’s output limit. Increase it or paginate when you intentionally raise `maxResults`; the Python client paginates. These filenames are overwritten by curl, so move them before another run. Do not enable shell tracing or put the token into a URL. See Apify’s [run API](https://docs.apify.com/api/v2/actors-runs-post) and [dataset items API](https://docs.apify.com/api/v2/dataset-items-get) for the underlying contract.

## Limits to keep with any report

Use this data to support creative research. It does not supply spend, impressions, conversions, ROI, or evidence that a campaign is currently delivering. Caps and source changes can leave gaps. Google may omit fields or change responses. An exact advertiser account is a narrower target than a domain, but it is not necessarily every account associated with a brand.

Version and input behavior were checked against published build **0.2.2 on 2 October 2026**. Pricing, client interfaces, and source availability can change; inspect the current Actor listing and [connection guide](connect-ai-assistants.md) before automating.
