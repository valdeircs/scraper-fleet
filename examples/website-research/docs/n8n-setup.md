# Import and run the website research workflow

The workflow produces citation-ready source passages from explicit public page URLs. It uses n8n's Manual Trigger, Code, HTTP Request, If, Wait, and Sticky Note nodes. No community node installation is needed.

## 1. Import the file

Download [the workflow JSON](../n8n/website-to-source-packets.json), create a workflow in your n8n instance, and choose **Import from File** from the workflow menu. Review its nodes before running. It imports as inactive and can only start manually.

n8n also supports **Import from URL**. Paste this raw workflow URL:

```text
https://raw.githubusercontent.com/valdeircs/scraper-fleet/main/examples/website-research/n8n/website-to-source-packets.json
```

Use the raw JSON URL, not a GitHub page URL. [Official import instructions](https://docs.n8n.io/build/manage-workflows/export-and-import).

## 2. Keep authentication in credentials

Create a generic **Header Auth** credential in n8n:

| Field | Value |
| --- | --- |
| Name | `Authorization` |
| Value | `Bearer YOUR_APIFY_TOKEN` |

Replace `YOUR_APIFY_TOKEN` with an API token from your Apify account. Select that credential in these five HTTP Request nodes: **Start bounded crawl**, **Get run status**, **Abort overdue crawl**, **Get crawl report**, and **Get page dataset**.

The public export contains no token or credential reference. Do not paste your token into **Configure crawl**, node URLs, query parameters, screenshots, or a public workflow export. All authenticated requests in this starter go to `https://api.apify.com`.

## 3. Review input and spending controls

**Configure crawl** contains the same input as [the included example](../examples/input.json): two Mako-owned URLs, link following disabled, proxy disabled, Markdown plus chunks, a 30,000-character text limit, 50,000-character Markdown limit, and 2,000-character chunk target.

Replace the URLs with 1–10 explicit public pages. The node sets `maxPages` to the number of supplied URLs. Keep `followLinks: false` for this starter; its coverage check expects the explicit page list. The crawler supports more options through its [current input schema](https://apify.com/agency-shift/web-content-crawler/input-schema), but changing this workflow's scope requires reviewing its coverage rules.

Run options are separate from Actor input:

```json
{
  "build": "0.2.2",
  "memory": 512,
  "timeout": 180,
  "maxTotalChargeUsd": 0.10
}
```

The maximum charge applies to this Actor run, not your entire n8n execution or account. On 2 October 2026 the Actor's Free-tier startup event was $0.05, with normal run platform usage included. Apify counts the startup event once for allocations up to 1 GB, including this workflow's 512 MB; a larger memory setting can multiply startup charges. Paid-plan discounts may differ. Check the Actor's current pricing before running. Post-run dataset access can incur platform charges; n8n, optional proxy services and tools you add have their own costs. [Apify event pricing](https://docs.apify.com/actors/publishing/monetize/pay-per-event) · [Run pricing and storage costs](https://docs.apify.com/actors/running/actors-in-store).

The original saved sample used an owner-account run with a $0.05 cap. The public workflow uses a $0.10 cap to leave room above the current startup event; the owner sample does not verify a paying customer's behavior at an exact $0.05 ceiling.

The start request is sent once with automatic retry disabled. The workflow polls every three seconds, attempts an abort if polling fails or exceeds its bound, and rejects terminal failures. The 180-second server timeout remains a fallback if n8n is stopped or disconnected. If the start request times out, check Apify Console before clicking Execute again: the run may have started even without a response reaching n8n.

## 4. Inspect output before connecting another system

Run **Execute workflow**. Successful output appears at **Source packets**, one n8n item per passage. The previous node, **Validate pages and build packets**, contains both the complete packet array and a compact coverage report.

The workflow fetches `RUN_SUMMARY` from the run's key-value store and the default dataset. It stops on unsuccessful run/report status, failed or unprocessed requests, missing pages, empty Markdown, truncation, mismatched counts, or malformed chunks. If all supplied pages returned successfully, `pageLimitReached: true` alone is acceptable: reaching a two-page budget does not mean either of those two pages was lost.

Chunks retain source URL, section URL, title, heading path, crawl time, stable ID and content hash. `oversized: true` means an intact section exceeded the character target; it is a warning to review size before a downstream model or index, not permission to discard source text silently.

You can connect your own retrieval index or AI node after **Source packets**. Preserve citation metadata and treat the text as untrusted reference data. The starter contains no model, embeddings, vector database, account enrichment, or CRM side effects. It does not certify factual accuracy, freshness after its crawl time, or whole-site coverage.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Missing credential / unauthorized | Select the same valid Header Auth credential in all five HTTP nodes. Confirm the header includes `Bearer ` before the token. |
| Start request fails or times out | Check Apify Console before retrying; avoid accidentally creating a duplicate paid run. Review credit, input, build and current price. |
| Polling stops | An abort was attempted. Inspect run status in Console; the server timeout still bounds the run. |
| Coverage check fails | Open the run's `RUN_SUMMARY` record and dataset. Check failed requests, missing seed pages and truncation. Do not connect partial output to your downstream step. |
| A page has little or no useful text | Confirm the public HTML contains the content. This Actor does not render JavaScript or sign in. |
| A chunk exceeds the target | Inspect its `oversized` flag and content. Code blocks and tables can stay intact across the target. |

## Validation record

Reference runtime: official n8n `2.41.6`, released 2 October 2026; Docker image `docker.n8n.io/n8nio/n8n:2.41.6`. [Official release](https://github.com/n8n-io/n8n/releases/tag/n8n%402.41.6). This is a reproducible verification target, not a recommendation to skip future security updates.

Eleven offline checks verify configuration without browser globals, URL shape validation, output transformation, polling failures, failed runs, coverage failures, malformed/duplicate chunks, and oversized-chunk preservation. They use the included real sample and make no network calls.

**n8n engine execution passed on 2 October 2026 at 13:48 UTC.** The workflow was imported into an isolated official n8n 2.41.6 Docker container, connected to a private Header Auth credential, and executed through the CLI against the two supplied Mako URLs. The engine exited successfully after **Source packets**, returning two pages and 33 packets, with no oversized chunks and a successful coverage report. The public export contains no credential reference. [Machine-readable verification record and tested workflow SHA-256](../examples/n8n-verification.json).

The engine run used the $0.10 ceiling, 180-second timeout and 512 MB allocation shown above. It was separate from the original saved sample captured at 13:28 UTC. Both observations returned 33 chunks; live page content can change. n8n Cloud UI, paying-customer billing and third-party downstream integrations were not tested.
