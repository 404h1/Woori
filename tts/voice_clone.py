import torch
import soundfile as sf
import numpy as np
import subprocess
import sys
import os
import imageio_ffmpeg


# ── 경로 설정 ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "source.m4a")   # 한글 파일명 회피용 복사본
SAMPLE_WAV  = os.path.join(BASE_DIR, "voice_sample.wav")
OUTPUT_WAV  = os.path.join(BASE_DIR, "output_cloned.wav")

REF_TEXT    = "저리가세요 저리가세요"          # 3~5초 구간에서 말한 내용
SYNTH_TEXT  = "안녕하세요, 저는 우리은행 AI 안내사 김민지입니다."
LANGUAGE    = "Korean"
MODEL_ID    = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"


# ── Step 1: 3~5초 구간 추출 ──────────────────────────────
def extract_clip():
    if os.path.exists(SAMPLE_WAV):
        print("[1] voice_sample.wav 이미 존재, 재사용")
        return

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg,
        "-y",
        "-i", INPUT_FILE,
        "-ss", "3",
        "-t", "2",         # 3초~5초 = 2초 길이
        "-ar", "24000",    # Qwen3-TTS 권장 샘플레이트
        "-ac", "1",        # 모노
        "-acodec", "pcm_s16le",
        SAMPLE_WAV,
    ]
    print("[1] 3~5초 클립 추출 중...")
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print("오류:", result.stderr.decode(errors='replace')[-500:])
        sys.exit(1)
    print(f"    → {SAMPLE_WAV} 생성 완료")


# ── Step 2: 모델 로드 ─────────────────────────────────────
def load_model():
    print(f"[2] 모델 로드: {MODEL_ID}")
    print("    (첫 실행 시 다운로드 약 3~6GB, 시간 걸림)")

    from qwen_tts import Qwen3TTSModel

    model = Qwen3TTSModel.from_pretrained(
        MODEL_ID,
        device_map="cuda:0",
        torch_dtype=torch.bfloat16,
        # flash_attention_2는 Windows에서 미지원 → 기본값(sdpa) 사용
    )
    print("    → 모델 로드 완료")
    return model


# ── Step 3: 음성 클로닝 ───────────────────────────────────
def clone_and_synthesize(model):
    print("[3] 음성 클로닝 프롬프트 생성 중...")

    prompt = model.create_voice_clone_prompt(
        ref_audio=SAMPLE_WAV,
        ref_text=REF_TEXT,
        x_vector_only_mode=False,   # ICL 모드 (레퍼런스 텍스트 활용, 품질↑)
    )
    print("    → 클로닝 프롬프트 생성 완료")

    print(f"[4] 합성 중: \"{SYNTH_TEXT}\"")
    wavs, sr = model.generate_voice_clone(
        text=SYNTH_TEXT,
        language=LANGUAGE,
        voice_clone_prompt=prompt,
    )

    sf.write(OUTPUT_WAV, wavs[0], sr)
    print(f"    → 저장 완료: {OUTPUT_WAV}")
    print(f"    → 샘플레이트: {sr}Hz")


# ── 메인 ─────────────────────────────────────────────────
if __name__ == "__main__":
    extract_clip()
    model = load_model()
    clone_and_synthesize(model)
    print("\n완료! output_cloned.wav 를 재생해보세요.")
