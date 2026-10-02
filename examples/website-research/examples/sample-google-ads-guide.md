[← All posts](https://makorev.com/blog)

Valdeir Lima · 2 October 2026 · 7 min read

# How to track competitor Google ads with Apify and Claude

A useful competitor ad review starts with evidence: which creative you observed, where you found it, and what changed since the previous check. This guide builds that workflow with Mako's Google Ads Competitor Tracker on Apify, from a small first run to a recurring watch that an AI assistant can read.

Use it to prepare an agency creative review, follow an advertiser in a target market, or keep a source-linked research log. You get public observations from the [Google Ads Transparency Center](https://adstransparency.google.com/). Spend, conversions and profitability are outside this dataset.

[Try Google Ads Competitor Tracker →](https://apify.com/agency-shift/google-ads-competitor-tracker)

Runs on your Apify account. Review the published pricing and set a run budget before starting.

## 1\. Start with one advertiser and one country

For an exact account, copy its advertiser ID from its Google Transparency page. This example uses [Notion Labs Japan's advertiser account](https://adstransparency.google.com/advertiser/AR10888897372843147265?region=JP)and asks for ads shown in Japan. The country filter describes where the ads were shown, not the advertiser's registration country.

Open the [prepared Notion Japan example](https://apify.com/agency-shift/google-ads-competitor-tracker/examples/track-notion-japan-google-ad-creatives)to inspect and run it, or open the Actor's Input tab, switch to JSON, and paste the following input. It saves a baseline and delivers up to 20 initial observations. Keep the monitor name so later runs can compare against the same history.

A bounded first run — JSON input

```
{
  "advertiserIds": [
    "AR10888897372843147265"
  ],
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

Set the maximum Actor charge to **$0.05** in the run options, then start. That is a ceiling, not a prepaid fee. Wait for the run to finish, then open both its dataset and the `SUMMARY` record in its key-value store.

To research a domain instead, replace `advertiserIds` with` "domains": ["your-competitor.com"]`. Domain results can include agencies or other advertisers associated with that site; check the advertiser identity before attributing an ad to a brand. You can supply up to ten domains and advertiser IDs combined. Set country and format explicitly: filters in a pasted Google URL are not imported.

## 2\. Turn the dataset into a reviewable ad log

Keep a compact table for the people doing the review. Export JSON for complete nested data, or CSV/Excel for a spreadsheet. Preserve the original creative link alongside every observation so someone can check the source.

Recommended fields and their meaning
| Field | What to use it for |
| --- | --- |
| advertiserName + advertiserId | Identify the public advertiser account. |
| creativeId + creativeUrl | Identify the creative and open its source page. |
| searchRegion + format | Keep the country scope and creative format visible. |
| observedAt | Record when this monitor collected the observation. |
| firstShown + lastShown | Retain Google's dates when supplied; these are not performance data. |
| eventType + changedFields | Separate the baseline, newly observed ads and changes. |
| before + after + eventId | Inspect changed values and deduplicate repeated deliveries. |

Some rows have no readable ad copy. Missing text or images stay `null`. The example enables `includeCreativeDetails`, with a ceiling of 20 preview requests across the run. Set it to `false` for listing data alone. Optional extraction visits supported public previews; it does not run OCR, transcribe videos or guarantee complete copy.

### What the example actually returned

On 2 October 2026, the first test delivered 13 initial observations. All 13 had creative links, 12 had image URLs, and none had readable ad copy. One optional preview request failed. The listing scan succeeded; the missing copy remained explicit. Here is a selected set of fields from one real record:

Observed output — real record, selected fields

```
{
  "advertiserName": "Notion Labs Japan合同会社",
  "advertiserId": "AR10888897372843147265",
  "creativeId": "CR15371418889862774785",
  "searchRegion": "JP",
  "format": "TEXT",
  "adText": null,
  "observedAt": "2026-10-02T12:44:11.043Z",
  "eventType": "initial",
  "creativeUrl": "https://adstransparency.google.com/advertiser/AR10888897372843147265/creative/CR15371418889862774785?region=JP"
}
```

[Open this creative's Google source page](https://adstransparency.google.com/advertiser/AR10888897372843147265/creative/CR15371418889862774785?region=JP). A repeat test observed the same 13 creatives and delivered zero new or changed records. That demonstrates deduplication for these two runs, not a promise that future scans will return the same data or that every ad was captured.

Check `SUMMARY` for successful scans, errors, capped coverage and preview availability. A successful run with zero changes can be legitimate. A failed source request, an unvisited target and a genuinely empty response should lead to different decisions.

Use the [public input files, sample output and monitoring examples on GitHub](https://github.com/valdeircs/scraper-fleet/tree/main/examples/google-ads-monitoring) to reproduce the workflow.

## 3\. Repeat the same watch and review the differences

Save the input as an Apify task. Add an Apify Schedule at a cadence you actually review, such as once a week. The Actor itself does not create the schedule or send notifications; connect Apify webhooks or your own workflow for delivery.

1.  Keep `mode: "changes"`, the monitor name, target, country and format consistent. Country and format changes have separate baselines.
2.  On the first run, `emitInitialSnapshot: true` delivers the starting observations. Set it to `false` if you only want to seed history.
3.  On later runs, review `new` and `changed` events. New means first observed by this monitor; a changed event includes previous and current values.
4.  Deduplicate exports or webhook deliveries by `eventId`. Delivery is at least once, so an interrupted run can repeat an event.

For an agency review, group observations by advertiser and format, open the source links, and annotate the message or visual you can actually inspect. Let an assistant summarize that evidence, then review its interpretation before using it in a client report.

`maxResults` caps delivered records across the run.` maxAdsPerDomain` caps observations per target, including advertiser IDs and unchanged ads. Keep both small while testing. Increasing only the output cap does not make a source scan complete.

## 4\. Budget for records, including the first baseline

The base price is **$0.78 per 1,000 delivered records**, before plan discounts, plus a **$0.00005 startup event**. Startup is charged per allocated GB with a minimum of one event. Platform compute is included. Check the [current Actor pricing](https://apify.com/agency-shift/google-ads-competitor-tracker/pricing) before running.

At those base rates and one startup event, 20 delivered records cost about **$0.01565**. The $0.05 ceiling above leaves room for this example; the minimum permitted maximum-charge budget is $0.01. Actual charges depend on delivered records, memory, applicable discounts and the current published price.

For the 13 records in our test, the base-rate illustration is` 13 × $0.00078 + $0.00005 = $0.01019`. A repeat with no delivered records still has the startup fee. These are customer pricing examples, not a claim about an individual account's invoice.

Snapshot mode charges for every delivered snapshot. Changes mode charges for delivered initial, new and changed records. Unchanged observations and the summary do not add record fees, but startup still applies to an empty run. Optional preview extraction has no separate event fee; it can increase runtime.

## 5\. Give Claude access through Apify's MCP server

Apify hosts the connection; you do not need to build a server. In an installed Claude Code CLI, add this Actor, sign in to your own Apify account through the browser, and check the connection:

Claude Code — run these commands in your terminal

```
claude mcp add --transport http --scope user mako-google-ads 'https://mcp.apify.com?tools=agency-shift/google-ads-competitor-tracker,call-actor'
claude mcp login mako-google-ads
claude mcp get mako-google-ads
```

Look for a connected status. If authentication is still needed, open` /mcp` inside Claude Code and follow the sign-in flow. OAuth connects your own Apify account; do not paste an API token into a shared prompt or public configuration. Runs use your account and normal Actor pricing.

Prompt after connecting — paste the JSON from step 1 with it

```
Use the Apify call-actor tool with:
actor: "agency-shift/google-ads-competitor-tracker"
input: the JSON below
callOptions: {"maxTotalChargeUsd": 0.05, "timeout": 180}

Use call-actor so the spending cap is applied.
Wait for completion, then retrieve the dataset and SUMMARY.
Return advertiser name, format, event type and creative URL.
Explain coverage errors and keep missing values as null.
Do not infer spend, profitability, launches or stopped campaigns.
```

This connection includes the Actor and Apify's generic `call-actor`tool. Use `call-actor` for this example because its` callOptions.maxTotalChargeUsd` field supports the spending cap; the dedicated Actor tool does not expose that option.

A successful connection should let you see the exact Actor run in Apify, retrieve its final status and read its dataset and summary. Seeing a saved connector alone does not prove a run worked. See the [Claude Code MCP reference](https://code.claude.com/docs/en/mcp) and the [Apify MCP guide](https://docs.apify.com/integrations/mcp) for connection details.

We verified an actual capped run and result retrieval through Apify's MCP protocol. The desktop and chat-client sign-in flows below are setup instructions; they were not tested end to end in each client for this guide.

### Claude Desktop and ChatGPT

In Claude Desktop, add a custom remote connector using the URL below and authorize Apify through OAuth. In ChatGPT on the web, use Developer mode and create a custom app with this URL if your account and workspace permit it. Select the app for the request and use the same bounded prompt.

Actor-specific remote MCP URL

```
https://mcp.apify.com?tools=agency-shift/google-ads-competitor-tracker,call-actor
```

Client availability and settings vary. Follow the current [Claude Desktop setup](https://docs.apify.com/integrations/claude-desktop) or [ChatGPT setup](https://docs.apify.com/integrations/chatgpt), and check your workspace's tool permissions. Connecting makes the Actor available to your assistant; it does not guarantee that every AI conversation will discover or recommend it.

## 6\. Keep the conclusions within the evidence

-   Source limits, ordering, blocks and partial responses can affect coverage. This is a bounded observation workflow, not an exhaustive inventory.
-   An absent ad does not establish that a campaign stopped. The Actor does not emit disappearance or retirement events.
-   First observed is different from first launched. Google's first/last-shown dates and the monitor's observation time describe different things.
-   Creative format is not a platform filter. The Actor searches across Google platforms and does not offer date-range filtering.
-   No spend, impressions, conversions, ROI or private Google Ads account data are supplied. Inspect original links before making marketing decisions.

Start with one useful question: what publicly visible creative changed for this advertiser in this market? Keep the source, the observation time and the coverage alongside your answer. That gives the next review a concrete starting point.

## Keep the workflow reproducible

The [GitHub examples](https://github.com/valdeircs/scraper-fleet/tree/main/examples/google-ads-monitoring) contain the input and output files. The [Actor's Issues tab](https://apify.com/agency-shift/google-ads-competitor-tracker/issues) is the place to report a reproducible source or output problem.

Built by Mako. Independent of Google, Notion and the advertisers returned. Examples are research observations, not endorsements or customer results.
