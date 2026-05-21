# Woori Advocate Demo Recording

This folder contains the recorded simulator flow used for presentation backup.

## Files

- `woori_demo.gif` — 24-second animated demo, 5 frames.
- `woori_demo_01_initial.png` — initial screen with provider status.
- `woori_demo_02_review.png` — split-screen Seller/Advocate review.
- `woori_demo_03_mad.png` — MAD two-round debate and moderator consensus.
- `woori_demo_04_senior.png` — senior-mode UI state.
- `woori_demo_05_fds.png` — FDS BLOCK and family-consent flow.

## Regenerate

Run the app, capture the five PNGs with the simulator flow, then:

```powershell
cd docs
python make_gif.py
```
