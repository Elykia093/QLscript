from __future__ import annotations

import unittest
from unittest.mock import patch

import requests

from scripts import tieba


class FakeResponse:
    def __init__(self, payload: object) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> object:
        return self.payload


class FakeSession:
    def __init__(self, payloads: list[object]) -> None:
        self.payloads = iter(payloads)
        self.calls = 0

    def post(self, *_args: object, **_kwargs: object) -> FakeResponse:
        self.calls += 1
        return FakeResponse(next(self.payloads))


class TiebaTests(unittest.TestCase):
    def test_credential_endpoints_require_https(self) -> None:
        for url in (tieba.TBS_URL, tieba.LIKE_URL, tieba.SIGN_URL):
            with self.subTest(url=url):
                self.assertTrue(url.startswith("https://"))

    def test_get_favorites_collects_multiple_pages(self) -> None:
        session = FakeSession(
            [
                {
                    "forum_list": {"non-gconforum": [{"id": "1", "name": "one"}]},
                    "has_more": "1",
                },
                {
                    "forum_list": {"gconforum": [{"id": "2", "name": "two"}]},
                    "has_more": "0",
                },
            ]
        )

        bars = tieba.get_favorites(session, "bduss")

        self.assertEqual([bar["id"] for bar in bars], ["1", "2"])
        self.assertEqual(session.calls, 2)

    def test_get_favorites_stops_when_pagination_makes_no_progress(self) -> None:
        repeated_page = {
            "forum_list": {"non-gconforum": [{"id": "1", "name": "one"}]},
            "has_more": "1",
        }
        session = FakeSession([repeated_page, repeated_page])

        with self.assertRaisesRegex(RuntimeError, "没有新增数据"):
            tieba.get_favorites(session, "bduss")

        self.assertEqual(session.calls, 2)

    def test_get_favorites_rejects_non_object_response(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "响应不是 JSON 对象"):
            tieba.get_favorites(FakeSession([[]]), "bduss")

    def test_request_retry_only_covers_transient_failures(self) -> None:
        self.assertTrue(tieba.is_retryable_request_error(requests.Timeout("timeout")))

        server_error_response = requests.Response()
        server_error_response.status_code = 503
        self.assertTrue(
            tieba.is_retryable_request_error(requests.HTTPError(response=server_error_response))
        )

        client_error_response = requests.Response()
        client_error_response.status_code = 400
        self.assertFalse(
            tieba.is_retryable_request_error(requests.HTTPError(response=client_error_response))
        )

    def test_sign_round_preserves_request_failure_as_retryable_result(self) -> None:
        bar = {"id": "1", "name": "one"}
        with patch("scripts.tieba.sign_bar", side_effect=requests.Timeout("timeout")):
            results = tieba.run_sign_round("bduss", "tbs", [bar], workers=1)

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0]["ok"])
        self.assertTrue(results[0]["retryable"])

    def test_sign_round_isolates_response_failure_without_retry(self) -> None:
        bar = {"id": "1", "name": "one"}
        with patch("scripts.tieba.sign_bar", side_effect=RuntimeError("invalid response")):
            results = tieba.run_sign_round("bduss", "tbs", [bar], workers=1)

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0]["ok"])
        self.assertFalse(results[0]["retryable"])

    def test_run_account_retries_only_transient_failures(self) -> None:
        favorites = [
            {"id": "1", "name": "business-failure"},
            {"id": "2", "name": "transient-failure"},
        ]
        first_round = [
            {
                "id": "1",
                "name": "business-failure",
                "error_code": "999",
                "status": "业务失败",
                "ok": False,
                "retryable": False,
            },
            {
                "id": "2",
                "name": "transient-failure",
                "error_code": "request_error",
                "status": "timeout",
                "ok": False,
                "retryable": True,
            },
        ]
        second_round = [
            {
                "id": "2",
                "name": "transient-failure",
                "error_code": "0",
                "status": "签到成功",
                "ok": True,
                "retryable": False,
            }
        ]

        with patch("scripts.tieba.get_tbs", return_value="tbs"), patch(
            "scripts.tieba.get_favorites", return_value=favorites
        ), patch(
            "scripts.tieba.run_sign_round", side_effect=[first_round, second_round]
        ) as run_sign_round, patch("scripts.tieba.requests.Session") as session_class:
            session_class.return_value.__enter__.return_value = object()
            result = tieba.run_account("BDUSS=1234567890", 1)

        self.assertTrue(result.ok)
        self.assertIn("成功/已签 1/2", result.message)
        self.assertIn("business-failure(业务失败)", result.message)
        self.assertEqual(run_sign_round.call_count, 2)
        self.assertEqual(run_sign_round.call_args_list[1].args[2], [favorites[1]])


if __name__ == "__main__":
    unittest.main()
