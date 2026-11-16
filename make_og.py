#!/usr/bin/env python3
"""og.png 1200x630 — Yours and Mine Coffee (2x supersample, measured clearances).
Outside-to-inside sweep: inviting green into cozy dark red; hibiscus medallion right
(gold glow), cream serif wordmark left. Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
S = 2
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

PINE = (24, 51, 34); PINE2 = (30, 58, 40)
BRICK = (94, 24, 22); BRICK2 = (142, 35, 32)
CREAM = (247, 236, 218); GOLD = (232, 192, 122)
JAMAICA = (193, 68, 78); DULCE = (217, 154, 61)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

serif   = lambda s: font(["Georgia Bold.ttf", "Georgia Bold Italic.ttf", "Georgia-Bold-Italic.ttf", "Times New Roman Bold.ttf"], s*S)
serifit = lambda s: font(["Georgia Bold Italic.ttf", "Georgia-Bold-Italic.ttf", "Times New Roman Bold Italic.ttf"], s*S)
sans    = lambda s: font(["Avenir Next Bold.ttf", "AvenirNext-Bold.ttf", "HelveticaNeue-Bold.ttf", "Arial Bold.ttf"], s*S)
sansm   = lambda s: font(["Avenir Next Medium.ttf", "AvenirNext-Medium.ttf", "HelveticaNeue.ttc", "Arial.ttf"], s*S)

L = 80                       # left text margin
cx0 = 840                    # medallion center x — text must stay left of (cx0 - 190)
img = Image.new("RGB", (W*S, H*S), PINE)
d = ImageDraw.Draw(img, "RGBA")

# diagonal sweep: pine (outside green) -> brick (inside red)
import math
diag = math.hypot(W, H)
for y in range(H*S):
    for_x_frac = 0.0
    # two-stop gradient with a slight diagonal push via per-row + per-col blend band
    for x in range(0, W*S, 8):
        t = (x / (W*S)) * 0.55 + (y / (H*S)) * 0.45
        r = int(PINE2[0] + (BRICK2[0]-PINE2[0])*t); g = int(PINE2[1] + (BRICK2[1]-PINE2[1])*t); b = int(PINE2[2] + (BRICK2[2]-PINE2[2])*t)
        d.rectangle([x, y, x+7, y], fill=(r, g, b))

def P(x, y): return (x*S, y*S)

# ---- hibiscus medallion (right), gold glow behind ----
glow = Image.new("RGBA", (W*S, H*S), (0,0,0,0))
gd = ImageDraw.Draw(glow)
gd.ellipse([(cx0-210)*S, (315-210)*S, (cx0+210)*S, (315+210)*S], fill=(232,192,122,52))
glow = glow.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(90*S//2))
img.paste(glow, (0,0), glow)

mr = 172                     # medallion ring radius
d.ellipse([P(cx0-mr,315-mr), P(cx0+mr,315+mr)], outline=GOLD, width=5*S)
d.ellipse([P(cx0-140,315-140), P(cx0+140,315+140)], outline=(202,164,92,140), width=int(1.6*S))
# five hibiscus petals around center (cx0, 328), dist 74
cxm, cym = cx0, 328
for ang in (-90, -18, 54, 126, 198):
    a = math.radians(ang)
    px, py = cxm + 74*math.cos(a), cym + 74*math.sin(a)
    d.ellipse([P(px-48, py-48), P(px+48, py+48)], fill=JAMAICA)
d.ellipse([P(cxm-32, cym-32), P(cxm+32, cym+32)], fill=DULCE)
# stamen
d.line([P(cxm+8, cym-8), P(cxm+50, cym-108)], fill=CREAM, width=int(3.4*S))
d.ellipse([P(cxm+44, cym-114), P(cxm+56, cym-102)], fill=CREAM)

# ---- wordmark (left), measured to stay clear of the medallion ----
zone_right = cx0 - 185
size = 96
while True:
    f = serifit(size)
    w = f.getlength("Yours and Mine")
    if w/S <= zone_right - L or size <= 52: break
    size -= 2
y0 = 118
d.text((L, y0), "Yours and Mine", font=serifit(size), fill=CREAM)

f = sans(30)
d.text((L+4, y0 + size + 44), "C O F F E E", font=f, fill=GOLD)

f = sansm(21)
d.text((L+2, y0 + size + 100), "Latina-inspired flavors · Westport", font=f, fill=(237, 224, 200))
d.text((L+2, y0 + size + 132), "4112 Pennsylvania Ave · Kansas City, MO", font=f, fill=(216, 196, 165))

# golden rule under address
d.rectangle([L, y0 + size + 178, L+150, y0 + size + 182], fill=GOLD)

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes; wordmark size", size, "width", round(w/S,1), "zone_right", zone_right)
