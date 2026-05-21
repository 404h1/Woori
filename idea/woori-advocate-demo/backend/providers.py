"""
LLM Provider 추상화 — OpenClaw/ZeroClaw 스타일 다중 인증 패턴 참고.

각 provider 는 3단 폴백:
  1) API key (환경변수)   — REST 직접 호출, 가장 안정
  2) CLI OAuth            — claude / codex 바이너리 subprocess
  3) Mock fallback        — 시연 안정성

레퍼런스:
- Anthropic Messages API: https://api.anthropic.com/v1/messages
- OpenAI Chat API:    https://api.openai.com/v1/chat/completions
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx


# ──────────────────────────────────────────────────────────────────────────
# Common types
# ──────────────────────────────────────────────────────────────────────────

@dataclass
class LLMCallResult:
    text: str
    backend: str  # e.g. "anthropic-api" | "claude-cli" | "openai-api" | "codex-cli" | "mock"
    model_hint: str = ""
    error: str = ""
    latency_ms: int = 0


def _sandbox_cwd() -> str:
    """CLI 자식 프로세스가 현재 프로젝트 컨텍스트를 읽지 않도록 빈 디렉토리."""
    p = Path(tempfile.gettempdir()) / "woori_llm_sandbox"
    p.mkdir(parents=True, exist_ok=True)
    return str(p)


# ──────────────────────────────────────────────────────────────────────────
# Abstract Provider
# ──────────────────────────────────────────────────────────────────────────

class LLMProvider(ABC):
    """Provider = LLM 한 종류 + 다중 인증 폴백."""

    name: str = "abstract"
    api_key_env_vars: tuple[str, ...] = ()
    cli_binary: str = ""
    model: str = ""

    def __init__(self, model: str | None = None) -> None:
        if model:
            self.model = model

    # ── public ─────────────────────────────────────────────────────────

    async def call(self, system: str, user: str) -> LLMCallResult:
        """3단 폴백: API key → CLI → mock."""
        last_failure: LLMCallResult | None = None
        # 1. API key 시도
        for env in self.api_key_env_vars:
            key = os.environ.get(env)
            if key:
                result = await self._call_api(key, system, user)
                if result.text:
                    return result
                last_failure = result
                # API 실패 시 다음 단계로
        # 2. CLI 시도
        if self.cli_binary and shutil.which(self.cli_binary):
            result = await self._call_cli(system, user)
            if result.text:
                return result
            last_failure = result
        # 3. Mock
        if last_failure is not None:
            return last_failure
        return LLMCallResult(
            text="", backend="mock",
            model_hint=f"{self.name}-disabled",
            error="no API key + no CLI",
        )

    # ── subclass hooks ─────────────────────────────────────────────────

    @abstractmethod
    async def _call_api(self, api_key: str, system: str, user: str) -> LLMCallResult:
        ...

    @abstractmethod
    async def _call_cli(self, system: str, user: str) -> LLMCallResult:
        ...


# ──────────────────────────────────────────────────────────────────────────
# OpenAI Provider
# ──────────────────────────────────────────────────────────────────────────

class OpenAIProvider(LLMProvider):
    name = "openai"
    api_key_env_vars = ("OPENAI_API_KEY",)
    cli_binary = "codex"
    model = "gpt-4o-mini"

    async def _call_api(self, api_key: str, system: str, user: str) -> LLMCallResult:
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.3,
            "max_tokens": 1024,
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code != 200:
                return LLMCallResult(
                    text="", backend="mock", model_hint=f"openai-api-{resp.status_code}",
                    error=f"openai API HTTP {resp.status_code}: {resp.text[:200]}",
                )
            data = resp.json()
            choices = data.get("choices", [])
            if not choices:
                return LLMCallResult(
                    text="", backend="mock", model_hint="openai-api-empty",
                    error=f"no choices: {data}",
                )
            text = (choices[0].get("message", {}).get("content") or "").strip()
            if not text:
                return LLMCallResult(text="", backend="mock", model_hint="openai-api-empty", error="empty")
            return LLMCallResult(text=text, backend="openai-api", model_hint=self.model)
        except Exception as exc:  # noqa: BLE001
            return LLMCallResult(
                text="", backend="mock", model_hint="openai-api-error",
                error=f"openai API exception: {exc}",
            )

    async def _call_cli(self, system: str, user: str) -> LLMCallResult:
        resolved = shutil.which(self.cli_binary)
        if not resolved:
            return LLMCallResult(text="", backend="mock", model_hint="codex-cli-missing", error="not found")
        combined = f"[SYSTEM]\n{system}\n\n[USER]\n{user}\n"
        use_shell = os.name == "nt" and resolved.lower().endswith((".cmd", ".bat"))
        sandbox = _sandbox_cwd()
        try:
            if use_shell:
                escaped = combined.replace('"', '""')
                cmdline = f'"{resolved}" exec --skip-git-repo-check "{escaped}"'
                proc = await asyncio.create_subprocess_shell(
                    cmdline, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                    cwd=sandbox,
                )
            else:
                proc = await asyncio.create_subprocess_exec(
                    resolved, "exec", "--skip-git-repo-check", combined,
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                    cwd=sandbox,
                )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=90.0)
        except asyncio.TimeoutError:
            return LLMCallResult(text="", backend="mock", model_hint="codex-cli-timeout", error="timeout 90s")
        except Exception as exc:  # noqa: BLE001
            return LLMCallResult(text="", backend="mock", model_hint="codex-cli-error", error=str(exc))
        if proc.returncode != 0:
            err = stderr.decode(errors="ignore").strip()
            if not err:
                err = stdout.decode(errors="ignore").strip()
            return LLMCallResult(
                text="", backend="mock", model_hint=f"codex-cli-rc{proc.returncode}",
                error=err[:300],
            )
        text = stdout.decode(errors="ignore").strip()
        if not text:
            return LLMCallResult(text="", backend="mock", model_hint="codex-cli-empty", error="empty")
        return LLMCallResult(text=text, backend="codex-cli", model_hint="gpt-default")


# ──────────────────────────────────────────────────────────────────────────
# Anthropic Provider (Claude)
# ──────────────────────────────────────────────────────────────────────────

class AnthropicProvider(LLMProvider):
    name = "anthropic"
    api_key_env_vars = ("ANTHROPIC_API_KEY",)
    cli_binary = "claude"
    model = "claude-sonnet-4-5"
    api_version = "2023-06-01"

    async def _call_api(self, api_key: str, system: str, user: str) -> LLMCallResult:
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "temperature": 0.4,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
        headers = {
            "x-api-key": api_key,
            "anthropic-version": self.api_version,
            "content-type": "application/json",
        }
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code != 200:
                return LLMCallResult(
                    text="", backend="mock", model_hint=f"anthropic-api-{resp.status_code}",
                    error=f"anthropic API HTTP {resp.status_code}: {resp.text[:200]}",
                )
            data = resp.json()
            blocks = data.get("content", [])
            text = "".join(b.get("text", "") for b in blocks if b.get("type") == "text").strip()
            if not text:
                return LLMCallResult(text="", backend="mock", model_hint="anthropic-api-empty", error="empty content")
            return LLMCallResult(text=text, backend="anthropic-api", model_hint=self.model)
        except Exception as exc:  # noqa: BLE001
            return LLMCallResult(
                text="", backend="mock", model_hint="anthropic-api-error",
                error=f"anthropic API exception: {exc}",
            )

    async def _call_cli(self, system: str, user: str) -> LLMCallResult:
        resolved = shutil.which(self.cli_binary)
        if not resolved:
            return LLMCallResult(text="", backend="mock", model_hint="claude-cli-missing", error="not found")
        use_shell = os.name == "nt" and resolved.lower().endswith((".cmd", ".bat"))
        sandbox = _sandbox_cwd()
        # claude CLI: -p (print/non-interactive) + --system-prompt + tools disabled.
        try:
            if use_shell:
                esc_sys = system.replace('"', '""')
                esc_user = user.replace('"', '""')
                cmdline = (
                    f'"{resolved}" -p "{esc_user}" '
                    f'--system-prompt "{esc_sys}" '
                    f'--permission-mode dontAsk --output-format text '
                    f'--tools ""'
                )
                proc = await asyncio.create_subprocess_shell(
                    cmdline, stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE, cwd=sandbox,
                )
            else:
                proc = await asyncio.create_subprocess_exec(
                    resolved, "-p", user,
                    "--system-prompt", system,
                    "--permission-mode", "dontAsk",
                    "--output-format", "text",
                    "--tools", "",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=sandbox,
                )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120.0)
        except asyncio.TimeoutError:
            return LLMCallResult(text="", backend="mock", model_hint="claude-cli-timeout", error="timeout 120s")
        except Exception as exc:  # noqa: BLE001
            return LLMCallResult(text="", backend="mock", model_hint="claude-cli-error", error=str(exc))
        if proc.returncode != 0:
            err = stderr.decode(errors="ignore").strip()
            if not err:
                err = stdout.decode(errors="ignore").strip()
            return LLMCallResult(
                text="", backend="mock", model_hint=f"claude-cli-rc{proc.returncode}",
                error=err[:300],
            )
        text = stdout.decode(errors="ignore").strip()
        if not text:
            return LLMCallResult(text="", backend="mock", model_hint="claude-cli-empty", error="empty")
        return LLMCallResult(text=text, backend="claude-cli", model_hint=self.model)


# ──────────────────────────────────────────────────────────────────────────
# Provider registry
# ──────────────────────────────────────────────────────────────────────────

_REGISTRY: dict[str, LLMProvider] = {
    "anthropic": AnthropicProvider(),
    "openai": OpenAIProvider(),
}


def get_provider(name: str) -> LLMProvider:
    if name not in _REGISTRY:
        raise KeyError(f"unknown provider: {name}")
    return _REGISTRY[name]


def report_provider_status() -> dict[str, dict[str, Any]]:
    """Provider 별 가용 인증 경로 진단 (서버 시작 시·디버깅용)."""
    out: dict[str, dict[str, Any]] = {}
    for name, prov in _REGISTRY.items():
        api_envs_present = [e for e in prov.api_key_env_vars if os.environ.get(e)]
        cli_present = bool(prov.cli_binary and shutil.which(prov.cli_binary))
        out[name] = {
            "model": prov.model,
            "api_key_env_vars": list(prov.api_key_env_vars),
            "api_key_present": api_envs_present,
            "cli_binary": prov.cli_binary,
            "cli_available": cli_present,
            "preferred_path": (
                "api" if api_envs_present else "cli" if cli_present else "mock"
            ),
        }
    return out
