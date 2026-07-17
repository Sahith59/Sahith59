#!/usr/bin/env python3
"""Photo -> ASCII portrait for the profile SVG.

High-res grid: 74 cols x 56 rows rendered at 8px/9px line-height in the SVG
(74 * 4.8px Menlo advance + 15px margin stays left of the x=390 info column).

Emits two files:
  ascii_art_light.txt  ink mapping   (dark pixels -> dense glyphs)
  ascii_art_dark.txt   photographic  (bright pixels -> dense glyphs)
so both themes read as a positive image, never a negative.

usage: ascii_convert.py <photo> [crop_l crop_t crop_r crop_b] [gamma]
"""
import os
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
COLS, ROWS = 74, 56
# glyph ramp indexed by DENSITY (sparse -> dense)
RAMP = ' .,:;i|(xoeajhkbdpwmgUXHNM#%@@'

BG_THRESHOLD = 238  # segmentation leaves soft blended edges; treat near-white as background

def luminance_grid(path, crop=None, gamma=1.0):
    img = Image.open(path).convert('L')
    if crop:
        img = img.crop(crop)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=80))
    # gentle stretch from person pixels only; preserves the photo's tonal ordering
    person = sorted(p for p in img.getdata() if p < BG_THRESHOLD)
    lo = person[int(len(person) * 0.02)]
    hi = person[int(len(person) * 0.97)]
    img = img.resize((COLS, ROWS), Image.LANCZOS)
    px = img.load()
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            raw = px[c, r]
            if raw >= BG_THRESHOLD:
                row.append(None)  # background: always empty
                continue
            v = min(1.0, max(0.0, (raw - lo) / max(1, hi - lo))) ** gamma
            row.append(v)
        grid.append(row)
    return grid

# dark mode lifts midtones so shaded skin stays visible on a dark card;
# build_svgs.py applies the same constant to the shade levels
DARK_DISPLAY_GAMMA = 0.55

def to_glyphs(grid, photographic):
    lines = []
    for row in grid:
        line = ''
        for v in row:
            if v is None:
                line += ' '
                continue
            density = v ** DARK_DISPLAY_GAMMA if photographic else 1.0 - v
            density = max(density, 0.05)  # person pixels never vanish entirely
            idx = min(len(RAMP) - 1, int(density * len(RAMP)))
            line += RAMP[idx]
        lines.append(line.rstrip())
    return lines

def render_preview(lines, out_png, dark):
    fg, bg = ('#e6edf3', '#0d1117') if dark else ('#1f2328', '#ffffff')
    # 2x scale for inspection (16px font, 18px line height)
    W, H = int(COLS * 9.7) + 30, ROWS * 18 + 30
    img = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 16)
    for i, line in enumerate(lines):
        d.text((15, 10 + i * 18), line, fill=fg, font=font)
    img.save(out_png)

if __name__ == '__main__':
    import json
    photo = sys.argv[1]
    crop = tuple(int(x) for x in sys.argv[2:6]) if len(sys.argv) >= 6 else None
    gamma = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
    grid = luminance_grid(photo, crop, gamma)
    # shade map: per-cell raw luminance in 0..255 (null = background);
    # build_svgs.py quantizes per theme (dark applies DARK_DISPLAY_GAMMA)
    shades = [[None if v is None else int(v * 255) for v in row] for row in grid]
    with open(os.path.join(HERE, 'ascii_shade.json'), 'w') as f:
        json.dump(shades, f)
    for name, photographic, dark in (('light', False, False), ('dark', True, True)):
        lines = to_glyphs(grid, photographic)
        with open(os.path.join(HERE, f'ascii_art_{name}.txt'), 'w') as f:
            f.write('\n'.join(lines))
        render_preview(lines, os.path.join(HERE, f'ascii_preview_{name}.png'), dark)
    print('wrote ascii_art_{light,dark}.txt + ascii_shade.json + previews')