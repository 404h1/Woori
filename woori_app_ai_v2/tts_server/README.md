# Edge TTS 음성 생성 도구

WON AI 뱅커 데모용 음성 합성. Microsoft Edge TTS의 한국어 여성 보이스 `ko-KR-SunHiNeural`로 페이지별 안내 음성을 미리 MP3로 생성합니다.

**런타임에는 백엔드 필요 없어요.** 생성된 MP3는 `../public/audio/`에 정적 파일로 들어가고, React 앱이 그걸 그대로 재생합니다.

## 처음 셋업

```powershell
cd woori_app_ai_v2\tts_server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 음성 생성

스크립트(`src/pages/*.jsx`의 `SCRIPT` 상수)를 바꿨거나 보이스를 교체했을 때만 실행:

```powershell
.\.venv\Scripts\python.exe generate_mp3.py
```

→ `public/audio/page02.mp3`, `page03.mp3`, `page03c.mp3`, `page05.mp3`, `page06.mp3`, `page07.mp3` 6개 갱신.

## 보이스·속도 변경

[generate_mp3.py](generate_mp3.py) 상단 `VOICE`, `RATE`, `PITCH` 수정 후 재생성.

한국어 여성 보이스 후보:

| 코드 | 톤 |
|---|---|
| `ko-KR-SunHiNeural` | 따뜻하고 자연스러움 (현재) |
| `ko-KR-JiMinNeural` | 밝고 젊은 톤 |
| `ko-KR-SeoHyeonNeural` | 차분하고 성숙함 |
| `ko-KR-YuJinNeural` | 활발한 톤 |

전체 목록: `.\.venv\Scripts\edge-tts.exe --list-voices | findstr ko-KR`

## 동적 합성 서버 (선택)

[server.py](server.py)는 FastAPI 백엔드. 페이지 안내가 아닌 **동적 음성**(예: 사용자 입력 기반 답변)이 필요할 때만 띄우면 됩니다. 현재 데모는 사용 안 함.

```powershell
.\.venv\Scripts\python.exe server.py   # localhost:8001
```
