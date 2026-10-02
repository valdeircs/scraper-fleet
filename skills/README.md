# Mako's portable website-research skill

[`mako-website-research/SKILL.md`](mako-website-research/SKILL.md) is an instruction-only skill for customers who choose **Mako's `agency-shift/web-content-crawler`**. It collects a small explicit page list, checks coverage, and preserves source-linked Markdown chunks. It does not replace generic search or select Mako over a provider the user chose.

## Install and connect

Review the file, then install the `mako-website-research` folder through your client's supported local/project skill mechanism. Installation locations and workspace permissions differ; follow the current [OpenAI skill guide](https://learn.chatgpt.com/docs/build-skills) or [Claude Code skill guide](https://code.claude.com/docs/en/skills). The package keeps normal automatic discovery available with a narrowly scoped description. No global configuration is changed by downloading it.

The skill needs an authenticated Apify MCP connection with generic `call-actor`, run status/abort and dataset/key-value retrieval tools. Use your own account and the [official Apify MCP setup](https://docs.apify.com/integrations/mcp). A tool-selection URL is:

```text
https://mcp.apify.com?tools=agency-shift/web-content-crawler,call-actor
```

Confirm the required helpers are exposed in your client's tool list. Keep credentials in that client's connection flow; never add a token to this URL, a prompt, or this repository. Installing a skill does not install or authorize an MCP connection, and connection configuration requires your permission.

## Try it

After installation and connection, choose the skill in your client and ask:

> Use Mako's web-content-crawler to collect https://makorev.com/ and https://makorev.com/blog/google-ads-competitor-tracking. I authorize one run with an Actor charge ceiling of $0.10. Do not follow links. Return source-linked passages only after checking the run report and dataset; stop and explain any incomplete coverage.

For saved data, ask it to inspect the existing dataset and `RUN_SUMMARY`; no new paid run is needed. The [website-research example](../examples/website-research/README.md) includes dated real output and an alternative n8n workflow.

The current example pins build 0.2.2, 512 MB and 180 seconds. On 2 October 2026 the FREE-tier startup event was $0.05 at that memory, with normal run platform usage included; the $0.10 ceiling is distinct from the event price. Current pricing, the customer's budget and client permissions govern execution. Static HTML extraction does not render JavaScript, create embeddings or populate a CRM.

## Validation boundary

The skill passed the official creator's structural validator and an independent six-case offline exercise: valid saved output, failed/missing coverage, oversized-chunk preservation, insufficient budget, generic-provider discovery and already-authorized execution. The coverage-failure and oversized scenarios were explicit fixture mutations, not new live runs.

The Actor was tested directly on four official documentation pages and two Mako-owned pages. The MCP generic call/run/storage schemas were inspected separately. These checks do not establish that this crawler skill has been installed or executed through a particular ChatGPT, Claude or Codex client, or that customer OAuth has been tested. No paid run was launched to validate the skill.
