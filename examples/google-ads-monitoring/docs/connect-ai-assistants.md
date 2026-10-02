# Connect Mako’s Google Ads tracker to an assistant

Use Apify’s hosted MCP server to expose [Google Ads Competitor Tracker](https://apify.com/agency-shift/google-ads-competitor-tracker) to a compatible assistant. Sign in with **your own Apify account**. Connecting lets that account use the tool; it does not publish a monitor, schedule runs, or guarantee recommendations elsewhere.

## Endpoint and verification status

Use this HTTPS server URL exactly; the `tools` parameter selects the Actor and the generic runner with budget controls:

```text
https://mcp.apify.com?tools=agency-shift/google-ads-competitor-tracker,call-actor
```

Protocol initialization, tool discovery, a bounded repeat run through `call-actor`, dataset retrieval, and SUMMARY retrieval were verified on **2 October 2026**. The Actor-specific tool name was `agency-shift--google-ads-competitor-tracker`; it was discovered but not invoked because its schema does not expose a dollar cap. Claude Code, Claude, and ChatGPT sign-in and execution have **not** been tested end to end in those clients. The instructions below follow their official documentation; account access and interface labels can differ.

Apify’s server supports OAuth and runs eligible Actors on the authenticated user’s account. Full-permission and rental Actors are excluded by its documentation; this Actor was verified with limited permissions and pay-per-event pricing. See [Apify MCP documentation](https://docs.apify.com/integrations/mcp).

## Claude Code

With a current Claude Code installation, run:

```sh
claude mcp add --transport http --scope user mako-google-ads \
  'https://mcp.apify.com?tools=agency-shift/google-ads-competitor-tracker,call-actor'
claude mcp login mako-google-ads
claude mcp get mako-google-ads
```

Complete the browser sign-in to Apify, then confirm the server connects. Within Claude Code, `/mcp` also opens connection and authentication controls. If your CLI does not recognize `mcp login`, use `/mcp` in an interactive session and consult the current [Claude Code MCP guide](https://code.claude.com/docs/en/mcp). If this server name already exists, inspect it with `get` rather than adding it again.

The `--scope user` setting makes this entry available across your local projects. It is not a shared team setup and does not embed an API token in a repository.

## Claude on the web or desktop

For accounts with custom connectors, open **Customize → Connectors → + Add → Add custom connector**. Name it “Mako Google Ads”, enter the endpoint above, and complete the detected OAuth sign-in to your Apify account. Enable the connector in the conversation’s connector controls.

Managed teams may need an owner to add the connector before members connect individually. Follow the current [Claude custom connector instructions](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) for your plan. Use OAuth instead of putting credentials in the URL or a chat message.

## ChatGPT

Where your account and workspace allow developer-mode connections, follow the [official plugin quickstart](https://developers.openai.com/plugins/quickstart): enable Developer mode in **Settings → Security and login**, add a connection from **ChatGPT Plugins**, and enter the exact endpoint above. Complete the Apify OAuth authorization, install the resulting personal plugin, and select it in a Work chat.

Some accounts use different app/connector labels or restrict custom connections. If the controls are unavailable, check workspace permissions and current [OpenAI connection guidance](https://developers.openai.com/plugins/deploy/connect-chatgpt). This guide does not promise access for every ChatGPT plan. Do not append a guessed `/mcp` path to Apify’s documented endpoint.

## First prompt: inspect before running

> Inspect the input schema and pricing for agency-shift/google-ads-competitor-tracker. Prepare one snapshot for advertiser AR10888897372843147265, country JP, all formats, at most 20 output records and 20 observations, with creative details enabled and at most 20 preview requests. Show the exact input and available run-budget controls before starting. Do not run another Actor or create a schedule.

The Actor’s `maxResults` input is a **record limit, not a dollar budget**. The verified endpoint also exposes the generic `call-actor` tool, whose `callOptions` supports both `maxTotalChargeUsd` and `timeout`. Use that tool for a bounded run. The tested repeat used this argument shape:

```json
{
  "actor": "agency-shift/google-ads-competitor-tracker",
  "input": {
    "advertiserIds": ["AR10888897372843147265"],
    "region": "JP",
    "mode": "changes",
    "monitorName": "mako-notion-japan-example-20261002",
    "format": "ALL",
    "maxResults": 20,
    "maxAdsPerDomain": 20,
    "emitInitialSnapshot": true,
    "includeCreativeDetails": true,
    "maxCreativeDetails": 20
  },
  "waitSecs": 30,
  "callOptions": {
    "memory": 256,
    "timeout": 180,
    "build": "0.2.2",
    "maxTotalChargeUsd": 0.05
  }
}
```

Use `get-actor-run` if the call returns a run that is still running, then `get-dataset-items` and `get-key-value-store-record` for `SUMMARY` using that run’s returned storage IDs. These retrieval tools were also verified. The [evidence summary](../examples/evidence-2026-10-02.json) records what the repeat actually returned.

A natural-language request to “spend no more than $0.05” does not by itself enforce that cap: inspect the actual arguments. If your client does not expose `call-actor` and its run options, create the bounded run in Apify Console or use the [Python/API starter](google-ads-monitoring.md). You can give the assistant the saved JSON to analyze.

## Prompt for a completed run

> Review these Google Ads observations and their SUMMARY. Begin with coverage: fresh scans, limits, errors, and targets not scanned. Group observed creatives by advertiser and event type. Cite creativeUrl and observedAt for each example. For changed records, show changedFields with before and after values. Treat null as unavailable. Do not infer spend, performance, campaign launches, stopped ads, or exhaustive coverage. Deduplicate by eventId.

For the second run, use the same Changes monitor name, target, country, format, and detail settings described in [the monitoring guide](google-ads-monitoring.md). Connecting an assistant alone does not create or preserve a baseline; the Actor’s Changes run does.

## Authentication and cost

OAuth grants the assistant access through your Apify account. Review the consent screen. Apify charges for runs according to the Actor’s current pricing and your account; an assistant subscription does not include those charges. Output can be empty while a startup fee still applies.

For direct API examples, keep `APIFY_TOKEN` in your environment or secret manager. Never add a token to the MCP URL, code, public issue, screenshot, or prompt. Removing a client connection and revoking its authorization are account-specific actions; use that client’s connection controls and Apify’s account settings when access is no longer needed.
