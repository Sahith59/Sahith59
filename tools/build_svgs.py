#!/usr/bin/env python3
"""Generates dark_mode.svg + light_mode.svg for Sahith59/Sahith59.
Every info line is computed to exactly LINE_WIDTH monospace chars so the
right edge aligns. Dynamic fields carry ids that today.py re-justifies daily.
"""
import datetime
from dateutil import relativedelta
import os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASCII_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ascii_art.txt')

LINE_WIDTH = 60
ROWS = list(range(30, 511, 20))  # y=30..490 used; height 510

# Monochrome: grayscale everything, single subtle terminal-green accent
THEMES = {
    'dark_mode.svg': {
        'bg': '#0d1117', 'fg': '#e6edf3',
        'key': '#7d8590', 'value': '#e6edf3', 'cc': '#2d333b',
        'add': '#3fb950', 'del': '#7d8590', 'accent': '#3fb950',
    },
    'light_mode.svg': {
        'bg': '#ffffff', 'fg': '#1f2328',
        'key': '#656d76', 'value': '#1f2328', 'cc': '#d0d7de',
        'add': '#1a7f37', 'del': '#656d76', 'accent': '#1a7f37',
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
    """Mirror of today.py justify_format spacing rules."""
    if just_len <= 2:
        return {0: '', 1: ' ', 2: '. '}[max(0, just_len)]
    return ' ' + '.' * just_len + ' '

def header(y, title):
    fill = LINE_WIDTH - len(title) - 1
    dashes = '-' + '—' * (fill - 4) + '-—-'
    return (f'<tspan x="390" y="{y}" class="accent">{esc(title)}</tspan>'
            f'<tspan class="cc"> {dashes}</tspan>'), len(title) + 1 + fill

def kv(y, keys, value, value_id=None):
    """'. Key.Sub: .... value' — dots computed so the line is LINE_WIDTH chars."""
    key_txt = '.'.join(keys)
    just = LINE_WIDTH - 2 - len(key_txt) - 1 - 2 - len(value)  # 2 spaces around dots
    assert just >= 0, f'line y={y} overflows: {key_txt}={value}'
    dots = ' ' + '.' * just + ' '
    key_ts = '.'.join(f'<tspan class="key">{esc(k)}</tspan>' for k in keys)
    id_dots = f' id="{value_id}_dots"' if value_id else ''
    id_val = f' id="{value_id}"' if value_id else ''
    line = (f'<tspan x="390" y="{y}" class="cc">. </tspan>{key_ts}:'
            f'<tspan class="cc"{id_dots}>{dots}</tspan>'
            f'<tspan class="value"{id_val}>{esc(value)}</tspan>')
    plain = f'. {key_txt}:{dots}{value}'
    return line, len(plain)

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
    plain_len = 2 + 6 + l1 + 2 + 13 + l2 + 4 + 6 + l3
    return line, plain_len

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
    out.append(kv(nxt(), ['Languages', 'Programming'], 'Python, TypeScript, Java, C++'))
    out.append(kv(nxt(), ['Languages', 'Computer'], 'HTML, CSS, SQL, LaTeX, YAML'))
    out.append(kv(nxt(), ['Languages', 'Real'], LANG_REAL))
    out.append(blank(nxt()))
    out.append(kv(nxt(), ['Hobbies', 'Software'], 'MCP Servers, Building Cool Stuff'))
    out.append(kv(nxt(), ['Hobbies', 'Hardware'], 'Robotics'))
    out.append(kv(nxt(), ['Hobbies', 'Science'], 'Physics'))
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

def load_ascii():
    with open(ASCII_FILE) as f:
        lines = f.read().rstrip('\n').split('\n')
    assert len(lines) <= 24, f'ASCII art has {len(lines)} lines, max 24'
    for i, l in enumerate(lines):
        assert len(l) <= 38, f'ASCII line {i+1} is {len(l)} chars, max 38'
    return lines

def build(theme_file, t):
    lines = info_lines()
    for _, plen in lines:
        if plen > 2:  # skip blanks; stats lines vary ±2 with digit counts (same as upstream)
            assert LINE_WIDTH - 2 <= plen <= LINE_WIDTH + 2, f'line width {plen}: expected ~{LINE_WIDTH}'
    ascii_lines = load_ascii()
    ascii_ts = '\n'.join(
        f'<tspan x="15" y="{30 + i * 20}">{esc(l)}</tspan>' for i, l in enumerate(ascii_lines))
    info_ts = '\n'.join(l for l, _ in lines)
    svg = f'''<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="510px" font-size="16px">
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
text, tspan {{white-space: pre;}}
</style>
<rect x="0.5" y="0.5" width="984px" height="509px" fill="{t['bg']}" stroke="{t['cc']}" stroke-width="1" rx="15"/>
<text x="15" y="30" fill="{t['fg']}" class="ascii">
{ascii_ts}
</text>
<text x="390" y="30" fill="{t['fg']}">
{info_ts}
</text>
</svg>'''
    path = os.path.join(REPO, theme_file)
    with open(path, 'w') as f:
        f.write(svg)
    print(f'wrote {theme_file}')

if __name__ == '__main__':
    for name, theme in THEMES.items():
        build(name, theme)
    print('all line widths validated at', LINE_WIDTH, 'chars')