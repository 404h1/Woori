"""
페이지별 TTS 스크립트를 Edge TTS로 합성해서 ../public/audio/pageXX.mp3 로 저장.
한 번 실행하면 React 앱은 백엔드 없이 정적 MP3만 재생.

실행:
    .\.venv\Scripts\python.exe generate_mp3.py

스크립트가 바뀌면 아래 SCRIPTS dict를 page 파일과 맞춰 수정 후 재실행.
"""

from __future__ import annotations

import asyncio
import re
from pathlib import Path

import edge_tts

VOICE = "ko-KR-SunHiNeural"
RATE = "-5%"
PITCH = "+0Hz"

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "audio"

SRC_DIR = Path(__file__).resolve().parent.parent / "src" / "pages"
PAGES = {
    "page02":  "Page02_InvestmentResult.jsx",
    "page03":  "Page03_FundList.jsx",
    "page03c": "Page03c_FundAI.jsx",
    "page05":  "Page05_InvestorCheck.jsx",
    "page06":  "Page06_FundJoin.jsx",
    "page07":  "Page07_Document.jsx",
}

SCRIPT_PATTERN = re.compile(r"const\s+SCRIPT\s*=\s*'([^']+)'", re.DOTALL)


def extract_script(jsx_path: Path) -> str:
    text = jsx_path.read_text(encoding="utf-8")
    m = SCRIPT_PATTERN.search(text)
    if not m:
        raise RuntimeError(f"SCRIPT const not found in {jsx_path.name}")
    return m.group(1).strip()


async def synth(text: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE, pitch=PITCH)
    with open(out_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])


async def main() -> None:
    print(f"Voice: {VOICE}  rate: {RATE}  pitch: {PITCH}")
    print(f"Out:   {OUT_DIR}\n")

    for key, filename in PAGES.items():
        jsx = SRC_DIR / filename
        out = OUT_DIR / f"{key}.mp3"
        try:
            text = extract_script(jsx)
            print(f"  [{key}] {len(text)}자 합성중...", flush=True)
            await synth(text, out)
            size_kb = out.stat().st_size / 1024
            print(f"          → {out.name} ({size_kb:.1f} KB)")
        except Exception as e:
            print(f"  [{key}] FAILED: {e}")

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())
