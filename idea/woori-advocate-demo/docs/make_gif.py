"""
docs/demo_recording/*.png -> docs/demo_recording/woori_demo.gif

5단계 PNG를 발표용 GIF로 묶는다:
- 각 프레임에 단계 라벨 + 진행바 오버레이
- 1280px 다운샘플, 16:9 크롭, 흰 배경 합성
- 각 프레임 표시 시간 3~6초, 무한 loop
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
REC = HERE / "demo_recording"

FRAMES = [
    ("woori_demo_01_initial.png", 3000,
     "STEP 1 - 초기 화면 / Provider badge 표시"),
    ("woori_demo_02_review.png", 5000,
     "STEP 2 - 가입 직전 분할 화면 / Seller(Claude) vs Advocate(GPT)"),
    ("woori_demo_03_mad.png", 6000,
     "STEP 3 - MAD 2라운드 토론 / 상호 반박 + Moderator 합의"),
    ("woori_demo_04_senior.png", 4000,
     "STEP 4 - 시니어 모드 / 큰 글자와 TTS"),
    ("woori_demo_05_fds.png", 6000,
     "STEP 5 - 송금 단계 / FDS BLOCK + 가족 동의 절차"),
]

TARGET_W = 1280
TARGET_H = int(TARGET_W * 9 / 16)
BAR_H = 6
LABEL_H = 56


def _font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/malgunbd.ttf",
        "C:/Windows/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_LABEL = _font(22)
F_SUB = _font(14)

images = []
durations = []
total_frames = len(FRAMES)

for idx, (fname, dur, label) in enumerate(FRAMES, start=1):
    src = REC / fname
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert("RGB")

    ratio = TARGET_W / img.width
    new_h = int(img.height * ratio)
    img = img.resize((TARGET_W, new_h), Image.LANCZOS)

    if img.height > TARGET_H:
        img = img.crop((0, 0, TARGET_W, TARGET_H))
    elif img.height < TARGET_H:
        bg = Image.new("RGB", (TARGET_W, TARGET_H), (255, 255, 255))
        bg.paste(img, (0, (TARGET_H - img.height) // 2))
        img = bg

    canvas_h = TARGET_H + LABEL_H + BAR_H
    canvas = Image.new("RGB", (TARGET_W, canvas_h), (255, 255, 255))
    canvas.paste(img, (0, 0))

    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, TARGET_H, TARGET_W, TARGET_H + LABEL_H], fill=(0, 60, 105))
    draw.text((20, TARGET_H + 8), label, font=F_LABEL, fill=(255, 255, 255))
    draw.text(
        (20, TARGET_H + 34),
        f"Woori Advocate / Woori Bank x SSAFY 2026 / Frame {idx}/{total_frames}",
        font=F_SUB,
        fill=(202, 220, 252),
    )

    bar_y = TARGET_H + LABEL_H
    draw.rectangle([0, bar_y, TARGET_W, bar_y + BAR_H], fill=(235, 235, 240))
    bar_w = int(TARGET_W * idx / total_frames)
    draw.rectangle([0, bar_y, bar_w, bar_y + BAR_H], fill=(200, 35, 43))

    images.append(canvas.convert("P", palette=Image.ADAPTIVE))
    durations.append(dur)

out = REC / "woori_demo.gif"
images[0].save(
    out,
    save_all=True,
    append_images=images[1:],
    duration=durations,
    loop=0,
    optimize=True,
    disposal=2,
)
print(f"Wrote {out}")
print(f"  {out.stat().st_size / 1024:.1f} KB / {len(images)} frames / {sum(durations) / 1000:.0f}s")
