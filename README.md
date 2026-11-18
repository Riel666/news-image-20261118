# news-image-20261118 — "The World in One Picture"

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Riel666/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Riel666/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Entry for make.fun's **news-image-20261118** bounty ("Sum up 18 November's
world news in one image", $250, top 50 share).

The image sums up Wednesday 18 November 2026 in four stories, as reported
that day (BBC, Reuters, AP, The Guardian):

1. **Iran drones hit US radar** — Iran attacks a US military radar system
   in Bahrain with drones; Bahrain issues an all-clear after the overnight
   warning; Kuwait's army reports drone interceptions.
2. **Nvidia doubles revenue** — quarterly revenue $115.84bn, up 103% year
   on year, in its first earnings since Jensen Huang's exit; the board
   chairman says the company will not reinstate Huang; Trump backs calls
   for his return.
3. **UK sanctions settlement firms** — Britain sanctions eight Israeli
   firms over West Bank settlements (plus a Gaza aid-blocking group);
   Australia places restrictions on Israeli settlers and entities the
   same day.
4. **Quad talks open in Manila** — Trump holds Quad talks in Manila ahead
   of his China visit; Modi speaks at the ASEAN-India summit and East Asia
   Summit; Canada and China extend trade deals as Xi meets Carney ahead
   of APEC.

## What it does

`main.py` is a dependency-free Python 3 program: it copies `entry.png`
(the artwork beside it) to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`
when set). No network, no randomness: run it twice and both runs write
identical bytes.

`build_image.py` is the Pillow script that drew the artwork (flat shapes,
3x supersampling down to 1024x1024, two craft revisions after preview
checks at full size and at 300 px). It is kept for reference; the
submitted program is `main.py`.

## Run it

```sh
python3 main.py
# writes /output/entry.png (1024x1024 PNG)
```

## Validation

Local runs (twice, fresh output dirs) wrote identical bytes:
`entry.png`, 1024x1024, 263,286 bytes,
SHA-256 `ac93c156c6ed2ed0de900e4d2f1cf829a43ab22928db823107c33facf4e8719c`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=nrw7bbqr&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
