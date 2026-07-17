from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from scripts import mihoyo


class MihoyoTests(unittest.TestCase):
    def test_parse_sign_response_accepts_only_explicit_success_code(self) -> None:
        self.assertEqual(mihoyo.parse_sign_response({"retcode": 0, "message": "OK"}), "OK")
        self.assertEqual(mihoyo.parse_sign_response({"retcode": "0", "message": "已签到"}), "已签到")

    def test_parse_sign_response_rejects_ambiguous_success_text(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "业务码 999"):
            mihoyo.parse_sign_response({"retcode": 999, "message": "签到不成功"})

    def test_parse_sign_response_classifies_known_failures(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "触发验证码"):
            mihoyo.parse_sign_response({"retcode": 1034, "message": "risk"})
        with self.assertRaisesRegex(RuntimeError, "Cookie 失效"):
            mihoyo.parse_sign_response({"retcode": -100, "message": "expired"})
        with self.assertRaisesRegex(RuntimeError, "不是 JSON 对象"):
            mihoyo.parse_sign_response([])
        with self.assertRaisesRegex(RuntimeError, "retcode 格式无效"):
            mihoyo.parse_sign_response({"retcode": False, "message": "OK"})
        with self.assertRaisesRegex(RuntimeError, "retcode 格式无效"):
            mihoyo.parse_sign_response({"retcode": {}, "message": "OK"})

    def test_run_account_keeps_successes_when_one_forum_fails(self) -> None:
        session_context = MagicMock()
        session_context.__enter__.return_value = object()
        with patch("scripts.mihoyo.selected_gids", return_value=["2", "6"]), patch(
            "scripts.mihoyo.requests.Session", return_value=session_context
        ), patch(
            "scripts.mihoyo.sign_forum",
            side_effect=["原神: OK", RuntimeError("触发验证码")],
        ) as sign_forum, patch("scripts.mihoyo.time.sleep"):
            result = mihoyo.run_account("account_id=1234567890", 1)

        self.assertTrue(result.ok)
        self.assertIn("成功/已签 1/2", result.message)
        self.assertIn("原神: OK", result.message)
        self.assertIn("崩坏：星穹铁道: 失败 - 触发验证码", result.message)
        self.assertEqual(sign_forum.call_count, 2)

    def test_run_account_fails_only_after_all_forums_fail(self) -> None:
        session_context = MagicMock()
        session_context.__enter__.return_value = object()
        with patch("scripts.mihoyo.selected_gids", return_value=["2", "6"]), patch(
            "scripts.mihoyo.requests.Session", return_value=session_context
        ), patch(
            "scripts.mihoyo.sign_forum",
            side_effect=[RuntimeError("first"), RuntimeError("second")],
        ), patch("scripts.mihoyo.time.sleep"):
            result = mihoyo.run_account("account_id=1234567890", 1)

        self.assertFalse(result.ok)
        self.assertIn("成功/已签 0/2", result.message)


if __name__ == "__main__":
    unittest.main()
