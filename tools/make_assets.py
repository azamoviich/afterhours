#!/usr/bin/env python3
"""Builds README/landing visuals from raw simulator screenshots.
Usage: python3 tools/make_assets.py <dir-with-m1..m4.png,b1..b4.png>"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC = sys.argv[1]
SERIF, SANS = '/System/Library/Fonts/NewYork.ttf', '/System/Library/Fonts/SFNS.ttf'
INK, PAPER, TOMATO = (26, 23, 20), (246, 243, 238), (255, 90, 54)

def font(path, size):
    return ImageFont.truetype(path, size)

def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *im.size), r, fill=255)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.paste(im, (0, 0), m); return out

def phone(path, w=420):
    shot = Image.open(path).convert('RGB'); h = int(shot.height * w / shot.width)
    shot = shot.resize((w, h), Image.LANCZOS); bez, r = 14, 58
    body = Image.new('RGBA', (w + bez * 2, h + bez * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(body)
    d.rounded_rectangle((0, 0, body.width - 1, body.height - 1), r + bez, fill=(28, 28, 30, 255))
    d.rounded_rectangle((2, 2, body.width - 3, body.height - 3), r + bez - 2, outline=(90, 90, 94, 255), width=2)
    body.alpha_composite(rounded(shot.convert('RGBA'), r), (bez, bez))
    pad = 60; canvas = Image.new('RGBA', (body.width + pad * 2, body.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new('L', canvas.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad + 10, pad + 30, pad + body.width - 10, pad + body.height + 10), r, fill=110)
    canvas.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(28)))
    canvas.alpha_composite(body, (pad, pad)); return canvas

framed = {}
for app, names in {'nudge': ['m1', 'm2', 'm3', 'm4'], 'benefit': ['b1', 'b2', 'b3', 'b4']}.items():
    framed[app] = [phone(f'{SRC}/{n}.png') for n in names]
    for i, f in enumerate(framed[app], 1):
        f.save(f'img/frames/{app}-{i}.png', optimize=True)

for app, bg in [('nudge', PAPER), ('benefit', (10, 10, 11))]:
    fs = framed[app]; W = sum(f.width for f in fs) - 140 * 3
    strip = Image.new('RGBA', (W, fs[0].height), bg + (255,)); x = 0
    for f in fs: strip.alpha_composite(f, (x, 0)); x += f.width - 140
    strip = strip.convert('RGB'); strip.thumbnail((1800, 1800)); strip.save(f'img/{app}-strip.jpg', quality=86)

# Banner / social preview 1280x640
W, H = 1280, 640
b = Image.new('RGB', (W, H), PAPER)
g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse((760, -280, 1520, 520), fill=130)
b = Image.composite(Image.new('RGB', (W, H), (255, 176, 146)), b, g.filter(ImageFilter.GaussianBlur(150)))
d = ImageDraw.Draw(b)
d.text((84, 96), 'APPS I BUILD AFTER HOURS', font=font(SANS, 20), fill=TOMATO)
d.text((76, 124), 'afterhours', font=font(SERIF, 128), fill=INK)
d.text((84, 300), 'Small, polished iOS apps', font=font(SANS, 32), fill=INK)
d.text((84, 342), 'made in my free time.', font=font(SANS, 32), fill=(130, 122, 114))
f = font(SANS, 24); label = 'Add to SideStore'; tw = d.textlength(label, font=f)
x0, y0, h = 84, 430, 64; w = int(tw) + 32 + 56 + 10
d.rounded_rectangle((x0, y0, x0 + w, y0 + h), h // 2, fill=INK)
d.text((x0 + 30, y0 + 18), label, font=f, fill=PAPER)
cx = x0 + w - 8 - 24; d.ellipse((cx - 24, y0 + 8, cx + 24, y0 + 56), fill=TOMATO)
d.line((cx - 7, y0 + 39, cx + 8, y0 + 24), fill='white', width=4); d.line((cx - 3, y0 + 24, cx + 8, y0 + 24), fill='white', width=4)
d.line((cx + 8, y0 + 24, cx + 8, y0 + 35), fill='white', width=4)
bb = b.convert('RGBA')
p2 = framed['benefit'][0].copy(); p2.thumbnail((320, 700)); p2 = p2.rotate(6, resample=Image.BICUBIC, expand=True)
p1 = framed['nudge'][0].copy(); p1.thumbnail((320, 700)); p1 = p1.rotate(-5, resample=Image.BICUBIC, expand=True)
bb.alpha_composite(p2, (930, 150)); bb.alpha_composite(p1, (740, 90))
for i, ic in enumerate(['img/nudge-icon.png', 'img/benefit-icon.png']):
    im = Image.open(ic).convert('RGBA').resize((60, 60), Image.LANCZOS); bb.alpha_composite(rounded(im, 14), (84 + i * 76, 544))
bb.convert('RGB').save('img/banner.png', optimize=True)
print('assets ok')
