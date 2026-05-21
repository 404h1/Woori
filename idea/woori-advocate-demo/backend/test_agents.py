import unittest
from unittest.mock import patch

from agents import _seller_rebuttal, run_seller
from providers import LLMCallResult, LLMProvider, report_provider_status


class _FakeProvider:
    def __init__(self, name: str) -> None:
        self.name = name

    async def call(self, system: str, user: str) -> LLMCallResult:
        return LLMCallResult(
            text=f"{self.name} seller response",
            backend=f"{self.name}-cli",
            model_hint=self.name,
        )


class _FailingCliProvider(LLMProvider):
    name = "failing"
    cli_binary = "python"

    async def _call_api(self, api_key: str, system: str, user: str) -> LLMCallResult:
        raise AssertionError("API should not be called without an API key")

    async def _call_cli(self, system: str, user: str) -> LLMCallResult:
        return LLMCallResult(
            text="",
            backend="mock",
            model_hint="claude-cli-rc1",
            error="authentication failed",
        )


class SellerProviderSelectionTest(unittest.IsolatedAsyncioTestCase):
    async def test_run_seller_uses_anthropic_provider(self) -> None:
        requested: list[str] = []

        def fake_get_provider(name: str) -> _FakeProvider:
            requested.append(name)
            return _FakeProvider(name)

        product = {
            "name": "ELS",
            "category": "ELS",
            "tenor_months": 36,
            "max_coupon_pct_annual": 6.0,
            "knock_in_pct": 50,
            "early_redemption_schedule": ["6m"],
        }

        with patch("agents.get_provider", side_effect=fake_get_provider):
            result = await run_seller(product)

        self.assertEqual(requested, ["anthropic"])
        self.assertEqual(result.backend, "anthropic-cli")

    async def test_seller_rebuttal_uses_anthropic_provider(self) -> None:
        requested: list[str] = []

        def fake_get_provider(name: str) -> _FakeProvider:
            requested.append(name)
            return _FakeProvider(name)

        with patch("agents.get_provider", side_effect=fake_get_provider):
            result = await _seller_rebuttal(
                product={},
                prev_seller="seller point",
                prev_advocate_items=[
                    {"no": 1, "title": "risk", "source": "T-001"}
                ],
            )

        self.assertEqual(requested, ["anthropic"])
        self.assertEqual(result.backend, "anthropic-cli")


class ProviderStatusTest(unittest.TestCase):
    def test_provider_status_reports_active_demo_providers_only(self) -> None:
        status = report_provider_status()

        self.assertIn("anthropic", status)
        self.assertIn("openai", status)
        self.assertNotIn("gemini", status)


class ProviderFallbackTest(unittest.IsolatedAsyncioTestCase):
    async def test_call_preserves_cli_failure_reason(self) -> None:
        result = await _FailingCliProvider().call("system", "user")

        self.assertEqual(result.model_hint, "claude-cli-rc1")
        self.assertEqual(result.error, "authentication failed")

    async def test_anthropic_cli_failure_includes_stdout_when_stderr_is_empty(self) -> None:
        from providers import AnthropicProvider

        captured_args: tuple[str, ...] = ()

        class _Process:
            returncode = 1

            async def communicate(self) -> tuple[bytes, bytes]:
                return b"Failed to authenticate", b""

        async def fake_exec(*args, **kwargs) -> _Process:
            nonlocal captured_args
            captured_args = args
            return _Process()

        with patch("providers.shutil.which", return_value="claude"), patch(
            "providers.asyncio.create_subprocess_exec", side_effect=fake_exec
        ):
            result = await AnthropicProvider()._call_cli("system", "user")

        self.assertEqual(result.model_hint, "claude-cli-rc1")
        self.assertIn("Failed to authenticate", result.error)
        self.assertIn("--permission-mode", captured_args)
        self.assertIn("dontAsk", captured_args)
        self.assertIn("--tools", captured_args)
        self.assertIn("", captured_args)


if __name__ == "__main__":
    unittest.main()
