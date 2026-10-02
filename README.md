# Mako APIs on Apify

Practical web data tools for GTM research and automation. Built by Valdeir Lima and published as [agency-shift on Apify](https://apify.com/agency-shift).

## Start with website research

**Turn public website pages into clean Markdown and source-linked material for an AI or account-research workflow.**

- [Inspect real output without signing up](https://makorev.com/apis/website-research): switch between Markdown, JSON and source chunks.
- [Download the n8n workflow and setup guide](examples/website-research/README.md).
- [Use the optional AI skill recipe](skills/mako-website-research/SKILL.md) with an existing Apify MCP connection.
- [Open the Web Content Crawler](https://apify.com/agency-shift/web-content-crawler) in your own Apify account.

The saved sample from **2 October 2026** contains two Mako-owned public pages and 33 source chunks, with no failed requests or truncated Markdown. It is a dated, bounded test—not a promise of complete website coverage. The crawler reads static HTML; it does not render JavaScript, create embeddings or generate AI answers. [Inspect the input, output and coverage report](examples/website-research/examples/proof-metadata.json).

The n8n starter runs manually, uses built-in nodes, retrieves both the dataset and crawl report, and checks for missing or truncated content before preparing source packets. It contains no credentials. Your own runs have Apify charges; the sample downloads are free.

## Google Ads monitoring example — availability under review

The [Google Ads monitoring starter](examples/google-ads-monitoring/README.md) includes Python and MCP instructions plus a real earlier 13-record baseline and zero-change repeat. A later live Python run on build 0.2.3 failed with `REDIRECT_REJECTED`; a subsequent bounded test on 0.2.2 succeeded. The cause is unresolved, so these results do not establish consistent availability or a build regression. Always inspect `SUMMARY` before using the output. [Read the dated test notice](https://makorev.com/blog/google-ads-competitor-tracking).

## More research tools

Start with the website-research example above. The catalog below links to each Actor's current inputs, pricing and limitations.

## 🎯 GTM & lead signals

| Actor | What it returns |
|---|---|
| [Find Newly Funded Companies + Decision Makers](https://apify.com/agency-shift/funding-signal-scraper) | Newly-funded US private companies from SEC Form D: company, amount raised, decision makers |
| [Track New Product Hunt Launches + Makers](https://apify.com/agency-shift/ph-launch-tracker) | Fresh PH launches as a GTM lead feed: products, makers, topics, upvotes |
| [ATS Jobs Scraper](https://apify.com/agency-shift/ats-jobs-scraper) | Job postings from Greenhouse, Lever, Ashby, Recruitee — hiring research |
| [Enrich Domains: Email Provider, DMARC & Tech Stack](https://apify.com/agency-shift/domain-intel-scraper) | Email provider (MX), SPF/DMARC posture, tech stack per company domain |
| [Company Registry Scraper (GLEIF / LEI)](https://apify.com/agency-shift/company-registry-lei-scraper) | EU & global legal entities: names, addresses, registry data |
| [SEC EDGAR Filings Scraper](https://apify.com/agency-shift/sec-edgar-filings-scraper) | 10-K, 8-K, Form 4 filings — insider trades and financial events |
| [Hacker News Jobs & Ask HN Scraper](https://apify.com/agency-shift/hackernews-jobs-ask-scraper) | Who-is-hiring threads, job posts, hiring trends |
| [Apple Podcasts Scraper](https://apify.com/agency-shift/apple-podcasts-scraper) | Podcast search, episodes and contact info — podcast outreach at scale |

## 📈 Demand & keyword intelligence

| Actor | What it returns |
|---|---|
| [Google Trends Scout](https://apify.com/agency-shift/google-trends-scout) | Search demand shifts and interest over time |
| [Keyword Ideas Scout](https://apify.com/agency-shift/keyword-ideas-scout) | Autocomplete expansion, related searches, People-Also-Ask |
| [SERP Search Scout](https://apify.com/agency-shift/serp-search-scout) | Who ranks, competitor density, featured snippets |
| [Amazon Autocomplete Keywords](https://apify.com/agency-shift/amazon-autocomplete-keywords) | What customers actually type into Amazon |
| [YouTube Search Scout](https://apify.com/agency-shift/youtube-search-scout) | Video metadata and engagement as demand signals |

## 📱 App-store & builder intelligence

| Actor | What it returns |
|---|---|
| [App Store Localization Gaps](https://apify.com/agency-shift/appstore-localization-gaps) | Apps not localized for specific markets — geo-arbitrage finder |
| [App Store Top Charts](https://apify.com/agency-shift/appstore-top-charts) | Rankings by country and category, new entrants |
| [Indie Launch Radar — Show HN Scanner](https://apify.com/agency-shift/indie-launch-radar-show-hn-early-traction-scanner) | Early-traction signals on Show HN launches |
| [npm & PyPI Package Tracker](https://apify.com/agency-shift/npm-pypi-package-tracker) | Package metadata, download stats, version history |

## 🔧 Utility

| Actor | What it returns |
|---|---|
| [Web Content Crawler](https://apify.com/agency-shift/web-content-crawler) | Structured text and links from supported public web pages |

## Costs, support and feedback

Use your own Apify account and API token. Never put a token in a public repository, issue or shared connection URL. Each Actor documents its own pricing, dependencies and coverage; source websites and available fields can change.

For a collection problem, use the relevant Actor's Issues tab. For the starter examples here, [open a reproducible issue](https://github.com/valdeircs/scraper-fleet/issues/new/choose). Tell us what you expected, what happened, and which decision the output helped you make. Remove credentials and personal data before sharing examples.

Built by **Valdeir Lima · Mako**, GTM and Automation Engineer in Ireland. [Mako website](https://makorev.com) · [Apify tools](https://apify.com/agency-shift) · [Discuss a workflow](https://cal.com/mako-gtm/15min)
