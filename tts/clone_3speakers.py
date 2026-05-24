"""
역삼동_2.m4a 3화자 분리 음성 클로닝
화자1: 구간1+구간2 (데모 영상이에요 / 영상을 찍어놨나?)
화자2: 구간3 (아니 아니 아니 아니 저리 가세요 저리 가세요)
화자3: 구간4 (오) ← 0.71s, 품질 제한
"""
import os, sys
import numpy as np
import soundfile as sf
import torch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FULL_24K  = os.path.join(BASE_DIR, "full_audio_24k.wav")
OUT_DIR   = os.path.join(BASE_DIR, "speakers")
os.makedirs(OUT_DIR, exist_ok=True)

# 24kHz 오디오 로드
wav24, sr24 = sf.read(FULL_24K, dtype="float32")
if wav24.ndim > 1:
    wav24 = wav24.mean(axis=1)

# ── 화자별 레퍼런스 세그먼트 정의 ──────────────────────────
# 화자1: 구간1(0.08-1.20s) + 구간2(1.40-2.35s) 합침
# 화자2: 구간3(2.65-4.85s)
# 화자3: 구간4(6.05-6.76s)

def extract(start, end):
    return wav24[int(start * sr24): int(end * sr24)]

segs = {
    "화자1": {
        "chunks": [(0.08, 1.20), (1.40, 2.35)],
        "ref_text": "데모 영상이에요 영상을 찍어놨나",
        "synth_text": "안녕하세요, 저는 우리은행 AI 안내사입니다. 상담을 시작하겠습니다.",
    },
    "화자2": {
        "chunks": [(2.65, 4.85)],
        "ref_text": "아니 아니 아니 아니 저리 가세요 저리 가세요",
        "synth_text": "펀드 가입 전에 반드시 단점을 확인하시기 바랍니다.",
    },
    "화자3": {
        "chunks": [(6.05, 6.76)],
        "ref_text": "오",
        "synth_text": "투자는 신중하게, 선택은 현명하게 하시기 바랍니다.",
    },
}

# ── 레퍼런스 WAV 생성 ──────────────────────────────────────
print("[1] 화자별 레퍼런스 오디오 생성...")
ref_paths = {}
for name, info in segs.items():
    chunks_audio = []
    for start, end in info["chunks"]:
        chunk = extract(start, end)
        chunks_audio.append(chunk)
    combined = np.concatenate(chunks_audio) if len(chunks_audio) > 1 else chunks_audio[0]
    path = os.path.join(OUT_DIR, f"{name}_ref.wav")
    sf.write(path, combined, sr24)
    dur = len(combined) / sr24
    print(f"  {name}: {path} ({dur:.2f}s) '{info['ref_text']}'")
    ref_paths[name] = path

# ── 대본 저장 ──────────────────────────────────────────────
transcript_path = os.path.join(BASE_DIR, "transcript.md")
with open(transcript_path, "w", encoding="utf-8") as f:
    f.write("# 역삼동_2 대본 (화자 3명)\n\n")
    f.write("> Whisper large-v3 전사 + resemblyzer 화자분리\n\n")
    f.write("---\n\n")
    f.write("**[화자1]** `0.08s ~ 1.20s`  \n데모 영상이에요\n\n")
    f.write("**[화자1]** `1.40s ~ 2.35s`  \n영상을 찍어놨나?\n\n")
    f.write("**[화자2]** `2.65s ~ 4.85s`  \n아니 아니 아니 아니 저리 가세요 저리 가세요\n\n")
    f.write("**[화자3]** `6.05s ~ 6.76s`  \n오\n\n")
    f.write("---\n\n")
    f.write("## 화자 분리 근거\n\n")
    f.write("| 구간 | 화자 | 유사도 근거 |\n")
    f.write("|------|------|-------------|\n")
    f.write("| 구간1 ↔ 구간2 | **화자1 동일** | 코사인 유사도 0.723 (동일인 가능성 높음) |\n")
    f.write("| 구간3 | **화자2** | 유사도 0.573~0.577 (다른 화자) |\n")
    f.write("| 구간4 | **화자3** | 구간3과 유사도 0.303 (명확히 다른 화자) |\n")
    f.write("\n> ⚠️ 화자3(구간4, 0.71s '오')은 레퍼런스가 너무 짧아 클로닝 품질 제한\n")

print(f"\n[2] 대본 저장: {transcript_path}")

# ── Qwen3-TTS 클로닝 ───────────────────────────────────────
print("[3] Qwen3-TTS 화자별 클로닝 시작...\n")
from qwen_tts import Qwen3TTSModel

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    dtype=torch.bfloat16,
    device_map="cuda:0" if torch.cuda.is_available() else "cpu",
)

for name, info in segs.items():
    ref_wav  = ref_paths[name]
    ref_text = info["ref_text"]
    synth    = info["synth_text"]
    dur = sf.info(ref_wav).duration

    print(f"  ── {name} ──")
    print(f"     레퍼런스: {dur:.2f}s | '{ref_text}'")
    print(f"     합성 텍스트: '{synth}'")

    try:
        prompt = model.create_voice_clone_prompt(
            ref_audio=ref_wav,
            ref_text=ref_text,
            x_vector_only_mode=False,
        )
        wavs, sr = model.generate_voice_clone(
            text=synth,
            language="Korean",
            voice_clone_prompt=prompt,
        )
        out = os.path.join(OUT_DIR, f"{name}_cloned.wav")
        sf.write(out, wavs[0], sr)
        print(f"     → 저장: {out}\n")
    except Exception as e:
        print(f"     ✗ 클로닝 실패: {e}\n")

print("=== 완료 ===")
print(f"대본:    {transcript_path}")
print(f"결과물:  {OUT_DIR}/")
print(f"  화자1_ref.wav / 화자1_cloned.wav")
print(f"  화자2_ref.wav / 화자2_cloned.wav")
print(f"  화자3_ref.wav / 화자3_cloned.wav (품질 제한)")
