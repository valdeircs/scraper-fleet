"""Contract checks for the starter; every API call is mocked and free."""

import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

SOURCE = Path(__file__).resolve().parents[1] / "examples" / "run_tracker.py"
SPEC = importlib.util.spec_from_file_location("run_tracker", SOURCE)
tracker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tracker)


class FakeClient:
    def __init__(self, replies):
        self.replies = iter(replies)
        self.calls = []

    def request(self, method, path, params=None, body=None):
        self.calls.append((method, path, params, body))
        reply = next(self.replies)
        if isinstance(reply, BaseException):
            raise reply
        return reply


def run(status="SUCCEEDED"):
    return {"data": {"id": "mock-run", "status": status,
                     "defaultDatasetId": "mock-dataset",
                     "defaultKeyValueStoreId": "mock-store"}}


class StarterTests(unittest.TestCase):
    def test_limits_and_input_are_sent_separately_then_summary_is_fetched(self):
        data = {"advertiserIds": ["mock-advertiser"], "maxResults": 20}
        client = FakeClient([run(), [{"eventType": "initial"}], {"status": "succeeded"}])
        result = tracker.run_tracker(client, data, 0.05, 120)
        method, path, query, body = client.calls[0]
        self.assertEqual(method, "POST")
        self.assertIn("/actors/agency-shift~google-ads-competitor-tracker/runs", path)
        self.assertEqual(query["maxTotalChargeUsd"], 0.05)
        self.assertEqual(query["timeout"], 120)
        self.assertEqual(query["restartOnError"], "false")
        self.assertIs(body, data)
        self.assertEqual(result["summary"]["status"], "succeeded")
        self.assertTrue(client.calls[-1][1].endswith("/records/SUMMARY"))

    def test_dataset_paginates_without_hiding_rows(self):
        client = FakeClient([run(), [{"n": n} for n in range(1000)], [{"n": 1000}],
                             {"status": "succeeded"}])
        result = tracker.run_tracker(client, {"maxResults": 1500})
        self.assertEqual(len(result["records"]), 1001)
        self.assertEqual(client.calls[2][2]["offset"], 1000)
        self.assertEqual(client.calls[2][2]["limit"], 500)

    def test_start_failure_is_not_retried(self):
        client = FakeClient([tracker.ApiError("unconfirmed")])
        with self.assertRaisesRegex(tracker.ApiError, "may already exist"):
            tracker.run_tracker(client, {})
        self.assertEqual(len(client.calls), 1)

    def test_poll_error_attempts_abort_without_restarting(self):
        client = FakeClient([run("RUNNING"), tracker.ApiError("poll failed"), run("ABORTED")])
        with self.assertRaisesRegex(tracker.ApiError, "poll failed"):
            tracker.run_tracker(client, {}, sleep=lambda _: None)
        self.assertEqual(client.calls[-1][:2], ("POST", "/actor-runs/mock-run/abort"))
        self.assertEqual(sum("/actors/" in c[1] for c in client.calls), 1)

    def test_local_deadline_requests_abort(self):
        ticks = iter([0, 182])
        client = FakeClient([run("RUNNING"), run("ABORTED")])
        with self.assertRaisesRegex(tracker.ApiError, "deadline"):
            tracker.run_tracker(client, {}, timeout=120, clock=lambda: next(ticks))
        self.assertTrue(client.calls[-1][1].endswith("/abort"))

    def test_failed_run_preserves_status_and_partial_evidence(self):
        client = FakeClient([run("FAILED"), [], {"status": "failed"}])
        result = tracker.run_tracker(client, {})
        self.assertEqual(result["runStatus"], "FAILED")
        self.assertEqual(result["summary"]["status"], "failed")

    def test_invalid_budgets_are_rejected_before_network(self):
        for budget in (0, -1, 0.001, float("nan"), float("inf")):
            client = FakeClient([])
            with self.assertRaises(ValueError):
                tracker.run_tracker(client, {}, max_usd=budget)
            self.assertEqual(client.calls, [])

    def test_credentials_use_headers_and_http_errors_do_not_echo_remote_data(self):
        client = tracker.Client("not-a-real-secret")
        error = HTTPError("https://api.apify.com", 401, "not-a-real-secret", {},
                          io.BytesIO(b'not-a-real-secret'))
        with patch.object(tracker, "urlopen", side_effect=error) as opener:
            with self.assertRaises(tracker.ApiError) as result:
                client.request("GET", "/actor-runs/mock-run")
            request = opener.call_args.args[0]
            self.assertEqual(request.get_header("Authorization"), "Bearer not-a-real-secret")
            self.assertNotIn("not-a-real-secret", request.full_url)
            self.assertNotIn("not-a-real-secret", str(result.exception))


if __name__ == "__main__":
    unittest.main()
