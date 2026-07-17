#!/usr/bin/env python3
"""Photo -> ASCII portrait for the profile SVG (24 rows x <=43 cols),
plus a PNG preview renderer so likeness can be checked visually.

usage: ascii_convert.py <photo> [crop_l crop_t crop_r crop_b] [gamma] [invert01]
Char cell is ~8.8x20px, so sampling corrects for the 2.27 aspect.
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter

COLS, ROWS = 38, 24  # 38*9.6px (Menlo fallback) + 15px margin stays left of the x=390 info column
CELL_W, CELL_H = 8.8, 20.0
# dark -> light glyph ramp (Andrew6rant-ish texture)
RAMP = '@@%#MNHgmwpbkhaoejix|(;:,. '

def to_ascii(path, crop=None, gamma=1.0, invert=False):
    img = Image.open(path).convert('L')
    if crop:
        img = img.crop(crop)
    img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=120))
    # levels from person pixels only (background is pure white after segmentation)
    person = sorted(p for p in img.getdata() if p < 245)
    lo = person[int(len(person) * 0.04)]
    hi = person[int(len(person) * 0.92)]
    # resample honoring char cell aspect
    img = img.resize((COLS, ROWS), Image.LANCZOS)
    px = img.load()
    lines = []
    for r in range(ROWS):
        line = ''
        for c in range(COLS):
            raw = px[c, r]
            if raw >= 245:
                v = 1.0  # background stays empty
            else:
                v = min(1.0, max(0.0, (raw - lo) / max(1, hi - lo)))
                # S-curve: crush darks (hair, lenses), lift skin midtones
                if v < 0.35:
                    v = v * 0.5
                else:
                    v = 0.175 + 0.825 * ((v - 0.35) / 0.65) ** gamma
                v = min(v, 0.96)  # person pixels never vanish entirely
            if invert:
                v = 1.0 - v
            idx = min(len(RAMP) - 1, int(v * len(RAMP)))
            line += RAMP[idx]
        lines.append(line.rstrip())
    return lines

def render_preview(lines, out_png, dark=True):
    fg, bg = ('#c9d1d9', '#161b22') if dark else ('#24292f', '#f6f8fa')
    W, H = int(COLS * 9.7) + 30, ROWS * int(CELL_H) + 30  # Menlo 16px advance ~9.6px
    img = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 16)
    except OSError:
        font = ImageFont.load_default()
    for i, line in enumerate(lines):
        d.text((15, 10 + i * int(CELL_H)), line, fill=fg, font=font)
    img.save(out_png)

if __name__ == '__main__':
    photo = sys.argv[1]
    crop = None
    if len(sys.argv) >= 6:
        crop = tuple(int(x) for x in sys.argv[2:6])
    gamma = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
    lines = to_ascii(photo, crop, gamma)
    with open('ascii_art.txt', 'w') as f:
        f.write('\n'.join(lines))
    render_preview(lines, 'ascii_preview_dark.png', dark=True)
    render_preview(lines, 'ascii_preview_light.png', dark=False)
    print('\n'.join(lines))