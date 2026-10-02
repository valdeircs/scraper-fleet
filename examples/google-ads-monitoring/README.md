# Review competitors’ Google ad creatives each week

> **Test update — 2 October 2026:** A later end-to-end run of the published Python starter against build 0.2.3 returned zero records and failed with `REDIRECT_REJECTED`. The client saved the failure summary and exited with code 2. A subsequent bounded check on pinned build 0.2.2 succeeded with one ad. The cause remains unresolved: this is intermittent availability, not a proven build regression. Check `SUMMARY` and test your target before depending on scheduled output.

Use Mako’s [Google Ads Competitor Tracker on Apify](https://apify.com/agency-shift/google-ads-competitor-tracker) to collect public ad observations, establish a baseline, and review newly observed or changed creatives on later runs. Mako publishes on Apify as **agency-shift**.

This starter follows one exact advertiser account in Japan. You can replace it with another Google advertiser ID or competitor domain. Results include source links and observation times so you can inspect the evidence behind a creative review.

**“New” means first observed by your monitor.** The data does not establish an ad’s launch date, current delivery, spend, impressions, conversions, or profitability. A bounded scan is not a complete ad inventory.

## Start in Apify

For a prefilled Changes workflow, open [Track Notion Japan Google ad creatives](https://apify.com/agency-shift/google-ads-competitor-tracker/examples/track-notion-japan-google-ad-creatives), duplicate it into your Apify account, and review the input and run limits before starting. It creates your own baseline. To inspect a Snapshot first, follow these steps:

1. Open the [Actor](https://apify.com/agency-shift/google-ads-competitor-tracker) in your own Apify account.
2. Copy [snapshot-input.json](examples/snapshot-input.json) into its JSON input. It targets one public advertiser account, filters for ads shown in Japan, and caps output and observations at 20.
3. Set the maximum run charge to **$0.05** and the timeout to **180 seconds**. These are run options, separate from the input JSON. Review current pricing before starting.
4. Run once. Open the dataset and the **SUMMARY** record in the run’s key-value store. Inspect `creativeUrl`, and check whether the source scan was complete, capped, empty, or failed.
5. For repeat comparisons, use [monitor-input.json](examples/monitor-input.json). The first Changes run creates a baseline. Later runs reuse its monitor name, advertiser, country, format, and detail settings.

A first Changes run normally emits `initial` observations; it does not compare against a previous Snapshot run. [The monitoring walkthrough](docs/google-ads-monitoring.md) explains the second run and how to read coverage.

## A real first run and immediate repeat

On **2 October 2026**, build 0.2.2 ran the bundled Changes input for Notion Labs Japan. The first run observed 13 creatives and delivered 13 `initial` records. An immediate repeat through Apify MCP observed the same 13 creatives and delivered no new or changed records. Both summaries reported one fresh, complete target scan.

The evidence also shows the limits: all 13 `adText` values were null, 12 records had an image URL, and the one attempted preview request failed. Source coverage and creative-text availability are different things. This is a small owner-run demonstration, not evidence of customer adoption or week-over-week performance.

See [three actual output excerpts](examples/observed-2026-10-02.json) and the [two-run evidence summary](examples/evidence-2026-10-02.json). Fields are omitted from the excerpts for readability; values are not invented. Future runs may return different results.

## Run from Python

Requires Python 3.9 or later; no packages to install. Set `APIFY_TOKEN` in your environment using your preferred secret manager. Do not commit it or paste it into a prompt.

```sh
python3 examples/run_tracker.py \
  --input examples/monitor-input.json \
  --max-usd 0.05 \
  --timeout 180 \
  --output first-review.json
```

Run the same command later with a new output filename, for example `second-review.json`. Each invocation can incur Apify charges. The JSON file contains `records`, `summary`, and the final run status. The client sends the budget and timeout to Apify, does not retry run creation, and attempts to abort a known run if polling is interrupted. It never overwrites an existing output file.

Exit code `0` means the run and reported coverage succeeded; `2` means results were saved but the run or coverage was incomplete; `1` means the client could not complete. Check SUMMARY even after success: successful source coverage does not guarantee complete creative text.

The Python starter has eight passing mocked API tests. A live owner-account client run was attempted on 2 October 2026 and correctly surfaced the failed upstream run described above; a successful live Python-client run is not established. See [curl instructions](docs/google-ads-monitoring.md#use-curl) if you prefer raw HTTP.

## Use Claude Code, Claude, or ChatGPT

Apify hosts the MCP server; you do not need to run your own. [Connect an assistant](docs/connect-ai-assistants.md) using your own Apify account, then have it inspect the input and coverage before summarizing observations.

Connecting the tool does not enable a schedule or guarantee recommendations in other people’s chats. Assistant subscriptions and Apify charges are separate. Client availability depends on your plan and workspace permissions.

## What can I change?

| Setting | Use it for |
| --- | --- |
| `domains` or `advertiserIds` | Up to ten combined targets. IDs identify exact Google advertiser accounts; domain matches can include agencies or partners. |
| `region` | Country where ads were shown, such as `JP`, `US`, or `GB`; `anywhere` searches worldwide. This is not advertiser registration country. |
| `format` | `ALL`, `TEXT`, `IMAGE`, or `VIDEO`. This does not select a Google platform. |
| `maxResults` | Maximum paid output records for the whole run. |
| `maxAdsPerDomain` | Maximum observations per target, including unchanged ads and advertiser-ID targets. |
| `includeCreativeDetails` | Optional recovery of available text and images from supported public previews. No OCR or script execution. |
| `maxCreativeDetails` | Maximum preview requests across the whole run. |

The [live Input tab](https://apify.com/agency-shift/google-ads-competitor-tracker/input-schema) is the authoritative input reference. The published version verified for this guide was **0.2.2 on 2 October 2026**. There are no platform or date-range filters in that version.

## Cost and limits

Pricing checked on **2 October 2026**: the base price before plan discounts is **$0.78 per 1,000 delivered records**, plus a **$0.00005 startup event**. Startup is charged per GB of memory with a minimum of one event; the verified default allocation is 256 MB. The minimum maximum-charge setting is $0.01. Platform compute is included; optional previews have no separate event fee.

At that base price, the 13-record example would cost **$0.01019**, and the zero-record repeat **$0.00005**. These are calculated customer-price estimates before plan discounts, not the owner account’s measured bill. Review [current Actor pricing](https://apify.com/agency-shift/google-ads-competitor-tracker) before each new workflow.

The $0.05 budget is a maximum-charge setting, not a prepaid fee or a promised result count. The output cap, observation cap, preview cap, and time limit control different parts of a run.

Snapshots charge for delivered records every time. Changes mode charges for delivered initial, new, and changed records. A startup charge still applies when a run emits no changes. Keep detail settings consistent between runs; newly recovered text can itself create a changed observation.

Missing data stays missing. An absent ad is not evidence that its campaign stopped. Delivery is at least once, so deduplicate by `eventId`; interrupted delivery can repeat an event and its charge. This independent tool is not affiliated with Google or the advertiser in the example.

## Feedback that helps

Report issues in the [Actor’s Issues tab](https://apify.com/agency-shift/google-ads-competitor-tracker/issues), or use the repository’s feedback template. Include redacted input, the coverage result, what you expected, and which decision the output was meant to support. Never attach credentials or private customer data.

If you have used the workflow, an honest review on Apify can help others understand both its value and limitations. Reviewing is optional and carries no reward or requirement.
