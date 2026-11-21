#!/usr/bin/env python3
"""THE WORLD IN ONE PAGE - Saturday 21 November 2026.

Renders a single-image newspaper front page (1024x1024 PNG) with PIL only.
Fully deterministic: no randomness, no timestamps, no network.
Running it writes entry.png next to this file, and also to
/output/entry.png when that directory exists.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants

W = H = 1024
MARGIN = 56
CW = W - 2 * MARGIN  # content width = 912

PAPER = (247, 243, 234)   # off-white paper #f7f3ea
INK = (22, 20, 18)        # near-black ink
RED = (139, 26, 26)       # deep red accent
BAND = (24, 22, 20)       # near-black date band
BAND_TEXT = (250, 248, 243)
GREY = (92, 86, 78)       # footer grey

FD = "/usr/share/fonts/truetype"
SERIF_BOLD = FD + "/liberation/LiberationSerif-Bold.ttf"
SANS = FD + "/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = FD + "/liberation/LiberationSans-Bold.ttf"
DATE_FONT = FD + "/dejavu/DejaVuSans-Bold.ttf"

# ------------------------------------------------------------------- stories

ANCHOR_LABEL = "EUROPE \u00b7 WAR"
ANCHOR_HEADLINE = ["RUSSIAN MISSILES", "HIT POLAND"]
ANCHOR_SUB = (
    "Missiles and a drone fell on Polish soil during the strike on Ukraine; "
    "Warsaw calls it a deliberate provocation, NATO a grave airspace violation."
)

STORIES = [
    (
        "THE HAGUE \u00b7 JUSTICE",
        "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
        "The ICJ rules Myanmar's forces committed genocide against the Rohingya.",
    ),
    (
        "SHENZHEN \u00b7 SUMMIT",
        "TRUMP, XI AND PUTIN MEET FACE TO FACE",
        "First trilateral summit ends with a joint peace declaration, few concrete results.",
    ),
    (
        "NEW YORK \u00b7 MARKETS",
        "WALL STREET SLIDES INTO CORRECTION",
        "AI and chip stocks plunge; the S&P 500 and Dow fall about 3.7%.",
    ),
    (
        "BRUSSELS \u00b7 EUROPE",
        "UK AND EU SIGN THREE NEW DEALS",
        "Food trade, carbon markets and youth mobility agreed at the Brussels summit.",
    ),
    (
        "HORMUZ \u00b7 CONFLICT",
        "IRAN WAR NEARS ITS NINTH MONTH",
        "Trump says he is in no rush on Iran and may not decide until 2027.",
    ),
]

FOOTER = "Saturday\u2019s world news at a glance \u2014 six stories, one page."

# ------------------------------------------------------------------- helpers


def font(path, size):
    return ImageFont.truetype(path, size)


def ink_h(draw, text, fnt):
    """Height of the ink box of a single line of text."""
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[3] - box[1]


def fit_font(draw, text, path, size, max_width, min_size=12):
    """Largest size <= size whose text width fits max_width."""
    s = size
    while s > min_size:
        f = font(path, s)
        if draw.textlength(text, font=f) <= max_width:
            return f
        s -= 2
    return font(path, min_size)


def tracked_width(draw, text, fnt, tracking):
    if not text:
        return 0
    return sum(draw.textlength(ch, font=fnt) for ch in text) + tracking * (len(text) - 1)


def draw_tracked(draw, x, y, text, fnt, fill, tracking, centre=False):
    """Draw letter-spaced text; x is the left edge, or the centre if centre."""
    if centre:
        x = x - tracked_width(draw, text, fnt, tracking) / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centred_lines(draw, cx, y, lines, fnt, fill, line_h):
    for line in lines:
        draw.text((cx, y), line, font=fnt, fill=fill, anchor="ma")
        y += line_h
    return y


# --------------------------------------------------------------------- build


def story_block_h(draw, story, label_f, head_f, sub_f):
    label, headline, sub = story
    h = ink_h(draw, label, label_f) + 5
    h += ink_h(draw, headline, head_f) + 6
    sub_lines = wrap(draw, sub, sub_f, CW)
    h += len(sub_lines) * (ink_h(draw, sub_lines[0], sub_f) + 4)
    return h


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    cx = W // 2

    # ---- masthead ------------------------------------------------------
    mast_f = font(SANS_BOLD, 27)
    draw_tracked(draw, cx, 44, "THE WORLD IN ONE PAGE", mast_f, INK, 6, centre=True)
    draw.line([(MARGIN, 88), (W - MARGIN, 88)], fill=INK, width=3)
    draw.line([(MARGIN, 94), (W - MARGIN, 94)], fill=INK, width=1)

    # ---- anchor story --------------------------------------------------
    label_f = font(SANS_BOLD, 21)
    draw_tracked(draw, cx, 114, ANCHOR_LABEL, label_f, RED, 3, centre=True)

    head_f = font(SERIF_BOLD, 80)
    y = draw_centred_lines(draw, cx, 142, ANCHOR_HEADLINE, head_f, INK, 90)

    sub_f = font(SANS, 23)
    sub_lines = wrap(draw, ANCHOR_SUB, sub_f, 880)
    y = draw_centred_lines(draw, cx, y + 14, sub_lines, sub_f, INK, 31)

    # small red accent rule between the anchor story and the date band
    draw.line([(cx - 60, 411), (cx + 60, 411)], fill=RED, width=3)

    # ---- date band (vertically centred, inside the central safe area) --
    band_y0, band_y1 = 427, 597
    draw.rectangle([(0, band_y0), (W, band_y1)], fill=BAND)

    sat_f = font(DATE_FONT, 30)
    date_f = fit_font(draw, "21 NOVEMBER 2026", DATE_FONT, 96, CW - 32)
    sat_h = ink_h(draw, "SATURDAY", sat_f)
    date_h = ink_h(draw, "21 NOVEMBER 2026", date_f)
    group_h = sat_h + 12 + date_h
    gy = band_y0 + (band_y1 - band_y0 - group_h) // 2
    draw_tracked(draw, cx, gy, "SATURDAY", sat_f, BAND_TEXT, 12, centre=True)
    draw.text((cx, gy + sat_h + 12), "21 NOVEMBER 2026",
              font=date_f, fill=BAND_TEXT, anchor="ma")

    # ---- supporting stories --------------------------------------------
    stories_top = 610
    stories_bottom = 958
    head_size, sub_size = 28, 17
    while True:
        s_label_f = font(SANS_BOLD, 17)
        s_head_base = head_size
        s_sub_f = font(SANS, sub_size)
        total = 0
        head_fonts = []
        for story in STORIES:
            hf = fit_font(draw, story[1], SERIF_BOLD, s_head_base, CW)
            head_fonts.append(hf)
            total += story_block_h(draw, story, s_label_f, hf, s_sub_f) + 9
        total -= 9  # no rule after the last story
        if total <= stories_bottom - stories_top or head_size <= 22:
            break
        head_size -= 1

    y = stories_top
    for i, story in enumerate(STORIES):
        label, headline, sub = story
        draw_tracked(draw, MARGIN, y, label, s_label_f, RED, 2)
        y += ink_h(draw, label, s_label_f) + 5
        draw.text((MARGIN, y), headline, font=head_fonts[i], fill=INK)
        y += ink_h(draw, headline, head_fonts[i]) + 6
        for line in wrap(draw, sub, s_sub_f, CW):
            draw.text((MARGIN, y), line, font=s_sub_f, fill=INK)
            y += ink_h(draw, line, s_sub_f) + 4
        if i < len(STORIES) - 1:
            y += 5
            draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=1)
            y += 4

    # ---- footer ----------------------------------------------------------
    foot_f = font(SANS, 15)
    draw.text((cx, 965), FOOTER, font=foot_f, fill=GREY, anchor="ma")

    return img


def main():
    img = render()
    here = os.path.dirname(os.path.abspath(__file__))
    img.save(os.path.join(here, "entry.png"), optimize=True)
    if os.path.isdir("/output"):
        img.save("/output/entry.png", optimize=True)


if __name__ == "__main__":
    main()
