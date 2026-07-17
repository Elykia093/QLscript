from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from utils.ql_common import (
    AccountResult,
    cookie_name,
    error_message,
    format_results,
    mask_secret,
    run_accounts,
    split_accounts,
)


class QlCommonTests(unittest.TestCase):
    def test_split_accounts_supports_documented_separators(self) -> None:
        self.assertEqual(split_accounts("one\r\ntwo"), ["one", "two"])
        self.assertEqual(split_accounts("one&two"), ["one", "two"])
        self.assertEqual(split_accounts("one#two"), ["one", "two"])
        self.assertEqual(split_accounts("  "), [])

    def test_sensitive_values_are_masked(self) -> None:
        self.assertEqual(mask_secret("1234567890"), "1234***7890")
        self.assertEqual(cookie_name("BDUSS=1234567890; foo=bar", 1), "BDUSS=1234***7890")
        self.assertEqual(
            error_message(Exception("GET https://example.test?a=secret&b=value")),
            "GET https://example.test?a=***&b=***",
        )

    def test_format_results_preserves_success_and_failure(self) -> None:
        content = format_results(
            [
                AccountResult(1, True, "first", "done"),
                AccountResult(2, False, "second", "failed"),
            ]
        )
        self.assertIn("成功 | 账号1 | first: done", content)
        self.assertIn("失败 | 账号2 | second: failed", content)

    def test_run_accounts_isolates_accounts_and_reports_partial_success(self) -> None:
        def runner(account: str, account_index: int) -> AccountResult:
            if account == "bad":
                raise RuntimeError("request failed")
            return AccountResult(account_index, True, account, "done")

        with patch.dict(os.environ, {"TEST_ACCOUNTS": "good\nbad"}, clear=False), patch(
            "utils.ql_common.send_notify"
        ) as send_notify:
            exit_code = run_accounts("test", "TEST_ACCOUNTS", runner)

        self.assertEqual(exit_code, 0)
        content = send_notify.call_args.args[1]
        self.assertIn("成功 | 账号1", content)
        self.assertIn("失败 | 账号2", content)

    def test_run_accounts_returns_nonzero_when_all_accounts_fail(self) -> None:
        def runner(_account: str, _account_index: int) -> AccountResult:
            raise RuntimeError("failed")

        with patch.dict(os.environ, {"TEST_ACCOUNTS": "one\ntwo"}, clear=False), patch(
            "utils.ql_common.send_notify"
        ):
            exit_code = run_accounts("test", "TEST_ACCOUNTS", runner)

        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
