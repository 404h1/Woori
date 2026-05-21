"""
woori_advocate_v1.pptx → slide-NN.png (15장) 렌더링.

LibreOffice·MS Office 가 없는 환경에서 aspose-slides 로 변환.
Spire.Presentation Free 가 10장 제한이 있어 aspose-slides 로 교체.

aspose-slides 무료 버전도 evaluation watermark 가 있으나 슬라이드 수 제한 없음.
시각 QA 용 PNG 출력. 평가 환경에서는 본 .pptx 그대로 사용.
"""
from __future__ import annotations

import sys
from pathlib import Path

import aspose.slides as slides

HERE = Path(__file__).parent
SRC = HERE / "woori_advocate_v1.pptx"
OUT_DIR = HERE / "slides_png"
OUT_DIR.mkdir(exist_ok=True)

# 기존 파일 정리
for old in OUT_DIR.glob("slide-*.png"):
    old.unlink()

with slides.Presentation(str(SRC)) as prs:
    print(f"Loaded {SRC.name} — {len(prs.slides)} slides")
    for i, slide in enumerate(prs.slides):
        # 1600x900 = 16:9 고해상도
        with slide.get_image(1.5, 1.5) as img:
            out = OUT_DIR / f"slide-{i+1:02d}.png"
            img.save(str(out), slides.ImageFormat.PNG)
        print(f"  wrote {out.name}")

print(f"\n✓ Done. Output: {OUT_DIR}")
