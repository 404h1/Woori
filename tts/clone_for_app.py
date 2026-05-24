"""
준엽_목소리.m4a (8.49s) 를 reference로 7개 페이지 TTS mp3 생성
→ woori_app_ai/public/audio/page0X.mp3 자동 저장

파이프라인:
1. ffmpeg: m4a → 24kHz mono wav
2. Whisper large-v3: 자동 전사 (ref_text)
3. Qwen3-TTS 음성 클로닝 × 7개 SCRIPT
4. ffmpeg: wav → mp3 (192kbps)
5. woori_app_ai/public/audio/ 로 복사
"""
import os, sys, subprocess, shutil
import numpy as np
import soundfile as sf
import torch
import imageio_ffmpeg


# ── 경로 설정 ──────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
SOURCE_M4A  = os.path.join(BASE_DIR, "준엽_목소리.m4a")
REF_WAV     = os.path.join(BASE_DIR, "준엽_ref_24k.wav")
OUT_DIR     = os.path.join(BASE_DIR, "app_outputs")
APP_AUDIO_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "woori_app_ai", "public", "audio"))

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(APP_AUDIO_DIR, exist_ok=True)

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()


# ── 7개 페이지 대본 (woori_app_ai의 각 SCRIPT와 동일) ──────
SCRIPTS = {
    "page02": "결과가 나왔어요. 공격투자형이라는 건, 높은 수익을 노리는 만큼 원금을 잃을 위험도 큰 상품에 어울리는 성향이라는 뜻이에요. 본인 상황과 정말 맞는지 한 번 더 생각해보세요.",
    "page03": "여기 보이는 펀드는 모두 매우높은위험 등급이에요. 수익률 숫자가 커 보여도, 과거 수익률이 미래를 보장하지는 않아요. 예금자보호 대상이 아니라는 점도 기억하세요. 펀드 이름을 누르면 자세한 내용을 보실 수 있어요.",
    "page03c": "이 펀드는 엔비디아, TSMC 같은 글로벌 AI 반도체 기업에 투자해요. 최근 3개월 수익률이 +46%라는 건, 같은 폭으로 떨어질 수도 있다는 뜻이에요. 환매수수료가 있어서 중간에 빼면 손실이 생길 수 있고, 해외 주식이라 환율에 따라 추가 손익도 발생해요. 장점, 주의, 적합한 분 탭을 하나씩 읽어보시고 본인에게 맞는지 직접 판단해주세요.",
    "page05": "가입 전 두 가지를 확인하는 단계예요. 첫 번째는 최근 1개월 안에 대출을 받으셨거나 받을 예정인지, 두 번째는 증권사에서 확인받은 전문 금융소비자인지 묻는 거예요. 본인 상황을 떠올려보시고 직접 답해주세요.",
    "page06": "가입할 금액을 입력하는 단계예요. 출금가능금액 안에서, 본인이 잃어도 생활에 지장이 없는 금액만 입력해주세요. 한 번 가입하면 매수예정일에 자동으로 빠져나가요.",
    "page07": "상품설명서예요. 원금 손실 가능성, 환매 조건, 청약철회가 가능한 기간이 적혀 있어요. 끝까지 직접 읽어보셔야 가입이 진행돼요. 시간이 걸려도 천천히 보시고, 이해 안 되는 부분은 상담을 요청하세요.",
    "page08": "해피콜이에요. 가입한 상품의 위험성, 설명서 확인 여부, 가입 강요 여부를 본인이 실제로 어떻게 인지하고 가입했는지 확인하는 단계예요. 8개 질문을 하나씩 읽어보시고, 본인이 직접 느낀 대로 답해주세요.",
}


# ── Step 1: m4a → 24kHz mono wav ───────────────────────────
def convert_reference():
    if os.path.exists(REF_WAV):
        print(f"[1] 이미 존재: {REF_WAV}")
        return
    print(f"[1] m4a → 24kHz wav 변환 중...")
    r = subprocess.run([
        ffmpeg, "-y", "-i", SOURCE_M4A,
        "-ar", "24000", "-ac", "1",
        "-acodec", "pcm_s16le",
        REF_WAV,
    ], capture_output=True)
    if r.returncode != 0:
        print("오류:", r.stderr.decode("utf-8", errors="replace")[-500:])
        sys.exit(1)
    dur = sf.info(REF_WAV).duration
    print(f"    → {REF_WAV} ({dur:.2f}s)")


# ── Step 2: ref_text (사용자가 직접 제공) ─────────────────
REF_TEXT = "안녕하세요 김준엽입니다. 숙취때문에 너무 힘들어 사당가고 있는데 진짜 죽을 것 같네요 이거야"

def get_reference_text():
    print(f"[2] ref_text 사용: '{REF_TEXT}'")
    return REF_TEXT


# ── Step 3: Qwen3-TTS 클로닝 × 7회 ────────────────────────
def clone_all(ref_text):
    print(f"\n[3] Qwen3-TTS 모델 로드 (Qwen/Qwen3-TTS-12Hz-1.7B-Base)...")
    from qwen_tts import Qwen3TTSModel

    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        dtype=torch.bfloat16,
        device_map="cuda:0" if torch.cuda.is_available() else "cpu",
    )
    print(f"    → 모델 로드 완료 (device: {'CUDA' if torch.cuda.is_available() else 'CPU'})")

    print(f"\n[4] 클로닝 프롬프트 생성 (ref_text='{ref_text}')...")
    prompt = model.create_voice_clone_prompt(
        ref_audio=REF_WAV,
        ref_text=ref_text,
        x_vector_only_mode=False,  # ICL 모드 (품질↑)
    )

    print(f"\n[5] 7개 페이지 합성 시작...\n")
    wav_paths = {}
    for page_id, script_text in SCRIPTS.items():
        print(f"  [{page_id}] {script_text[:40]}...")
        try:
            wavs, sr = model.generate_voice_clone(
                text=script_text,
                language="Korean",
                voice_clone_prompt=prompt,
            )
            wav_path = os.path.join(OUT_DIR, f"{page_id}.wav")
            sf.write(wav_path, wavs[0], sr)
            wav_paths[page_id] = wav_path
            dur = len(wavs[0]) / sr
            print(f"     → {wav_path} ({dur:.1f}s)\n")
        except Exception as e:
            print(f"     ✗ 실패: {e}\n")
    return wav_paths


# ── Step 4: WAV → MP3 + app에 복사 ─────────────────────────
def convert_and_deploy(wav_paths):
    print(f"\n[6] MP3 변환 + 앱 폴더로 복사...")
    for page_id, wav_path in wav_paths.items():
        mp3_local = os.path.join(OUT_DIR, f"{page_id}.mp3")
        mp3_app   = os.path.join(APP_AUDIO_DIR, f"{page_id}.mp3")

        r = subprocess.run([
            ffmpeg, "-y", "-i", wav_path,
            "-ar", "22050", "-ac", "1", "-b:a", "96k",
            mp3_local,
        ], capture_output=True)
        if r.returncode != 0:
            print(f"  [FAIL] {page_id} mp3 conversion failed")
            continue

        shutil.copy(mp3_local, mp3_app)
        size_kb = os.path.getsize(mp3_app) / 1024
        print(f"  [OK] {page_id}.mp3 -> {mp3_app} ({size_kb:.0f} KB)")


# ── 메인 ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("준엽 목소리로 우리은행 앱 TTS 7개 생성")
    print("=" * 60)

    if not os.path.exists(SOURCE_M4A):
        print(f"✗ 원본 없음: {SOURCE_M4A}")
        sys.exit(1)

    convert_reference()
    ref_text = get_reference_text()
    wav_paths = clone_all(ref_text)
    convert_and_deploy(wav_paths)

    print("\n" + "=" * 60)
    print("완료!")
    print(f"  로컬:  {OUT_DIR}/page0X.wav, page0X.mp3")
    print(f"  앱:    {APP_AUDIO_DIR}/page0X.mp3")
    print("\n다음 단계:")
    print(f"  cd ../woori_app_ai")
    print(f"  npm run dev  # 자동으로 mp3 사용 (실패 시 Web Speech TTS fallback)")
    print("=" * 60)
