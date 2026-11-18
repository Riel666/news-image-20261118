#!/usr/bin/env python3
"""Draw the news-image-20261118 artwork: a one-page newspaper front page
summing up Wednesday 18 November 2026 in four stories.

Stories (all first reported / developed on 18 Nov 2026, sources: BBC,
Reuters, AP, The Guardian):
  1. Iran attacks a US military radar system in Bahrain with drones;
     Bahrain issues an all-clear after the overnight warning; Kuwait's
     army reports drone interceptions.
  2. Nvidia reports quarterly revenue $115.84bn, up 103% year on year, in
     its first earnings since Jensen Huang's exit; the board chairman says
     the company will not reinstate Huang; Trump backs calls for his return.
  3. Britain sanctions eight Israeli firms over West Bank settlements
     (plus a Gaza aid-blocking group); Australia places restrictions on
     Israeli settlers and entities the same day.
  4. Trump holds Quad talks in Manila ahead of his China visit; Modi
     speaks at the ASEAN-India summit and East Asia Summit; Canada and
     China extend trade deals as Xi meets Carney ahead of APEC.

Drawn flat at 3x supersampling (3072x3072) and downscaled to 1024x1024.
Run: python3 build_image.py  ->  writes entry.png next to this script.
"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 3  # supersampling factor
W, H = 1024, 1024

PAPER = (246, 241, 227)
NAVY = (22, 35, 63)
NAVY_LIGHT = (46, 64, 87)
GOLD = (217, 164, 65)
INK = (30, 30, 34)
GREY = (90, 100, 114)
WHITE = (255, 255, 255)
RED = (176, 58, 46)
TEAL = (23, 126, 118)
TEAL_DARK = (16, 90, 86)
SKY_PALE = (207, 232, 228)
GREEN = (118, 185, 0)
GREEN_DARK = (30, 122, 52)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * S)


def X(v):
    return v * S


def box(d, x0, y0, x1, y1, fill):
    d.rectangle([X(x0), X(y0), X(x1), X(y1)], fill=fill)


def rbox(d, x0, y0, x1, y1, r, fill):
    d.rounded_rectangle([X(x0), X(y0), X(x1), X(y1)], radius=X(r), fill=fill)


def poly(d, pts, fill):
    d.polygon([(X(x), X(y)) for x, y in pts], fill=fill)


def line(d, pts, fill, width=1):
    d.line([(X(x), X(y)) for x, y in pts], fill=fill, width=X(width))


def ell(d, x0, y0, x1, y1, fill):
    d.ellipse([X(x0), X(y0), X(x1), X(y1)], fill=fill)


def text(d, x, y, s, f, fill, anchor="la"):
    d.text((X(x), X(y)), s, font=f, fill=fill, anchor=anchor)


def draw_tracked(d, cx, y, s, path, size, fill, tracking=3):
    """Centred text with letter-spacing (tracking in 1024-space px)."""
    f = font(path, size)
    widths = [d.textlength(ch, font=f) // S for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, w in zip(s, widths):
        d.text((X(x), X(y)), ch, font=f, fill=fill)
        x += w + tracking


def wrap(d, s, path, size, max_w):
    """Greedy word wrap; returns list of lines fitting max_w (1024-space)."""
    f = font(path, size)
    words = s.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) / S <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star(cx, cy, r_out, r_in, fill, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
box(d, 0, 0, W, 132, NAVY)
draw_tracked(d, W // 2, 22, "THE WORLD IN ONE PICTURE", FONT_BOLD, 25, GOLD, tracking=6)
f_date = font(FONT_BOLD, 54)
d.text((X(W // 2), X(56)), "WEDNESDAY 18 NOVEMBER 2026", font=f_date, fill=WHITE, anchor="ma")
box(d, 0, 128, W, 132, GOLD)

# ---------------------------------------------------------------- kicker
draw_tracked(d, W // 2, 146, "FOUR STORIES THAT DEFINED THE DAY", FONT_BOLD, 24, NAVY, tracking=4)

# ---------------------------------------------------------------- panels
PANELS = [
    # (x, y, headline, sub, draw_fn)
    (28, 188, "IRAN DRONES HIT US RADAR",
     "Bahrain all-clear after overnight alert; Kuwait downs drones"),
    (528, 188, "NVIDIA DOUBLES REVENUE",
     "Revenue $115.84bn, up 103%; board will not reinstate Huang"),
    (28, 568, "UK SANCTIONS SETTLEMENT FIRMS",
     "Eight Israeli firms hit over West Bank settlements; Australia acts"),
    (528, 568, "QUAD TALKS OPEN IN MANILA",
     "Trump meets Quad leaders ahead of China visit; Modi at ASEAN summits"),
]
PW, PH, ILL_H = 468, 360, 200


def drone(d, cx, cy, scale=1.0):
    """Small quadcopter silhouette with a red blinking light."""
    bw, bh = 16 * scale, 7 * scale
    box(d, cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2, INK)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax, ay = cx + sx * 13 * scale, cy + sy * 8 * scale
            line(d, [(cx + sx * 6 * scale, cy + sy * 3 * scale), (ax, ay)], INK, 2)
            ell(d, ax - 7 * scale, ay - 2 * scale, ax + 7 * scale, ay + 2 * scale, (90, 92, 96))
    ell(d, cx - 3, cy + bh / 2 + 2, cx + 3, cy + bh / 2 + 8, (222, 41, 16))


def draw_radar(d, x0, y0):
    # night sky over the Gulf, stars, dark sea, sandy strip with the dome
    box(d, x0, y0, x0 + PW, y0 + 130, (16, 26, 54))
    for sx, sy, r in [(40, 24, 2), (120, 44, 2), (210, 18, 3), (300, 30, 2),
                      (380, 52, 2), (440, 20, 2), (70, 80, 2), (250, 70, 2),
                      (420, 90, 3), (330, 12, 2), (160, 100, 2)]:
        ell(d, x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r, (200, 205, 220))
    box(d, x0, y0 + 130, x0 + PW, y0 + ILL_H, (18, 64, 86))
    # wave lines on the sea
    for wy in (150, 172, 192):
        for wx in range(0, PW, 52):
            d.arc([X(x0 + wx), X(y0 + wy), X(x0 + wx + 40), X(y0 + wy + 18)],
                  start=180, end=360, fill=(120, 170, 185), width=X(3))
    # sandy strip holding the radar station, left side
    box(d, x0, y0 + 150, x0 + 220, y0 + ILL_H, (206, 188, 152))
    # radar sweep arcs from the dome
    cx, cy = x0 + 110, y0 + 128
    for r in (58, 92):
        d.arc([X(cx - r), X(cy - r), X(cx + r), X(cy + r)], start=200, end=340,
              fill=(120, 220, 180), width=X(3))
    line(d, [(cx, cy), (cx + 64, cy - 52)], (140, 235, 195), 3)
    # dome: grey base + white hemisphere (half-ellipse, base at y0+150)
    box(d, x0 + 72, y0 + 148, x0 + 148, y0 + 166, (90, 92, 96))
    ell(d, x0 + 76, y0 + 112, x0 + 144, y0 + 150, WHITE)
    d.arc([X(x0 + 76), X(y0 + 112), X(x0 + 144), X(y0 + 150)], start=180, end=360,
          fill=(180, 184, 190), width=X(3))
    # interception burst, upper right
    bx, by = x0 + 330, y0 + 58
    ell(d, bx - 22, by - 22, bx + 22, by + 22, (255, 176, 66))
    ell(d, bx - 12, by - 12, bx + 12, by + 12, (255, 224, 150))
    poly(d, star(bx, by, 26, 10, (255, 140, 0)), (255, 140, 0))
    # three drones approaching, with motion trails
    for (dx, dy, sc) in [(268, 92, 1.0), (392, 96, 0.9), (300, 40, 0.8)]:
        line(d, [(x0 + dx - 46 * sc, y0 + dy + 14 * sc), (x0 + dx - 18 * sc, y0 + dy + 4 * sc)],
             (150, 160, 175), 3)
        drone(d, x0 + dx, y0 + dy, sc)


def draw_chip(d, x0, y0):
    box(d, x0, y0, x0 + PW, y0 + ILL_H, (234, 245, 233))
    # rising chart line behind the chip
    pts = [(x0 + 24, y0 + 176), (x0 + 96, y0 + 148), (x0 + 150, y0 + 160),
           (x0 + 220, y0 + 122), (x0 + 300, y0 + 132), (x0 + 372, y0 + 96),
           (x0 + 424, y0 + 66)]
    line(d, pts, GREEN_DARK, 7)
    poly(d, [(x0 + 424, y0 + 66), (x0 + 400, y0 + 62), (x0 + 416, y0 + 86)], GREEN_DARK)
    # chip with pins (kept left of the tag)
    cx0, cy0, cx1, cy1 = x0 + 150, y0 + 42, x0 + 282, y0 + 174
    for i in range(5):
        px = cx0 + 18 + i * 24
        box(d, px, cy0 - 16, px + 12, cy0, GREEN_DARK)
        box(d, px, cy1, px + 12, cy1 + 16, GREEN_DARK)
    for i in range(5):
        py = cy0 + 18 + i * 24
        box(d, cx0 - 16, py, cx0, py + 12, GREEN_DARK)
        box(d, cx1, py, cx1 + 16, py + 12, GREEN_DARK)
    rbox(d, cx0, cy0, cx1, cy1, 12, GREEN)
    rbox(d, cx0 + 26, cy0 + 26, cx1 - 26, cy1 - 26, 8, (90, 150, 20))
    f_nv = font(FONT_BOLD, 34)
    d.text((X((cx0 + cx1) // 2), X((cy0 + cy1) // 2 - 6)), "NVDA",
           font=f_nv, fill=WHITE, anchor="ma")
    # tag, top-right, clear of the chart arrow
    rbox(d, x0 + 300, y0 + 14, x0 + 460, y0 + 48, 8, GREEN_DARK)
    f_up = font(FONT_BOLD, 18)
    d.text((X(x0 + 380), X(y0 + 19)), "+103% REVENUE", font=f_up, fill=WHITE, anchor="ma")


def draw_sanctions(d, x0, y0):
    box(d, x0, y0, x0 + PW, y0 + ILL_H, (233, 229, 216))
    # sanction document, left, with folded corner
    box(d, x0 + 36, y0 + 18, x0 + 296, y0 + 182, WHITE)
    d.rectangle([X(x0 + 36), X(y0 + 18), X(x0 + 296), X(y0 + 182)], outline=(160, 160, 155), width=X(2))
    poly(d, [(x0 + 266, y0 + 18), (x0 + 296, y0 + 48), (x0 + 296, y0 + 18)], (200, 200, 195))
    # lines of text on the document
    for i, (lw, ly) in enumerate([(200, 44), (220, 62), (180, 80), (210, 98), (150, 116)]):
        box(d, x0 + 56, y0 + ly, x0 + 56 + lw, y0 + ly + 7, (150, 155, 165))
    # red wax seal, bottom-left of the document
    sx, sy = x0 + 86, y0 + 150
    ell(d, sx - 17, sy - 17, sx + 17, sy + 17, RED)
    ell(d, sx - 11, sy - 11, sx + 11, sy + 11, (200, 80, 66))
    poly(d, star(sx, sy, 8, 3.5, WHITE), WHITE)
    # red SANCTIONED stamp across the document, bottom-right
    d.rounded_rectangle([X(x0 + 122), X(y0 + 136), X(x0 + 280), X(y0 + 170)],
                        radius=X(6), outline=RED, width=X(3))
    f_st = font(FONT_BOLD, 20)
    d.text((X(x0 + 201), X(y0 + 141)), "SANCTIONED", font=f_st, fill=RED, anchor="ma")
    # gavel, right side: handle diagonal, head joined to its top end
    line(d, [(x0 + 330, y0 + 176), (x0 + 404, y0 + 92)], (122, 84, 52), 9)
    # gavel head: one rotated block centred on the handle's top end
    hx, hy = x0 + 400, y0 + 88
    poly(d, [(hx - 36, hy - 2), (hx - 10, hy - 38), (hx + 36, hy - 10),
             (hx + 10, hy + 26)], (150, 104, 62))
    line(d, [(hx - 24, hy - 18), (hx + 22, hy + 10)], (122, 84, 52), 3)
    # sound block under the gavel
    ell(d, x0 + 312, y0 + 172, x0 + 348, y0 + 188, (150, 104, 62))


def draw_quad(d, x0, y0):
    box(d, x0, y0, x0 + PW, y0 + ILL_H, (220, 233, 245))
    box(d, x0, y0 + 178, x0 + PW, y0 + ILL_H, (232, 220, 192))
    # flag poles
    for px in (14, 128, 242, 356):
        line(d, [(x0 + px, y0 + 26), (x0 + px, y0 + 178)], (60, 60, 66), 4)
        ell(d, x0 + px - 5, y0 + 18, x0 + px + 5, y0 + 28, GOLD)
    # US flag
    fx, fy = x0 + 18, y0 + 30
    for i in range(7):
        box(d, fx, fy + i * 9, fx + 96, fy + i * 9 + 9,
            RED if i % 2 == 0 else WHITE)
    box(d, fx, fy, fx + 40, fy + 36, (30, 50, 110))
    for r in range(3):
        for c in range(4):
            ell(d, fx + 5 + c * 9, fy + 5 + r * 11, fx + 10 + c * 9, fy + 10 + r * 11, WHITE)
    # India flag
    fx = x0 + 132
    box(d, fx, fy, fx + 96, fy + 21, (255, 153, 51))
    box(d, fx, fy + 21, fx + 96, fy + 42, WHITE)
    box(d, fx, fy + 42, fx + 96, fy + 63, (19, 136, 8))
    ccx, ccy = fx + 48, fy + 31
    d.ellipse([X(ccx - 10), X(ccy - 10), X(ccx + 10), X(ccy + 10)],
              outline=(0, 0, 128), width=X(2))
    for k in range(8):
        a = math.radians(k * 45)
        line(d, [(ccx + 3 * math.cos(a), ccy + 3 * math.sin(a)),
                 (ccx + 9 * math.cos(a), ccy + 9 * math.sin(a))], (0, 0, 128), 1)
    # Japan flag
    fx = x0 + 246
    box(d, fx, fy, fx + 96, fy + 63, WHITE)
    ell(d, fx + 48 - 14, fy + 31 - 14, fx + 48 + 14, fy + 31 + 14, (188, 0, 45))
    # Australia flag
    fx = x0 + 360
    box(d, fx, fy, fx + 96, fy + 63, (0, 40, 120))
    # simplified Union Jack canton
    box(d, fx, fy, fx + 48, fy + 31, (0, 0, 90))
    line(d, [(fx, fy), (fx + 48, fy + 31)], WHITE, 3)
    line(d, [(fx + 48, fy), (fx, fy + 31)], WHITE, 3)
    line(d, [(fx + 24, fy), (fx + 24, fy + 31)], (200, 0, 0), 5)
    line(d, [(fx, fy + 15), (fx + 48, fy + 15)], (200, 0, 0), 5)
    # seven-point star below the canton + two Southern Cross stars
    poly(d, star(fx + 24, fy + 47, 10, 4, WHITE), WHITE)
    for sx, sy in [(70, 44), (84, 56)]:
        poly(d, star(fx + sx, fy + sy, 6, 2.5, WHITE), WHITE)
    # airplane silhouette: slim fuselage, tail fin, swept wing
    ax, ay = x0 + 150, y0 + 128
    ell(d, ax, ay - 7, ax + 130, ay + 7, NAVY)
    poly(d, [(ax + 6, ay - 5), (ax + 22, ay - 26), (ax + 34, ay - 24),
             (ax + 30, ay - 5)], NAVY)
    poly(d, [(ax + 52, ay + 4), (ax + 78, ay + 24), (ax + 92, ay + 22),
             (ax + 76, ay + 4)], NAVY)
    for lx in (52, 96, 140):
        line(d, [(x0 + lx, y0 + 128), (x0 + lx + 30, y0 + 128)], (150, 160, 175), 3)


DRAW = [draw_radar, draw_chip, draw_sanctions, draw_quad]

for (px, py, headline, sub), draw_fn in zip(PANELS, DRAW):
    box(d, px, py, px + PW, py + PH, WHITE)
    d.rectangle([X(px), X(py), X(px + PW), X(py + PH)], outline=NAVY, width=X(2))
    draw_fn(d, px + 2, py + 2)
    # headline + sub (panel interior is 360 tall: illustration 200,
    # up to 2 headline lines + up to 2 sub lines must fit below it)
    f_head = font(FONT_BOLD, 36)
    head_lines = wrap(d, headline, FONT_BOLD, 36, PW - 36)
    hy = py + ILL_H + 14
    for ln in head_lines:
        d.text((X(px + 18), X(hy)), ln, font=f_head, fill=NAVY)
        hy += 40
    f_sub = font(FONT_REG, 22)
    for ln in wrap(d, sub, FONT_REG, 22, PW - 36):
        d.text((X(px + 18), X(hy + 4)), ln, font=f_sub, fill=GREY)
        hy += 27

# ---------------------------------------------------------------- footer
f_src = font(FONT_REG, 21)
d.text((X(W // 2), X(952)), "Sources: BBC \u00b7 Reuters \u00b7 AP \u00b7 The Guardian  \u2014  as reported on 18 November 2026",
       font=f_src, fill=GREY, anchor="ma")
box(d, 28, 940, W - 28, 942, (200, 190, 160))

out = img.resize((W, H), Image.LANCZOS)
out.save("entry.png", optimize=True)
print("wrote entry.png", out.size, len(open("entry.png", "rb").read()), "bytes")
