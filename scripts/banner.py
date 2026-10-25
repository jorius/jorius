#!/usr/bin/env python3
"""Writes assets/banner-{dark,light}.svg in jorius.github.io's paper/ink/RGB style.

Space Mono is fetched from Google Fonts subset to the banner's own glyphs and embedded as a data URI:
an SVG shown through <img> (which is how GitHub shows it) cannot load fonts from anywhere else.
Run from the repo root: python3 scripts/banner.py
"""
import base64
import re
import urllib.parse
import urllib.request

# Palettes copied from jorius.github.io src/contexts/ThemeContext.tsx (B_THEMES).
THEMES = {
    'dark': dict(paper='#292929', ink='#f2efe7', dim='#a4a197', rule='#e6e2d6', r='#ff2f2f', b='#2fb6ff', blend='screen', scan=True),
    'light': dict(paper='#efece4', ink='#0d0d0d', dim='#5f5c55', rule='#0d0d0d', r='#d01818', b='#1068c4', blend='multiply', scan=False),
}
GREEN = '#4ADE80'

BRAND = 'JORIUS'
RECORD = 'PERSONAL RECORD'
NAME = 'JOSE RÍOS'
BOX = 'WORK FROM ANYWHERE'
TZ = 'GMT-5 · COLOMBIA'
SPEC = [('SCOPE', 'Full-Stack Engineer'), ('YEARS', '10+ in production'), ('STATUS', 'available, remote'), ('GPG', '0x365602820FC1B86C')]

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def font(weight: int, text: str) -> str:
    url = 'https://fonts.googleapis.com/css2?' + urllib.parse.urlencode({'family': f'Space Mono:wght@{weight}', 'text': text})
    css = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA})).read().decode()
    src = re.search(r'url\((https://[^)]+)\)', css).group(1)
    data = urllib.request.urlopen(urllib.request.Request(src, headers={'User-Agent': UA})).read()
    return base64.b64encode(data).decode()


def svg(t: dict, regular: str, bold: str) -> str:
    rows = '\n'.join(
        f'<text x="800" y="{160 + i * 40}" class="m dim">{k}</text>'
        + (f'<circle cx="907" cy="{154 + i * 40}" r="5" fill="{GREEN}"/><circle class="pulse" cx="907" cy="{154 + i * 40}" r="5" fill="{GREEN}"/>'
           f'<text x="924" y="{160 + i * 40}" class="m">{v}</text>' if k == 'STATUS' else f'<text x="900" y="{160 + i * 40}" class="m">{v}</text>')
        for i, (k, v) in enumerate(SPEC)
    )
    name = f'<text x="56" y="236" class="name">{NAME}</text>'
    scan = '<rect width="1200" height="360" fill="url(#scan)"/>' if t['scan'] else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" width="1200" height="360" role="img" aria-label="Jose Ríos, full-stack engineer. Work from anywhere, GMT-5, Colombia.">
<style>
@font-face {{ font-family: SM; font-weight: 400; src: url(data:font/woff2;base64,{regular}) format("woff2"); }}
@font-face {{ font-family: SM; font-weight: 700; src: url(data:font/woff2;base64,{bold}) format("woff2"); }}
text {{ font-family: SM, "Space Mono", ui-monospace, Menlo, monospace; fill: {t['ink']}; }}
.m {{ font-size: 18px; letter-spacing: .06em; }}
.dim {{ fill: {t['dim']}; }}
.bold {{ font-weight: 700; }}
.name {{ font-size: 112px; font-weight: 700; letter-spacing: -.01em; }}
.r text {{ fill: {t['r']}; }} .b text {{ fill: {t['b']}; }}
.r, .b {{ mix-blend-mode: {t['blend']}; }}
.r {{ animation: gr 7s steps(1) infinite; }}
.b {{ animation: gb 7s steps(1) infinite; }}
.slice {{ animation: sl 7s steps(1) infinite; }}
.cursor {{ animation: blink 1.1s steps(1) infinite; }}
.pulse {{ animation: pulse 2.4s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
@keyframes gr {{ 0%, 100% {{ transform: translate(-2px, 0); }} 90% {{ transform: translate(-9px, 2px); }} 92% {{ transform: translate(5px, -1px); }} 94% {{ transform: translate(-2px, 0); }} }}
@keyframes gb {{ 0%, 100% {{ transform: translate(2px, 0); }} 90% {{ transform: translate(8px, -2px); }} 92% {{ transform: translate(-6px, 1px); }} 94% {{ transform: translate(2px, 0); }} }}
@keyframes sl {{ 0%, 100% {{ transform: translateX(0); opacity: 0; }} 90% {{ transform: translateX(14px); opacity: 1; }} 91.5% {{ transform: translateX(-10px); opacity: 1; }} 93% {{ transform: translateX(0); opacity: 0; }} }}
@keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
@keyframes pulse {{ 0% {{ transform: scale(1); opacity: .6; }} 100% {{ transform: scale(3); opacity: 0; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<defs>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".22"/></pattern>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 .09 0"/></filter>
<clipPath id="cut"><rect x="0" y="175" width="1200" height="16"/><rect x="0" y="205" width="1200" height="12"/></clipPath>
</defs>
<rect width="1200" height="360" fill="{t['paper']}"/>
<rect width="1200" height="360" filter="url(#grain)"/>
{scan}
<g transform="translate(56 30) scale(.875)">
<path d="M4 13 L7 3 L11 13 L21 13 L25 3 L28 13 L28 24 Q28 28 24 28 L8 28 Q4 28 4 24 Z" fill="{t['ink']}"/>
<path d="M7 6 L8.5 11 L9.5 8 Z M22.5 8 L23.5 11 L25 6 Z M16 22 L14.4 23.4 L17.6 23.4 Z" fill="#ff7ab0"/>
<circle cx="12" cy="18" r="2" fill="{t['paper']}"/><circle cx="20" cy="18" r="2" fill="{t['paper']}"/>
</g>
<text x="96" y="54" class="m bold">{BRAND}</text>
<text x="1144" y="54" class="m dim" text-anchor="end">{RECORD}</text>
<line x1="56" y1="84" x2="1144" y2="84" stroke="{t['rule']}" stroke-opacity=".35"/>
<g class="r">{name}</g><g class="b">{name}</g><g>{name}</g>
<g class="slice" clip-path="url(#cut)"><rect x="0" y="175" width="1200" height="16" fill="{t['paper']}"/><rect x="0" y="205" width="1200" height="12" fill="{t['paper']}"/><g transform="translate(6 0)">{name}</g></g>
<rect class="cursor" x="677" y="155" width="52" height="81" fill="{t['ink']}"/>
<rect x="56.5" y="290.5" width="{len(BOX) * 12.1 + 27}" height="34" fill="none" stroke="{t['ink']}"/>
<text x="70" y="313" class="m bold">{BOX}</text>
<text x="{56 + len(BOX) * 12.1 + 50}" y="313" class="m dim">{TZ}</text>
<line x1="770" y1="128" x2="770" y2="292" stroke="{t['rule']}" stroke-opacity=".35"/>
{rows}
</svg>
'''


def main() -> None:
    glyphs = ''.join(sorted(set(''.join([BRAND, RECORD, NAME, BOX, TZ] + [k + v for k, v in SPEC]))))
    regular, bold = font(400, glyphs), font(700, glyphs)
    for name, t in THEMES.items():
        with open(f'assets/banner-{name}.svg', 'w', encoding='utf-8') as f:
            f.write(svg(t, regular, bold))


if __name__ == '__main__':
    main()
