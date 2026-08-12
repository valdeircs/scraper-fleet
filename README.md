# scraper-fleet

**18 production data actors on the [Apify Store](https://apify.com/agency-shift)** — lead signals, market intelligence, app-store data and demand research. Built and maintained by me, running under the `agency-shift` account, feeding my own outbound engine daily.

The thesis: **own the data pipe instead of renting seats.** Data vendors charge per credit forever; a scraper you own costs cents per run and nobody can deprecate your column.

## 🎯 GTM & lead signals

| Actor | What it returns |
|---|---|
| [Find Newly Funded Companies + Decision Makers](https://apify.com/agency-shift/funding-signal-scraper) | Newly-funded US private companies from SEC Form D: company, amount raised, decision makers |
| [Track New Product Hunt Launches + Makers](https://apify.com/agency-shift/ph-launch-tracker) | Fresh PH launches as a GTM lead feed: products, makers, topics, upvotes |
| [ATS Jobs Scraper](https://apify.com/agency-shift/ats-jobs-scraper) | Job postings from Greenhouse, Lever, Ashby, Recruitee — hiring = buying signal |
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
| [Web Content Crawler](https://apify.com/agency-shift/web-content-crawler) | Clean text extraction from any URL |

## How I use them

Each actor is one input node of my outbound engine: **source → enrich → qualify → message**, orchestrated with n8n, stored in Supabase, personalized with Claude. A recent pay-per-event run sourced ~100 qualified B2B leads for about $0.27.

---

Built by [Valdeir Lima](https://www.linkedin.com/in/valdeir-lima/) — GTM & Automation Engineer, Ireland. [agencyshift.dev](https://agencyshift.dev) · [Book 15 min](https://cal.com/valdeir-lima-yfs2lk/15min)
