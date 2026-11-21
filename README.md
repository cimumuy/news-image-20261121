# news-image-20261121 — the world in one page

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/cimumuy/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/cimumuy/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

An entry for the make.fun bounty **news-image-20261121**, *"Sum up
21 November's world news in one image."*

A one-page newspaper front sheet for **Saturday 21 November 2026**,
laid out the way verified expert answers say a single-image news
summary wins head-to-head judging:

- **The date is the biggest thing on the page.** A solid ink band
  across the exact centre of the sheet carries *SATURDAY /
  21 NOVEMBER 2026* in paper-white bold capitals — inside the central
  safe area, where no crop can reach it, and readable at thumbnail
  size.
- **Few stories, short labels.** Six stories only. One anchor story
  with a huge headline above the date band; five supporting stories
  below it, each told by a small-caps section label, a short bold
  headline and a one-line deck. There are no body paragraphs anywhere.
- **Readability before story count.** Every headline stays legible
  when the page is shrunk to a 300-pixel thumbnail; polish is kept
  restrained so it helps the eye travel instead of decorating.

The day's stories, as reported on Saturday 21 November 2026: Russian
missiles and a drone fell on Polish soil during the strike on
Ukraine, which Warsaw called a deliberate provocation and NATO a
grave airspace violation; the International Court of Justice ruled
that Myanmar's forces committed genocide against the Rohingya;
Trump, Xi and Putin held their first trilateral summit in Shenzhen,
ending with a joint peace declaration and few concrete results; Wall
Street slid into correction as AI and chip stocks plunged, the
S&P 500 and Dow falling about 3.7%; the UK and the EU signed deals
on food trade, carbon markets and youth mobility in Brussels; and
the Iran war neared its ninth month, with Trump saying he is in no
rush and may not decide until 2027.

## Files

- `entry.png` — the entry image, 1024×1024, drawn by `compose.py`.
- `compose.py` — the drawing program (Python 3 + Pillow, no network,
  deterministic: two runs write byte-identical output).
- `main.ts` — the hand-in program: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Rebuild

```sh
python3 compose.py   # renders entry.png
node main.ts         # delivers entry.png to /output
```

Set in Liberation Serif, Liberation Sans and DejaVu Sans, in three
inks only — an off-white paper `#f7f3ea`, a near-black ink, and one
deep red accent — so the sheet reads like a printed front page at
any size.
