#!/usr/bin/env python3
"""Generates dark_mode.svg + light_mode.svg for Sahith59/Sahith59.

Info column: bold monospace, values left-aligned at a fixed column (col 16
of a 60-char line). Dynamic stat fields carry ids that today.py rewrites
daily (stats keep dot-justified budgets so those lines stay width-stable).

Portrait: 74x64 glyph grid rendered at 8px from the files in this
directory, one glyph file per theme so both render as a photographic
positive, with a breathing arc-reactor glow behind the chest.

Motion (SMIL only — the sole animation tech GitHub READMEs allow):
  - HUD boot: rows reveal top-to-bottom with eased fades, settle static
  - typewriter quote with a cursor that blinks out
  - arc pulse beside the header + slow reactor glow
All animations use the values="0;0;1" keyTimes pattern with begin="0s" so
renderers without SMIL show the finished card instead of a blank one.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

LINE_WIDTH = 60
VALUE_COL = 16          # 0-indexed char column where every kv value starts
HEIGHT = 650            # 31 info rows: y=30..630 step 20
ROWS = list(range(30, 631, 20))

BOOT_START = 0.15       # s before the first row begins revealing
BOOT_STAGGER = 0.05     # s between consecutive rows
BOOT_FADE = 0.30        # s each row takes to fade in
TYPE_START = 2.1        # s when the quote starts typing
TYPE_CHAR = 0.045       # s per character

# Monochrome: grayscale everything, single gold accent
THEMES = {
    'dark_mode.svg': {
        'bg': '#0d1117', 'fg': '#e6edf3',
        'key': '#7d8590', 'value': '#e6edf3', 'cc': '#2d333b',
        'add': '#e3b341', 'del': '#7d8590', 'accent': '#e3b341',
        'quote': '#8b949e', 'glow_opacity': '0.30',
        'ascii_file': 'ascii_art_dark.txt',
        'display_gamma': 0.55,  # keep in sync with ascii_convert.DARK_DISPLAY_GAMMA
        # luminance level 0 (darkest) -> 7 (brightest) on a dark card
        'shades': ['#1c2128', '#2d333b', '#444c56', '#616e7f',
                   '#7d8590', '#9ea7b3', '#c9d1d9', '#f0f6fc'],
    },
    'light_mode.svg': {
        'bg': '#ffffff', 'fg': '#1f2328',
        'key': '#656d76', 'value': '#1f2328', 'cc': '#d0d7de',
        'add': '#9a6700', 'del': '#656d76', 'accent': '#9a6700',
        'quote': '#8b949e', 'glow_opacity': '0.14',
        'ascii_file': 'ascii_art_light.txt',
        'display_gamma': 1.0,
        # same level order: dark tones get dark ink on a white card
        'shades': ['#1f2328', '#30363d', '#484f58', '#656d76',
                   '#8b949e', '#afb8c1', '#c9d1d9', '#e6e9ec'],
    },
}

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def reveal_anim(delay, fade):
    """Safe delayed fade-in: hidden from t=0, eased fade at `delay`.
    Renderers without SMIL simply show the element (no static opacity=0)."""
    dur = delay + fade
    kt = round(delay / dur, 4)
    return (f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{kt};1" '
            f'calcMode="spline" keySplines="0 0 1 1;0.25 0.1 0.25 1" '
            f'dur="{round(dur, 3)}s" begin="0s" fill="freeze"/>')

def dots_str(just_len):
    """Mirror of today.py justify_format spacing rules (stats fields only)."""
    if just_len <= 2:
        return {0: '', 1: ' ', 2: '. '}[max(0, just_len)]
    return ' ' + '.' * just_len + ' '

def header(y, title):
    fill = LINE_WIDTH - len(title) - 1
    dashes = '-' + '—' * (fill - 4) + '-—-'
    return (f'<tspan x="390" y="{y}" class="accent">{esc(title)}</tspan>'
            f'<tspan class="cc"> {dashes}</tspan>'), LINE_WIDTH

def kv(y, key, value, value_id=None, value_class='value'):
    """'. Key: ... value' — value always starts at VALUE_COL."""
    n = VALUE_COL - 2 - len(key) - 1 - 2
    assert n >= 2, f'key too long at y={y}: {key}'
    assert len(value) <= LINE_WIDTH - VALUE_COL, f'value too long at y={y}: {value}'
    dots = ' ' + '.' * n + ' '
    id_val = f' id="{value_id}"' if value_id else ''
    line = (f'<tspan x="390" y="{y}" class="cc">. </tspan><tspan class="key">{esc(key)}</tspan>:'
            f'<tspan class="cc">{dots}</tspan>'
            f'<tspan class="{value_class}"{id_val}>{esc(value)}</tspan>')
    return line, VALUE_COL + len(value)

def blank(y):
    return f'<tspan x="390" y="{y}" class="cc">. </tspan>', 2

def typewriter(y, text):
    """Per-character reveal + cursor that blinks four times, then fades out."""
    assert len(text) + 1 <= LINE_WIDTH, f'quote too long: {len(text)}'
    parts = []
    for i, ch in enumerate(text):
        at = TYPE_START + i * TYPE_CHAR
        dur = at + 0.002
        kt = round(at / dur, 5)
        parts.append(
            f'<tspan>{esc(ch)}'
            f'<animate attributeName="fill-opacity" values="0;0;1" keyTimes="0;{kt};1" '
            f'dur="{round(dur, 3)}s" begin="0s" fill="freeze"/></tspan>')
    done = TYPE_START + len(text) * TYPE_CHAR
    # cursor: hidden, appears at TYPE_START, blinks with the typing, four
    # slow blinks after the text lands, then gone for good
    blink_end = done + 2.4
    kts = [0, TYPE_START / blink_end]
    vals = ['0', '1']
    t = done
    while t < blink_end - 0.01:
        kts += [t / blink_end, min((t + 0.3) / blink_end, 1)]
        vals += ['0', '1']
        t += 0.6
    kts += [1]
    vals += ['0']
    kt_s = ';'.join(str(round(k, 5)) for k in kts)
    cursor = (f'<tspan class="accent">▊'
              f'<animate attributeName="fill-opacity" values="{";".join(vals)}" '
              f'keyTimes="{kt_s}" calcMode="discrete" dur="{round(blink_end, 3)}s" '
              f'begin="0s" fill="freeze"/></tspan>')
    line = f'<tspan x="390" y="{y}" class="accent" font-style="italic">{"".join(parts)}{cursor}</tspan>'
    return line, len(text) + 1

def field(fid, value, budget):
    """Dynamic stat field: dots tspan (id=fid_dots) + value tspan (id=fid)."""
    v = '{:,}'.format(value) if isinstance(value, int) else str(value)
    d = dots_str(max(0, budget - len(v)))
    dots_ts = f'<tspan class="cc" id="{fid}_dots">{d}</tspan>' if budget else ''
    return f'{dots_ts}<tspan class="value" id="{fid}">{v}</tspan>', len(d) + len(v)

def stats_repos(y, repos, contrib, stars):
    f1, l1 = field('repo_data', repos, 6)
    f2, l2 = field('contrib_data', contrib, 0)
    f3, l3 = field('star_data', stars, 14)
    line = (f'<tspan x="390" y="{y}" class="cc">. </tspan><tspan class="key">Repos</tspan>:{f1}'
            f' {{<tspan class="key">Contributed</tspan>: {f2}}} | <tspan class="key">Stars</tspan>:{f3}')
    return line, 2 + 6 + l1 + 2 + 13 + l2 + 4 + 6 + l3

def stats_commits(y, commits, followers):
    f1, l1 = field('commit_data', commits, 23)
    f2, l2 = field('follower_data', followers, 10)
    line = (f'<tspan x="390" y="{y}" class="cc">. </tspan><tspan class="key">Commits</tspan>:{f1}'
            f' | <tspan class="key">Followers</tspan>:{f2}')
    return line, 2 + 8 + l1 + 3 + 10 + l2

def stats_loc(y, loc, loc_add, loc_del):
    f1, l1 = field('loc_data', loc, 15)
    add_v = '{:,}'.format(loc_add)
    del_v = '{:,}'.format(loc_del)
    del_d = dots_str(max(0, 7 - len(del_v)))
    line = (f'<tspan x="390" y="{y}" class="cc">. </tspan><tspan class="key">Lines of Code</tspan>:{f1}'
            f' ( <tspan class="addColor" id="loc_add">{add_v}</tspan><tspan class="addColor">++</tspan>, '
            f'<tspan id="loc_del_dots">{del_d}</tspan><tspan class="delColor" id="loc_del">{del_v}</tspan>'
            f'<tspan class="delColor">--</tspan> )')
    return line, 2 + 14 + l1 + 3 + len(add_v) + 4 + len(del_d) + len(del_v) + 4

# ---------------------------------------------------------------- content --
SEEDS = dict(repos=58, contrib=61, stars=1, commits=815, followers=2,
             loc=1242638, loc_add=1320297, loc_del=77659)

QUOTE_TEXT = '"We\'re here to put a dent in the universe."'

def info_lines():
    y = iter(ROWS)
    out = []
    def nxt(): return next(y)
    out.append(header(nxt(), 'sahith@thummala'))
    out.append(kv(nxt(), 'Role', 'Machine Learning Engineer'))
    out.append(kv(nxt(), 'Company', 'FedEx Express'))
    out.append(kv(nxt(), 'Education', 'M.S. Computer Science, GSU'))
    out.append(kv(nxt(), 'Award', 'FedEx Innovation Award'))
    out.append(kv(nxt(), 'Focus', 'GenAI, Agents, Production ML'))
    out.append(blank(nxt()))
    nxt()  # skip row
    out.append(header(nxt(), '- Stack'))
    out.append(kv(nxt(), 'Languages', 'Python, SQL, Java, TypeScript'))
    out.append(kv(nxt(), 'ML', 'PyTorch, TensorFlow, XGBoost'))
    out.append(kv(nxt(), 'LLM', 'HuggingFace, RAG, Fine-Tuning'))
    out.append(kv(nxt(), 'Agents', 'LangGraph, LangChain, Ollama, MCP'))
    out.append(kv(nxt(), 'Data', 'Databricks, Snowflake, Spark'))
    out.append(kv(nxt(), 'Infra', 'Docker, AWS, GCP, Redis, FastAPI'))
    out.append(blank(nxt()))
    nxt()  # skip row
    out.append(header(nxt(), '- Contact'))
    out.append(kv(nxt(), 'Email', 'tsahith59@gmail.com'))
    out.append(kv(nxt(), 'Phone', '404-861-6382'))
    out.append(kv(nxt(), 'LinkedIn', 'linkedin.com/in/sahith-reddy-thummala59'))
    out.append(kv(nxt(), 'GitHub', 'github.com/Sahith59'))
    out.append(blank(nxt()))
    nxt()  # skip row
    out.append(header(nxt(), '- GitHub Stats'))
    out.append(stats_repos(nxt(), SEEDS['repos'], SEEDS['contrib'], SEEDS['stars']))
    out.append(stats_commits(nxt(), SEEDS['commits'], SEEDS['followers']))
    out.append(stats_loc(nxt(), SEEDS['loc'], SEEDS['loc_add'], SEEDS['loc_del']))
    out.append(kv(nxt(), 'Activity', '▁' * 30, 'spark_data', value_class='addColor'))
    nxt()  # skip row
    out.append(typewriter(nxt(), QUOTE_TEXT))
    return out

# 'ascii' (glyph portrait, the live default) or 'lego' (mosaic tiles);
# CRT_FX=1 additionally layers scan lines + flicker + glitch strips
PORTRAIT_STYLE = os.environ.get('PORTRAIT_STYLE', 'ascii')
CRT_FX = os.environ.get('CRT_FX', '0') == '1'

def lego_cells(raw_shades, display_gamma, shades_hex):
    """Lego-mosaic portrait: merge shade-grid column pairs into ~square cells,
    each drawn as a rounded tile with a lighter stud (21st.dev 'lego' mode)."""
    out = []
    rows = len(raw_shades)
    for r in range(rows):
        row = raw_shades[r]
        for c in range(0, 74, 2):
            pair = [v for v in row[c:c + 2] if v is not None]
            if not pair:
                continue
            v = sum(pair) / len(pair)
            level = min(7, int(((v / 255.0) ** display_gamma) * 8))
            x = 15 + (c // 2) * 9.6
            y = 15 + r * 9
            tile = shades_hex[level]
            stud = shades_hex[min(7, level + 1)]
            out.append(f'<rect x="{x:.1f}" y="{y}" width="8.8" height="8.2" rx="1.5" fill="{tile}"/>')
            out.append(f'<circle cx="{x + 4.4:.1f}" cy="{y + 4.1}" r="2.4" fill="{stud}" opacity="0.85"/>')
    return '\n'.join(out)

def crt_overlays(t):
    """Recipe post-fx, SMIL edition: scanlines, CRT flicker is applied on the
    portrait group; two clipped strips of the portrait jump sideways on long
    staggered periods so the glitch never feels looped."""
    line_color = '#000000' if t['bg'] != '#ffffff' else '#1f2328'
    line_op = '0.32' if t['bg'] != '#ffffff' else '0.06'
    return f'''<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse">
<rect y="2" width="4" height="1" fill="{line_color}" opacity="{line_op}"/>
</pattern>
<clipPath id="strip1"><rect x="8" y="212" width="370" height="12"/></clipPath>
<clipPath id="strip2"><rect x="8" y="425" width="370" height="9"/></clipPath>''', f'''<rect x="8" y="10" width="372" height="{HEIGHT - 20}" fill="url(#scan)"/>
<g clip-path="url(#strip1)"><use href="#portrait">
<animateTransform attributeName="transform" type="translate" calcMode="discrete"
values="0 0;-7 0;5 0;0 0" keyTimes="0;0.906;0.934;0.962" dur="9s" repeatCount="indefinite"/>
</use></g>
<g clip-path="url(#strip2)"><use href="#portrait">
<animateTransform attributeName="transform" type="translate" calcMode="discrete"
values="0 0;6 0;-4 0;0 0" keyTimes="0;0.937;0.958;0.981" dur="13s" repeatCount="indefinite"/>
</use></g>'''

FLICKER = ('<animate attributeName="opacity" '
           'values="1;1;0.93;1;1;0.97;1;1" keyTimes="0;0.41;0.43;0.45;0.78;0.8;0.82;1" '
           'dur="7s" begin="2s" repeatCount="indefinite"/>')

def load_ascii(filename):
    with open(os.path.join(HERE, filename)) as f:
        lines = f.read().rstrip('\n').split('\n')
    assert len(lines) <= 64, f'ASCII art has {len(lines)} lines, max 64'
    for i, l in enumerate(lines):
        assert len(l) <= 74, f'ASCII line {i+1} is {len(l)} chars, max 74'
    return lines

def ascii_tspans(glyph_lines, raw_shades, display_gamma):
    """One tspan per run of equal shade level, so each glyph run carries
    its grayscale tone (class s0..s7). Background cells stay plain spaces."""
    quant = lambda v: None if v is None else min(7, int(((v / 255.0) ** display_gamma) * 8))
    shades = [[quant(v) for v in row] for row in raw_shades]
    out = []
    for i, line in enumerate(glyph_lines):
        y = 28 + i * 9
        row_shades = shades[i]
        parts, j = [], 0
        while j < len(line):
            level = row_shades[j] if j < len(row_shades) else None
            k = j
            while k < len(line) and (row_shades[k] if k < len(row_shades) else None) == level:
                k += 1
            seg = esc(line[j:k])
            parts.append(seg if level is None else f'<tspan class="s{level}">{seg}</tspan>')
            j = k
        out.append(f'<tspan x="15" y="{y}">{"".join(parts)}</tspan>')
    return '\n'.join(out)

def build(theme_file, t):
    lines = info_lines()
    for _, plen in lines:
        assert plen <= LINE_WIDTH + 2, f'line width {plen} exceeds {LINE_WIDTH + 2}'
    ascii_lines = load_ascii(t['ascii_file'])
    with open(os.path.join(HERE, 'ascii_shade.json')) as f:
        shades = json.load(f)
    if PORTRAIT_STYLE == 'lego':
        portrait_inner = f'<g>{lego_cells(shades, t["display_gamma"], t["shades"])}\n{reveal_anim(0.0, 0.7)}</g>'
    else:
        ascii_ts = ascii_tspans(ascii_lines, shades, t['display_gamma'])
        portrait_inner = (f'<text x="15" y="28" fill="{t["fg"]}" class="ascii" font-size="8px" font-weight="bold">\n'
                          f'{ascii_ts}\n{reveal_anim(0.0, 0.7)}\n</text>')
    crt_defs, crt_body = crt_overlays(t) if CRT_FX else ('', '')
    flicker = FLICKER if CRT_FX else ''
    # each info row is its own <text> so the HUD boot can reveal them in order;
    # the typewriter row (last) manages its own per-character timing instead
    row_texts = []
    for i, (line, _) in enumerate(lines):
        anim = '' if i == len(lines) - 1 else reveal_anim(BOOT_START + i * BOOT_STAGGER, BOOT_FADE)
        row_texts.append(f'<text>{line}{anim}</text>')
    info_ts = '\n'.join(row_texts)
    shade_css = '\n'.join(f'.s{i} {{fill: {c};}}' for i, c in enumerate(t['shades']))
    svg = f'''<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="{HEIGHT}px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {t['key']};}}
.value {{fill: {t['value']};}}
.addColor {{fill: {t['add']};}}
.delColor {{fill: {t['del']};}}
.cc {{fill: {t['cc']};}}
.accent {{fill: {t['accent']};}}
.quote {{fill: {t['quote']};}}
{shade_css}
text, tspan {{white-space: pre;}}
</style>
<defs>
<radialGradient id="reactor">
<stop offset="0%" stop-color="{t['accent']}" stop-opacity="{t['glow_opacity']}"/>
<stop offset="55%" stop-color="{t['accent']}" stop-opacity="{float(t['glow_opacity']) * 0.45:.3f}"/>
<stop offset="100%" stop-color="{t['accent']}" stop-opacity="0"/>
</radialGradient>
{crt_defs}
</defs>
<rect x="0.5" y="0.5" width="984px" height="{HEIGHT - 1}px" fill="{t['bg']}" stroke="{t['cc']}" stroke-width="1" rx="15"/>
<circle cx="192" cy="546" r="88" fill="url(#reactor)">
<animate attributeName="opacity" values="0.55;1;0.55" dur="5s" begin="1s" repeatCount="indefinite"/>
</circle>
<circle cx="379" cy="24" r="6" fill="none" stroke="{t['accent']}" stroke-width="1" opacity="0.4"/>
<circle cx="379" cy="24" r="3" fill="{t['accent']}">
<animate attributeName="opacity" values="1;0.25;1" dur="2.6s" repeatCount="indefinite"/>
</circle>
<g id="portrait">
{flicker}
{portrait_inner}
</g>
{crt_body}
<g fill="{t['fg']}" font-weight="bold">
{info_ts}
</g>
</svg>'''
    with open(os.path.join(REPO, theme_file), 'w') as f:
        f.write(svg)
    print(f'wrote {theme_file}')

if __name__ == '__main__':
    for name, theme in THEMES.items():
        build(name, theme)
    print('validated: values at col', VALUE_COL, ', lines <=', LINE_WIDTH)