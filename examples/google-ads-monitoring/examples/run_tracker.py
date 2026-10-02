#!/usr/bin/env python3
"""Run one bounded Mako Google Ads observation and save dataset + coverage.

Python 3.9+; standard library only. Requires APIFY_TOKEN in the environment.
No retries of paid run creation. Local tests make no network requests.
"""

import argparse
import json
import math
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://api.apify.com/v2"
ACTOR = "agency-shift~google-ads-competitor-tracker"
TERMINAL = {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}


class ApiError(RuntimeError):
    pass


class Client:
    def __init__(self, token):
        if not token or any(c.isspace() for c in token):
            raise ValueError("Set APIFY_TOKEN to your Apify API token without whitespace.")
        self.token = token

    def request(self, method, path, params=None, body=None):
        url = BASE_URL + path
        if params:
            url += "?" + urlencode(params)
        request = Request(
            url,
            data=None if body is None else json.dumps(body).encode("utf-8"),
            method=method,
            headers={"Authorization": "Bearer " + self.token,
                     "Content-Type": "application/json", "Accept": "application/json"},
        )
        try:
            with urlopen(request, timeout=45) as response:
                return json.load(response)
        except HTTPError as error:
            # Do not echo headers, response bodies, tokens, or remote error text.
            raise ApiError(f"Apify returned HTTP {error.code}; inspect Apify Console.") from None
        except (URLError, TimeoutError, OSError):
            raise ApiError("Apify request failed or timed out; inspect Apify Console before retrying.") from None
        except (ValueError, UnicodeError):
            raise ApiError("Apify returned an unreadable response; inspect Apify Console.") from None


def run_tracker(client, actor_input, max_usd=0.05, timeout=180, *, sleep=time.sleep,
                clock=time.monotonic):
    """Create once, poll, and fetch results. Abort best-effort after a polling error."""
    if not math.isfinite(max_usd) or max_usd < 0.01:
        raise ValueError("--max-usd must be finite and at least 0.01.")
    if not 1 <= timeout <= 3600:
        raise ValueError("--timeout must be between 1 and 3600 seconds.")
    if not isinstance(actor_input, dict):
        raise ValueError("The input JSON must contain an object.")
    max_rows = actor_input.get("maxResults", 1000)
    if type(max_rows) is not int or not 1 <= max_rows <= 10000:
        raise ValueError("Input maxResults must be an integer from 1 to 10000.")
    # Platform limits are query parameters, not Actor input fields.
    try:
        run = client.request("POST", f"/actors/{ACTOR}/runs", {
            "maxTotalChargeUsd": max_usd, "timeout": timeout,
            "waitForFinish": 0, "restartOnError": "false",
        }, actor_input)["data"]
    except (ApiError, KeyError, TypeError):
        raise ApiError("Run creation was not confirmed. Check Apify Console before retrying; a run may already exist.") from None
    run_id = run.get("id")
    if not isinstance(run_id, str) or not run_id:
        raise ApiError("Run ID was missing. Check Apify Console before retrying.")
    run_path = "/actor-runs/" + quote(run_id, safe="")
    deadline = clock() + timeout + 60
    try:
        while run.get("status") not in TERMINAL:
            if clock() >= deadline:
                raise ApiError("Local polling deadline reached; an abort was requested. Check Apify Console.")
            sleep(2)
            run = client.request("GET", run_path)["data"]
    except (ApiError, KeyError, TypeError, KeyboardInterrupt):
        try:
            client.request("POST", run_path + "/abort")
        except (ApiError, KeyError, TypeError):
            pass  # The server-side timeout and budget still apply.
        raise

    items = []
    dataset_id = run.get("defaultDatasetId")
    if dataset_id:
        dataset_path = "/datasets/" + quote(dataset_id, safe="") + "/items"
        while len(items) < max_rows:
            page_size = min(1000, max_rows - len(items))
            page = client.request("GET", dataset_path, {
                "format": "json", "offset": len(items), "limit": page_size,
            })
            if not isinstance(page, list):
                raise ApiError("Expected a dataset array; check Apify Console.")
            items.extend(page)
            if len(page) < page_size:
                break

    summary = None
    store_id = run.get("defaultKeyValueStoreId")
    if store_id:
        summary = client.request("GET", "/key-value-stores/" + quote(store_id, safe="")
                                 + "/records/SUMMARY")
    return {"runStatus": run.get("status"), "records": items, "summary": summary,
            "maxTotalChargeUsd": max_usd, "timeoutSecs": timeout}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--max-usd", type=float, default=0.05,
                        help="Server-side run budget; default 0.05 USD.")
    parser.add_argument("--timeout", type=int, default=180,
                        help="Server-side run timeout in seconds; default 180.")
    parser.add_argument("--output", type=Path, default=Path("results.json"),
                        help="New JSON file for records and SUMMARY; never overwrites.")
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError("Output file exists; choose a new --output name.")
        if not args.output.parent.is_dir():
            raise ValueError("Output directory does not exist; create it before running.")
        actor_input = json.loads(args.input.read_text(encoding="utf-8"))
        result = run_tracker(Client(os.environ.get("APIFY_TOKEN", "")), actor_input,
                             args.max_usd, args.timeout)
        with args.output.open("x", encoding="utf-8") as output:
            json.dump(result, output, ensure_ascii=False, indent=2)
            output.write("\n")
        complete = (result["runStatus"] == "SUCCEEDED"
                    and isinstance(result["summary"], dict)
                    and result["summary"].get("status") == "succeeded")
        print(f"Saved {len(result['records'])} records and coverage to {args.output}.")
        if not complete:
            print("Run or coverage was incomplete. Inspect summary before using these results.", file=sys.stderr)
        return 0 if complete else 2
    except (ApiError, ValueError, OSError, KeyError, TypeError) as error:
        # File and validation errors cannot contain the token; API text is sanitized above.
        print(str(error), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted. Check Apify Console; server-side limits still apply.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
