#!/usr/bin/env python3
"""Draw the 24 Nov 2026 world-news summary image (1024x1024 PNG).

Flat editorial front-page style, drawn with PIL so every word is crisp.
Stories verified against Reuters / AP / CNN / Al Jazeera / SCMP reporting
of 22-24 November 2026 (see README for sources).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
NAVY2 = (28, 48, 88)
AMBER = (232, 163, 23)
RED = (178, 34, 34)
GREEN = (30, 122, 52)
NVGREEN = (118, 185, 0)
TEAL = (14, 110, 110)
PURPLE = (88, 44, 130)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (200, 192, 175)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def rrect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ------------------------------------------------------------
d.rectangle([0, 0, W, 148], fill=NAVY)
d.rectangle([0, 148, W, 154], fill=AMBER)
d.text((28, 22), "THE WORLD IN ONE IMAGE", font=font(SERIF_B, 56), fill=WHITE)
d.text((28, 96), "TUESDAY,  24  NOVEMBER  2026", font=font(SANS_B, 30), fill=AMBER)
d.text((700, 100), "5 STORIES  \u00b7  ONE DAY", font=font(SANS_B, 24), fill=(200, 210, 230))
d.text((28, 164), "The day's most consequential news \u2014 in five stories.",
       font=font(SANS, 23), fill=INK)

# ---- lead story: COP31 ---------------------------------------------------
LX, LY, LW, LH = 28, 196, 968, 268
rrect(d, [LX, LY, LX + LW, LY + LH], 10, fill=CARD, outline=LINE, width=2)
# visual: cracked earth + sun, right side
VX, VY, VW, VH = LX + LW - 300, LY + 12, 288, LH - 24
d.rectangle([VX, VY, VX + VW, VY + VH], fill=(250, 232, 200))
d.ellipse([VX + 96, VY + 18, VX + 192, VY + 114], fill=(235, 120, 40))
for ang in range(0, 360, 30):
    import math
    x0 = VX + 144 + int(56 * math.cos(math.radians(ang)))
    y0 = VY + 66 + int(56 * math.sin(math.radians(ang)))
    x1 = VX + 144 + int(70 * math.cos(math.radians(ang)))
    y1 = VY + 66 + int(70 * math.sin(math.radians(ang)))
    d.line([x0, y0, x1, y1], fill=(235, 120, 40), width=6)
d.rectangle([VX, VY + 150, VX + VW, VY + VH], fill=(146, 96, 48))
d.line([VX + 20, VY + 170, VX + 90, VY + 205, VX + 150, VY + 178, VX + 220, VY + 215, VX + 270, VY + 190],
       fill=(90, 55, 20), width=5)
d.line([VX + 90, VY + 205, VX + 110, VY + 232], fill=(90, 55, 20), width=4)
d.line([VX + 150, VY + 178, VX + 140, VY + 150], fill=(90, 55, 20), width=4)
d.text((VX + 14, VY + VH - 34), "NO DEAL", font=font(SANS_B, 26), fill=(255, 240, 210))

TX = LX + 24
d.text((TX, LY + 18), "CLIMATE  \u00b7  ANTALYA, TURKEY", font=font(SANS_B, 22), fill=RED)
d.text((TX, LY + 48), "CLIMATE TALKS", font=font(SERIF_B, 48), fill=INK)
d.text((TX, LY + 100), "COLLAPSE", font=font(SERIF_B, 48), fill=INK)
text_block(d, TX, LY + 162,
           "COP31 ends with no deal \u2014 the final draft never even mentioned fossil fuels. "
           "The EU and 90+ nations rejected it, after the longest summit on record.",
           font(SANS, 22), INK, 620, 28)

# ---- four panels ---------------------------------------------------------
PX, PY, PW, PH, GAP = 28, 480, 478, 236, 12


def panel(x, y, accent, kicker, headline, deck, draw_visual):
    rrect(d, [x, y, x + PW, y + PH], 10, fill=CARD, outline=LINE, width=2)
    d.rectangle([x, y, x + PW, y + 78], fill=accent)
    d.rounded_rectangle([x, y, x + PW, y + 78], radius=10, fill=accent)
    d.rectangle([x, y + 50, x + PW, y + 78], fill=accent)
    draw_visual(x, y)
    d.text((x + 16, y + 90), kicker, font=font(SANS_B, 19), fill=accent)
    d.text((x + 16, y + 114), headline, font=font(SANS_B, 29), fill=INK)
    text_block(d, x + 16, y + 150, deck, font(SANS, 19), (60, 60, 60), PW - 32, 24)


def vis_chip(x, y):
    # green chip on dark green band
    d.rounded_rectangle([x + 330, y + 12, x + 410, y + 66], radius=8, fill=(20, 60, 20), outline=NVGREEN, width=3)
    d.rectangle([x + 356, y + 28, x + 384, y + 50], fill=NVGREEN)
    for px in (336, 352, 368, 384, 400):
        d.line([px, y + 4, px, y + 12], fill=NVGREEN, width=3)
        d.line([px, y + 66, px, y + 74], fill=NVGREEN, width=3)
    d.text((x + 16, y + 18), "+30%", font=font(SANS_B, 44), fill=WHITE)


def vis_ship(x, y):
    # sea + warship + blast
    d.rectangle([x, y + 44, x + PW, y + 78], fill=(38, 84, 124))
    d.polygon([(x + 300, y + 44), (x + 332, y + 16), (x + 346, y + 44)], fill=(200, 200, 200))
    d.rectangle([x + 300, y + 44, x + 420, y + 62], fill=(120, 120, 120))
    d.rectangle([x + 372, y + 28, x + 380, y + 44], fill=(120, 120, 120))
    for dx, dy in [(0, 0), (13, -8), (-11, -9), (9, 9), (-13, 5)]:
        d.ellipse([x + 432 + dx - 9, y + 30 + dy - 9, x + 432 + dx + 9, y + 30 + dy + 9],
                  fill=(255, 170, 0))
    d.text((x + 16, y + 18), "BENGHAZI", font=font(SANS_B, 30), fill=WHITE)


def vis_space(x, y):
    # satellite + orbit
    for sx, sy in [(60, 20), (150, 52), (240, 16), (300, 60), (420, 24)]:
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=WHITE)
    d.ellipse([x + 330, y + 2, x + 470, y + 76], outline=(150, 180, 220), width=3)
    d.rectangle([x + 380, y + 30, x + 420, y + 48], fill=(180, 190, 205))
    d.rectangle([x + 352, y + 34, x + 380, y + 44], fill=(90, 140, 200))
    d.rectangle([x + 420, y + 34, x + 448, y + 44], fill=(90, 140, 200))
    d.ellipse([x + 392, y + 8, x + 408, y + 24], fill=RED)
    d.text((x + 16, y + 18), "ORBIT", font=font(SANS_B, 30), fill=WHITE)


def vis_gavel(x, y):
    # phone + red ban
    d.rounded_rectangle([x + 350, y + 10, x + 420, y + 68], radius=8, outline=WHITE, width=4)
    d.line([x + 372, y + 22, x + 398, y + 22], fill=WHITE, width=3)
    d.ellipse([x + 352, y + 12, x + 418, y + 66], outline=(255, 70, 70), width=6)
    d.line([x + 356, y + 16, x + 414, y + 62], fill=(255, 70, 70), width=6)
    d.text((x + 16, y + 18), "COURT", font=font(SANS_B, 30), fill=WHITE)


panel(PX, PY, GREEN, "TECH  \u00b7  SILICON VALLEY",
      "HUANG IS BACK",
      "Nvidia's board reinstates Jensen Huang as CEO, 11 days after he quit. "
      "Shares soar ~30% \u2014 nearly $1 trillion regained in a day.", vis_chip)

panel(PX + PW + GAP, PY, NAVY2, "WAR  \u00b7  LIBYA",
      "WARSHIP SUNK AT SEA",
      "Ukraine says sea drones sank Russia's corvette Merkury at Benghazi and hit "
      "cargo ship Angara \u2014 the war reaches the Med.", vis_ship)

panel(PX, PY + PH + GAP, (16, 24, 48), "SECURITY  \u00b7  NATO",
      "SPACE IS ON THE LINE",
      "Reports say Russia may launch a nuclear-armed satellite. NATO chief Rutte: "
      "the defence pledge covers space.", vis_space)

panel(PX + PW + GAP, PY + PH + GAP, PURPLE, "AI & LAW  \u00b7  USA",
      "MUSK SUED OVER GROK",
      "Virginia and Oregon sue SpaceX over Grok's \u201cspicy mode\u201d, which made "
      "non-consensual sexual images \u2014 20,000+ images of children.", vis_gavel)

# ---- footer --------------------------------------------------------------
d.rectangle([0, 968, W, H], fill=NAVY)
d.text((28, 980), "Why it matters: no climate plan \u00b7 chip king restored \u00b7 war at sea \u00b7 space on edge \u00b7 AI on trial",
       font=font(SANS_B, 17), fill=WHITE)
d.text((28, 1004), "Reported 24 Nov 2026  \u00b7  Sources: Reuters, AP, CNN, Al Jazeera, SCMP",
       font=font(SANS, 15), fill=(170, 180, 200))

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
