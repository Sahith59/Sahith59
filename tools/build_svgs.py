#!/usr/bin/env python3
"""Generates dark_mode.svg + light_mode.svg for Sahith59/Sahith59.

Info column: values left-aligned at a fixed column (col 28 of a 60-char
line) so the panel reads as a clean two-column table. Dynamic stat fields
carry ids that today.py rewrites daily (stats keep dot-justified budgets
so those lines stay width-stable).

Portrait: 74x56 glyph grid rendered at 8px (own font-size), one file per
theme so both render as a photographic positive.
"""
import datetime
from dateutil import relativedelta
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

LINE_WIDTH = 60
VALUE_COL = 28          # 0-indexed char column where every kv value starts
HEIGHT = 550            # 26 info rows: y=30..530 step 20
ROWS = list(range(30, 531, 20))

# Monochrome: grayscale everything, single subtle terminal-green accent
THEMES = {
    'dark_mode.svg': {
        'bg': '#0d1117', 'fg': '#e6edf3',
        'key': '#7d8590', 'value': '#e6edf3', 'cc': '#2d333b',
        'add': '#3fb950', 'del': '#7d8590', 'accent': '#3fb950',
        'ascii_file': 'ascii_art_dark.txt',
        'display_gamma': 0.55,  # keep in sync with ascii_convert.DARK_DISPLAY_GAMMA
        # luminance level 0 (darkest) -> 7 (brightest) on a dark card
        'shades': ['#1c2128', '#2d333b', '#444c56', '#616e7f',
                   '#7d8590', '#9ea7b3', '#c9d1d9', '#f0f6fc'],
    },
    'light_mode.svg': {
        'bg': '#ffffff', 'fg': '#1f2328',
        'key': '#656d76', 'value': '#1f2328', 'cc': '#d0d7de',
        'add': '#1a7f37', 'del': '#656d76', 'accent': '#1a7f37',
        'ascii_file': 'ascii_art_light.txt',
        'display_gamma': 1.0,
        # same level order: dark tones get dark ink on a white card
        'shades': ['#1f2328', '#30363d', '#484f58', '#656d76',
                   '#8b949e', '#afb8c1', '#c9d1d9', '#e6e9ec'],
    },
}

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def age_now():
    diff = relativedelta.relativedelta(datetime.datetime.today(), datetime.datetime(2004, 5, 9))
    s = 's' if diff.years != 1 else ''
    m = 's' if diff.months != 1 else ''
    d = 's' if diff.days != 1 else ''
    return f'{diff.years} year{s}, {diff.months} month{m}, {diff.days} day{d}'

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

def kv(y, keys, value, value_id=None):
    """'. Key.Sub: ... value' — value always starts at VALUE_COL."""
    key_txt = '.'.join(keys)
    n = VALUE_COL - 2 - len(key_txt) - 1 - 2
    assert n >= 2, f'key too long at y={y}: {key_txt}'
    assert len(value) <= LINE_WIDTH - VALUE_COL, f'value too long at y={y}: {value}'
    dots = ' ' + '.' * n + ' '
    key_ts = '.'.join(f'<tspan class="key">{esc(k)}</tspan>' for k in keys)
    id_val = f' id="{value_id}"' if value_id else ''
    line = (f'<tspan x="390" y="{y}" class="cc">. </tspan>{key_ts}:'
            f'<tspan class="cc">{dots}</tspan>'
            f'<tspan class="value"{id_val}>{esc(value)}</tspan>')
    return line, VALUE_COL + len(value)

def blank(y):
    return f'<tspan x="390" y="{y}" class="cc">. </tspan>', 2

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
LANG_REAL = os.environ.get('LANG_REAL', 'English')
SEEDS = dict(repos=53, contrib=54, stars=11, commits=656, followers=1,
             loc=1148848, loc_add=1221785, loc_del=72937)

def info_lines():
    y = iter(ROWS)
    out = []
    def nxt(): return next(y)
    out.append(header(nxt(), 'sahith@thummala'))
    out.append(kv(nxt(), ['OS'], 'macOS 26.5, Linux'))
    out.append(kv(nxt(), ['Uptime'], age_now(), 'age_data'))
    out.append(kv(nxt(), ['Host'], 'FedEx Express'))
    out.append(kv(nxt(), ['Kernel'], 'Machine Learning Engineer'))
    out.append(kv(nxt(), ['IDE'], 'VSCode 1.122.1, Cursor'))
    out.append(blank(nxt()))
    out.append(kv(nxt(), ['Languages', 'Programming'], 'Python, SQL, Java, TypeScript'))
    out.append(kv(nxt(), ['Languages', 'Real'], LANG_REAL))
    out.append(blank(nxt()))
    out.append(kv(nxt(), ['Stack', 'ML'], 'PyTorch, TensorFlow, HuggingFace'))
    out.append(kv(nxt(), ['Stack', 'Agents'], 'LangGraph, LangChain, RAG'))
    out.append(kv(nxt(), ['Stack', 'Infra'], 'Docker, AWS, GCP, Redis, FastAPI'))
    out.append(blank(nxt()))
    out.append(kv(nxt(), ['Hobbies', 'Software'], 'MCP Servers, Building Cool Stuff'))
    out.append(kv(nxt(), ['Hobbies', 'Real'], 'Physics, Robotics'))
    nxt()  # skip row
    out.append(header(nxt(), '- Contact'))
    out.append(kv(nxt(), ['Email', 'Personal'], 'tsahith59@gmail.com'))
    out.append(kv(nxt(), ['Phone', 'Personal'], '404-861-6382'))
    out.append(kv(nxt(), ['LinkedIn'], 'sahith-reddy-thummala59'))
    nxt()  # skip row
    out.append(header(nxt(), '- GitHub Stats'))
    out.append(stats_repos(nxt(), SEEDS['repos'], SEEDS['contrib'], SEEDS['stars']))
    out.append(stats_commits(nxt(), SEEDS['commits'], SEEDS['followers']))
    out.append(stats_loc(nxt(), SEEDS['loc'], SEEDS['loc_add'], SEEDS['loc_del']))
    return out

def load_ascii(filename):
    with open(os.path.join(HERE, filename)) as f:
        lines = f.read().rstrip('\n').split('\n')
    assert len(lines) <= 56, f'ASCII art has {len(lines)} lines, max 56'
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
    # portrait: own 8px bold font, 9px line height, grayscale-shaded runs
    ascii_ts = ascii_tspans(ascii_lines, shades, t['display_gamma'])
    info_ts = '\n'.join(l for l, _ in lines)
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
{shade_css}
text, tspan {{white-space: pre;}}
</style>
<rect x="0.5" y="0.5" width="984px" height="{HEIGHT - 1}px" fill="{t['bg']}" stroke="{t['cc']}" stroke-width="1" rx="15"/>
<text x="15" y="28" fill="{t['fg']}" class="ascii" font-size="8px" font-weight="bold">
{ascii_ts}
</text>
<text x="390" y="30" fill="{t['fg']}">
{info_ts}
</text>
</svg>'''
    with open(os.path.join(REPO, theme_file), 'w') as f:
        f.write(svg)
    print(f'wrote {theme_file}')

if __name__ == '__main__':
    for name, theme in THEMES.items():
        build(name, theme)
    print('validated: values at col', VALUE_COL, ', lines <=', LINE_WIDTH)