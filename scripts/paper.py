"""A tiny SVG canvas: gruvbox palettes, grain-paper cards and subset-embedded fonts."""

import base64
import io

from collections import defaultdict
from functools import cache
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont


FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
ADVANCE = 0.6  # both families are 600/1000 em monospace

PALETTES = {
    "dark": {
        "bg": "#282828",
        "bg_soft": "#32302f",
        "line": "#3c3836",
        "line2": "#504945",
        "fg": "#ebdbb2",
        "fg2": "#d5c4a1",
        "muted": "#a89984",
        "faint": "#7c6f64",
        "red": "#fb4934",
        "green": "#b8bb26",
        "yellow": "#fabd2f",
        "blue": "#83a598",
        "purple": "#d3869b",
        "aqua": "#8ec07c",
        "orange": "#fe8019",
        "grain": "#fbf1c7",
    },
    "light": {
        "bg": "#fbf1c7",
        "bg_soft": "#f2e5bc",
        "line": "#ebdbb2",
        "line2": "#d5c4a1",
        "fg": "#3c3836",
        "fg2": "#504945",
        "muted": "#7c6f64",
        "faint": "#a89984",
        "red": "#9d0006",
        "green": "#79740e",
        "yellow": "#b57614",
        "blue": "#076678",
        "purple": "#8f3f71",
        "aqua": "#427b58",
        "orange": "#af3a03",
        "grain": "#3c3836",
    },
}

# key -> (css family, weight, style, file)
FONTS = {
    "regular": ("Maple Mono", 400, "normal", "MapleMono-Regular.ttf"),
    "italic": ("Maple Mono", 400, "italic", "MapleMono-Italic.ttf"),
    "bold": ("Maple Mono", 700, "normal", "MapleMono-Bold.ttf"),
    "fallback": ("JetBrains Mono", 400, "normal", "JetBrainsMono-Regular.ttf"),
}
STACK = '"Maple Mono","JetBrains Mono",ui-monospace,monospace'


@cache
def _cmap(key: str) -> frozenset[int]:
    return frozenset(TTFont(FONT_DIR / FONTS[key][3]).getBestCmap())


def _woff2(key: str, chars: set[str]) -> str:
    font = TTFont(FONT_DIR / FONTS[key][3], recalcTimestamp=False)
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]
    sub = subset.Subsetter(options)
    sub.populate(text="".join(sorted(chars)))
    sub.subset(font)
    font.flavor = "woff2"
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def mono_width(s: str, size: float, spacing: float = 0) -> float:
    return len(s) * (size * ADVANCE + spacing)


class Paper:
    """One card. Draw with `text`/`add`, then `render()`."""

    def __init__(
        self,
        width: int,
        height: int,
        theme: str,
        title: str,
        *,
        radius: float = 10,
        marks: bool = True,
    ):
        self.w, self.h, self.theme, self.title = width, height, theme, title
        self.radius, self.marks = radius, marks
        self.c = PALETTES[theme]
        self.body: list[str] = []
        self.defs: list[str] = []
        self.css: list[str] = []
        self.glyphs: dict[str, set[str]] = defaultdict(set)

    def color(self, name: str) -> str:
        return self.c.get(name, name)

    def add(self, *parts: str) -> None:
        self.body.extend(parts)

    def text(
        self,
        x: float,
        y: float,
        s: str,
        *,
        size: float = 13,
        font: str = "regular",
        fill: str = "fg",
        anchor: str = "start",
        spacing: float = 0,
        opacity: float = 1,
        extra: str = "",
    ) -> float:
        """Place a run of text and return its rendered width."""
        for ch in s:
            target = font if ord(ch) in _cmap(font) else "fallback"
            self.glyphs[target].add(ch)
        _, weight, style, _ = FONTS[font]
        attrs = f'x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{self.color(fill)}"'
        if weight != 400:
            attrs += f' font-weight="{weight}"'
        if style != "normal":
            attrs += f' font-style="{style}"'
        if anchor != "start":
            attrs += f' text-anchor="{anchor}"'
        if spacing:
            attrs += f' letter-spacing="{spacing:g}"'
        if opacity != 1:
            attrs += f' opacity="{opacity:g}"'
        self.add(f"<text {attrs}{extra}>{escape(s)}</text>")
        return mono_width(s, size, spacing)

    def missing(self) -> set[str]:
        """Characters neither embedded font can draw."""
        return {
            ch for ch in self.glyphs["fallback"] if ord(ch) not in _cmap("fallback")
        }

    def _fontfaces(self) -> str:
        faces = []
        for key, chars in sorted(self.glyphs.items()):
            family, weight, style, _ = FONTS[key]
            faces.append(
                f'@font-face{{font-family:"{family}";font-weight:{weight};font-style:{style};'
                f'src:url(data:font/woff2;base64,{_woff2(key, chars | {" "})}) format("woff2")}}'
            )
        return "".join(faces)

    def render(self) -> str:
        w, h, c = self.w, self.h, self.c
        dark = self.theme == "dark"
        # speckle: noise -> single ink color, alpha from one noise channel
        grain_alpha, grain_opacity = (
            ("2.4 0 0 0 -1.05", 0.16) if dark else ("2.6 0 0 0 -1.15", 0.22)
        )
        mottle_opacity = 0.05 if dark else 0.07
        r = self.radius
        marks = ""
        if self.marks:
            ticks = "".join(
                f"M{cx} {cy + 8 * dy}V{cy}H{cx + 8 * dx}"
                for cx, cy, dx, dy in (
                    (14, 14, 1, 1),
                    (w - 14, 14, -1, 1),
                    (14, h - 14, 1, -1),
                    (w - 14, h - 14, -1, -1),
                )
            )
            marks = f'<path d="{ticks}" stroke="{c["faint"]}" stroke-width="1" fill="none" opacity=".6"/>'
        return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">
<title id="t">{escape(self.title)}</title>
<style>{self._fontfaces()}text{{font-family:{STACK};font-kerning:none}}{"".join(self.css)}</style>
<defs>
<clipPath id="card"><rect width="{w}" height="{h}" rx="{r:g}"/></clipPath>
<filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="11" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 {grain_alpha}" result="mask"/>
<feFlood flood-color="{c["grain"]}"/><feComposite operator="in" in2="mask"/>
</filter>
<filter id="mottle" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="0.012 0.02" numOctaves="4" seed="4"/>
<feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.8 0 0 0 -0.75" result="mask"/>
<feFlood flood-color="{c["grain"]}"/><feComposite operator="in" in2="mask"/>
</filter>
{"".join(self.defs)}
</defs>
<g clip-path="url(#card)">
<rect width="{w}" height="{h}" fill="{c["bg"]}"/>
<rect width="{w}" height="{h}" filter="url(#mottle)" opacity="{mottle_opacity}"/>
{"".join(self.body)}
<rect width="{w}" height="{h}" filter="url(#grain)" opacity="{grain_opacity}"/>
</g>
{marks}
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{r - 0.5:g}" fill="none" stroke="{c["line2"]}"/>
</svg>
"""
