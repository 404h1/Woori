"""
역삼동_2.m4a 화자 분리 + 전사 + 음성 클로닝 파이프라인
- Whisper large-v3 → 한국어 전사 + 타임스탬프
- resemblyzer → 화자 임베딩 + K-means 클러스터링 (3명)
- Qwen3-TTS → 화자별 음성 클로닝
"""
import os, sys, copy, json
import numpy as np
import soundfile as sf
import subprocess
import imageio_ffmpeg
import torch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE   = os.path.join(BASE_DIR, "source.m4a")
FULL_WAV = os.path.join(BASE_DIR, "full_audio.wav")          # 16kHz mono (Whisper용)
HIFI_WAV = os.path.join(BASE_DIR, "full_audio_24k.wav")      # 24kHz mono (TTS용)
OUT_DIR  = os.path.join(BASE_DIR, "speakers")
SCRIPT   = os.path.join(BASE_DIR, "transcript.md")

os.makedirs(OUT_DIR, exist_ok=True)
N_SPEAKERS = 3
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()


# ── Step 1: 전처리 ─────────────────────────────────────────
def convert_audio():
    print("[1] 오디오 변환 중...")
    for out, sr in [(FULL_WAV, "16000"), (HIFI_WAV, "24000")]:
        if not os.path.exists(out):
            r = subprocess.run(
                [ffmpeg, "-y", "-i", SOURCE, "-ar", sr, "-ac", "1",
                 "-acodec", "pcm_s16le", out],
                capture_output=True
            )
            if r.returncode != 0:
                print("오류:", r.stderr.decode("utf-8", errors="replace")[-300:])
                sys.exit(1)
    print(f"    → {FULL_WAV} (16kHz), {HIFI_WAV} (24kHz) 생성")


# ── Step 2: Whisper 전사 ──────────────────────────────────
def transcribe():
    print("[2] Whisper 전사 중 (캐시 로드)...")
    import whisper

    # 시스템 ffmpeg 없어도 되도록 numpy array로 직접 로드
    audio_np, sr = sf.read(FULL_WAV, dtype="float32")
    if audio_np.ndim > 1:
        audio_np = audio_np.mean(axis=1)
    # Whisper expects float32 mono at 16000Hz
    if sr != 16000:
        import librosa
        audio_np = librosa.resample(audio_np, orig_sr=sr, target_sr=16000)

    model = whisper.load_model("large-v3")
    result = model.transcribe(
        audio_np,
        language="ko",
        word_timestamps=True,
        verbose=False,
    )
    print(f"    → 전사 완료: {len(result['segments'])} 세그먼트")
    return result


# ── Step 3: 화자 임베딩 + 클러스터링 ──────────────────────
def diarize(result):
    print("[3] 화자 분리 중 (resemblyzer)...")
    from resemblyzer import preprocess_wav, VoiceEncoder
    from sklearn.cluster import KMeans, AgglomerativeClustering

    wav_full, sr = sf.read(FULL_WAV)
    if wav_full.dtype != np.float32:
        wav_full = wav_full.astype(np.float32)

    encoder = VoiceEncoder()
    segments = result["segments"]

    # 세그먼트별 임베딩 계산
    embeds = []
    valid_segs = []
    for seg in segments:
        start = seg["start"]
        end   = seg["end"]
        dur   = end - start
        if dur < 0.3:
            continue
        s_idx = int(start * sr)
        e_idx = int(end   * sr)
        chunk = wav_full[s_idx:e_idx]
        if len(chunk) < int(0.3 * sr):
            continue
        # resemblyzer는 16kHz 기대
        try:
            embed = encoder.embed_utterance(chunk)
            embeds.append(embed)
            valid_segs.append(seg)
        except Exception as e:
            print(f"    세그먼트 {seg['id']} 임베딩 실패: {e}")

    if len(valid_segs) == 0:
        print("    유효 세그먼트 없음. 수동 분할로 폴백.")
        return None, segments

    embeds_arr = np.vstack(embeds)
    n_clusters = min(N_SPEAKERS, len(valid_segs))

    if len(valid_segs) < N_SPEAKERS:
        # 클러스터 수를 줄임
        print(f"    세그먼트가 {len(valid_segs)}개뿐 → {len(valid_segs)}명으로 처리")
        n_clusters = len(valid_segs)

    if n_clusters == 1:
        labels = [0] * len(valid_segs)
    else:
        km = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
        labels = km.fit_predict(embeds_arr)

    print(f"    → {n_clusters}명 화자 구분 완료")
    return labels, valid_segs


# ── Step 4: 대본 작성 + 오디오 분할 ──────────────────────
def write_transcript_and_split(labels, valid_segs, result, n_actual):
    print("[4] 대본 작성 + 화자별 오디오 추출 중...")

    wav_24k, sr_24k = sf.read(HIFI_WAV)
    if wav_24k.dtype != np.float32:
        wav_24k = wav_24k.astype(np.float32)

    speaker_names = {i: f"화자{chr(65+i)}" for i in range(n_actual)}
    speaker_segments = {i: [] for i in range(n_actual)}

    if labels is None:
        # 폴백: 세그먼트 순서대로 화자 순환 배정
        for idx, seg in enumerate(valid_segs):
            spk = idx % N_SPEAKERS
            speaker_segments[spk % n_actual].append(seg)
        labels = [i % n_actual for i in range(len(valid_segs))]
    else:
        for spk_id, seg in zip(labels, valid_segs):
            speaker_segments[int(spk_id)].append(seg)

    # 대본 작성
    lines = [
        "# 역삼동_2 대본 (자동 생성)\n",
        f"> Whisper large-v3 전사 + resemblyzer 화자분리 ({n_actual}명)\n\n",
        "---\n\n",
    ]
    ordered = sorted(
        [(int(spk), seg) for spk, seg in zip(labels, valid_segs)],
        key=lambda x: x[1]["start"]
    )
    for spk_id, seg in ordered:
        name = speaker_names[spk_id]
        t_start = seg["start"]
        t_end   = seg["end"]
        text    = seg["text"].strip()
        lines.append(f"**[{name}]** `{t_start:.2f}s ~ {t_end:.2f}s`  \n")
        lines.append(f"{text}\n\n")

    with open(SCRIPT, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"    → {SCRIPT} 저장 완료")

    # 화자별 오디오 추출
    speaker_wav_paths = {}
    speaker_ref_texts = {}
    for spk_id, segs in speaker_segments.items():
        if not segs:
            continue
        name = speaker_names[spk_id]
        # 가장 긴 단일 세그먼트를 레퍼런스로 선택
        best_seg = max(segs, key=lambda s: s["end"] - s["start"])
        s_idx = int(best_seg["start"] * sr_24k)
        e_idx = int(best_seg["end"]   * sr_24k)
        chunk = wav_24k[s_idx:e_idx]

        out_path = os.path.join(OUT_DIR, f"speaker_{chr(65+spk_id)}_ref.wav")
        sf.write(out_path, chunk, sr_24k)
        speaker_wav_paths[spk_id] = out_path
        speaker_ref_texts[spk_id] = best_seg["text"].strip()
        print(f"    → {name} 레퍼런스: {out_path} ({best_seg['end']-best_seg['start']:.2f}s) '{speaker_ref_texts[spk_id]}'")

    return speaker_wav_paths, speaker_ref_texts, speaker_names


# ── Step 5: 화자별 음성 클로닝 ───────────────────────────
def clone_all(speaker_wav_paths, speaker_ref_texts, speaker_names):
    print("[5] Qwen3-TTS 화자별 클로닝 시작...")
    from qwen_tts import Qwen3TTSModel

    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        dtype=torch.bfloat16,
        device_map="cuda:0" if torch.cuda.is_available() else "cpu",
    )

    synth_texts = {
        0: "안녕하세요, 저는 우리은행 AI 안내사입니다.",
        1: "펀드 가입 전에 단점을 꼭 확인하세요.",
        2: "투자는 신중하게, 선택은 현명하게 하시기 바랍니다.",
    }

    for spk_id, ref_wav in speaker_wav_paths.items():
        name = speaker_names[spk_id]
        ref_text  = speaker_ref_texts[spk_id]
        synth_txt = synth_texts.get(spk_id, "안녕하세요.")

        print(f"\n  [{name}] 레퍼런스: '{ref_text}'")
        print(f"  [{name}] 합성 텍스트: '{synth_txt}'")

        try:
            prompt = model.create_voice_clone_prompt(
                ref_audio=ref_wav,
                ref_text=ref_text,
                x_vector_only_mode=False,
            )
            wavs, sr = model.generate_voice_clone(
                text=synth_txt,
                language="Korean",
                voice_clone_prompt=prompt,
            )
            out_path = os.path.join(OUT_DIR, f"speaker_{chr(65+spk_id)}_cloned.wav")
            sf.write(out_path, wavs[0], sr)
            print(f"  [{name}] → 저장: {out_path}")
        except Exception as e:
            print(f"  [{name}] 클로닝 실패: {e}")


# ── 메인 ─────────────────────────────────────────────────
if __name__ == "__main__":
    convert_audio()
    result     = transcribe()
    labels, valid_segs = diarize(result)
    n_actual   = len(set(labels)) if labels is not None else min(N_SPEAKERS, len(valid_segs))
    spk_wavs, spk_texts, spk_names = write_transcript_and_split(
        labels, valid_segs, result, n_actual
    )
    print("\n=== 대본 ===")
    with open(SCRIPT, encoding="utf-8") as f:
        print(f.read())

    clone_all(spk_wavs, spk_texts, spk_names)
    print("\n\n=== 완료 ===")
    print(f"대본: {SCRIPT}")
    print(f"화자별 WAV: {OUT_DIR}/")
