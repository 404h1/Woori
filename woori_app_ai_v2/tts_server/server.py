"""
Edge TTS FastAPI 백엔드.
React 앱의 VoiceContext가 POST /api/tts 로 호출하면
ko-KR-SunHiNeural 한국어 여성 보이스로 합성한 MP3를 반환합니다.

실행:
    pip install -r requirements.txt
    python server.py
        (또는: uvicorn server:app --host 0.0.0.0 --port 8001 --reload)
"""

from __future__ import annotations

import asyncio
import io
import logging

import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tts_server")

DEFAULT_VOICE = "ko-KR-SunHiNeural"  # 한국어 여성, 자연스럽고 따뜻한 톤

app = FastAPI(title="Woori Demo Edge TTS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    voice: str = DEFAULT_VOICE
    rate: str = "-5%"   # 시니어 페르소나 — 살짝 천천히
    pitch: str = "+0Hz"


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "voice": DEFAULT_VOICE}


@app.post("/api/tts")
async def synthesize(req: TTSRequest):
    try:
        communicate = edge_tts.Communicate(
            text=req.text,
            voice=req.voice,
            rate=req.rate,
            pitch=req.pitch,
        )

        buf = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buf.write(chunk["data"])

        if buf.tell() == 0:
            raise HTTPException(status_code=500, detail="Edge TTS returned no audio")

        buf.seek(0)
        return StreamingResponse(
            buf,
            media_type="audio/mpeg",
            headers={"Cache-Control": "no-store"},
        )
    except HTTPException:
        raise
    except Exception as e:
        log.exception("TTS synth failed")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
