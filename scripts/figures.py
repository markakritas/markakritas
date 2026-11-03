"""The figures on the profile. Each function returns a filled `Paper` for one theme."""

import itertools
import math
import re
import textwrap

from datetime import date
from pathlib import Path

import content as C

from paper import Paper, mono_width


W = 900


# ── helpers ───────────────────────────────────────────────────────────────
def lorenz(steps=9000, dt=0.006, sigma=10.0, rho=28.0, beta=8 / 3):
    def f(x, y, z):
        return sigma * (y - x), x * (rho - z) - y, x * y - beta * z

    x, y, z = 0.1, 0.0, 0.0
    out = []
    for i in range(steps):
        k1 = f(x, y, z)
        k2 = f(x + dt / 2 * k1[0], y + dt / 2 * k1[1], z + dt / 2 * k1[2])
        k3 = f(x + dt / 2 * k2[0], y + dt / 2 * k2[1], z + dt / 2 * k2[2])
        k4 = f(x + dt * k3[0], y + dt * k3[1], z + dt * k3[2])
        x += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        z += dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        if i > 400:  # drop the transient
            out.append((x, z))
    return out


def simplify(pts, tol):
    """Ramer–Douglas–Peucker, iterative."""
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (ax, ay), (bx, by) = pts[a], pts[b]
        dx, dy = bx - ax, by - ay
        norm = math.hypot(dx, dy) or 1e-9
        idx, dmax = a, 0.0
        for i in range(a + 1, b):
            px, py = pts[i]
            d = abs(dy * (px - ax) - dx * (py - ay)) / norm
            if d > dmax:
                idx, dmax = i, d
        if dmax > tol:
            keep[idx] = True
            stack += [(a, idx), (idx, b)]
    return [p for p, k in zip(pts, keep, strict=True) if k]


def years(ym: str) -> float:
    y, m = map(int, ym.split("-"))
    return y + (m - 1) / 12


def ym_label(ym: str | None) -> str:
    return "now" if ym is None else ym.replace("-", ".")


# ── fig. 1: header ────────────────────────────────────────────────────────
def header(theme: str, today: date) -> Paper:
    p = Paper(W, 330, theme, f"{C.NAME} — {C.ROLE}")
    c = p.c

    # running head
    p.text(
        40, 34, "preprint · github.com/" + C.USER, size=10.5, fill="faint", spacing=0.3
    )
    p.text(
        860,
        34,
        f"rev. {today:%Y.%m.%d}",
        size=10.5,
        fill="faint",
        anchor="end",
        spacing=0.3,
    )
    p.add(f'<path d="M40 46H860" stroke="{c["line2"]}" stroke-width="1"/>')

    # title block
    name_w = p.text(40, 112, C.NAME, size=46, font="bold", spacing=-0.5)
    p.add(
        f'<rect x="{40 + name_w + 8:g}" y="76" width="4" height="42" fill="{c["orange"]}">'
        '<animate attributeName="opacity" values="1;0" calcMode="discrete" dur="1.1s" '
        'repeatCount="indefinite"/></rect>'
    )
    p.text(40, 147, C.ROLE, size=17, fill="orange")
    p.text(40, 175, C.TAGLINE, size=15, font="italic", fill="muted")
    for i, (key, value) in enumerate(C.FACTS):
        y = 220 + i * 21
        p.text(40, y, key, size=12.5, fill="faint")
        p.text(40 + mono_width("speaks  ", 12.5), y, value, size=12.5, fill="fg2")

    # figure: lorenz attractor on graph paper
    bx, by, bw, bh = 516, 66, 344, 222
    p.defs.append(
        f'<pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse" x="{bx}" y="{by}">'
        f'<path d="M10 0H0V10" fill="none" stroke="{c["line2"]}" stroke-width=".5"/></pattern>'
        f'<pattern id="grid5" width="50" height="50" patternUnits="userSpaceOnUse" x="{bx}" y="{by}">'
        f'<path d="M50 0H0V50" fill="none" stroke="{c["line2"]}" stroke-width="1"/></pattern>'
        f'<linearGradient id="flow" x1="0" x2="1" y1="0" y2="0">'
        f'<stop offset="0" stop-color="{c["blue"]}"/><stop offset=".5" stop-color="{c["aqua"]}"/>'
        f'<stop offset="1" stop-color="{c["yellow"]}"/></linearGradient>'
    )
    p.add(
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="url(#grid)" opacity=".45"/>',
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="url(#grid5)" opacity=".5"/>',
    )
    raw = lorenz()
    xs, zs = [q[0] for q in raw], [q[1] for q in raw]
    pad = 14
    sz = (bh - 2 * pad) / (max(zs) - min(zs))
    sx = min(
        (bw - 2 * pad) / (max(xs) - min(xs)), 1.45 * sz
    )  # a gently stretched x axis
    ox = bx + bw / 2 - sx * (max(xs) + min(xs)) / 2
    oz = by + bh / 2 + sz * (max(zs) + min(zs)) / 2
    pts = simplify([(ox + sx * x, oz - sz * z) for x, z in raw], 0.2)
    d = "M" + " ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    length = sum(math.dist(a, b) for a, b in itertools.pairwise(pts))
    p.defs.append(f'<path id="lorenz" d="{d}"/>')
    p.add(
        '<use href="#lorenz" xlink:href="#lorenz" fill="none" stroke="url(#flow)" stroke-width=".7" opacity=".85"/>'
    )
    # a particle tracing the flow, with a short comet tail
    dur = length / 55
    for lag, r, op in (
        (0.0, 2.6, 1),
        (0.12, 2.0, 0.55),
        (0.24, 1.5, 0.3),
        (0.36, 1.1, 0.15),
    ):
        p.add(
            f'<circle r="{r}" fill="{c["orange"]}" opacity="{op}">'
            f'<animateMotion dur="{dur:.0f}s" begin="{lag - 0.4:.2f}s" repeatCount="indefinite">'
            f'<mpath href="#lorenz" xlink:href="#lorenz"/></animateMotion></circle>'
        )
    # axes
    ax0, ay0 = bx, by + bh
    p.add(
        f'<path d="M{ax0} {by}V{ay0}H{bx + bw}" fill="none" stroke="{c["muted"]}" stroke-width="1"/>'
    )
    for v in (-20, -10, 0, 10, 20):
        tx = ox + sx * v
        p.add(f'<path d="M{tx:.1f} {ay0}v4" stroke="{c["muted"]}"/>')
        p.text(tx, ay0 + 14, str(v), size=8.5, fill="faint", anchor="middle")
    for v in (10, 25, 40):
        ty = oz - sz * v
        p.add(f'<path d="M{ax0} {ty:.1f}h-4" stroke="{c["muted"]}"/>')
        p.text(ax0 - 7, ty + 3, str(v), size=8.5, fill="faint", anchor="end")
    p.text(
        bx + bw - 2, ay0 - 6, "x", size=10, font="italic", fill="muted", anchor="end"
    )
    p.text(bx + 6, by + 12, "z", size=10, font="italic", fill="muted")
    p.text(
        bx,
        316,
        "fig. 1 — lorenz attractor · σ=10 ρ=28 β=8/3",
        size=10.5,
        font="italic",
        fill="muted",
    )
    return p


# ── fig. 2: periodic table of the stack ───────────────────────────────────
def stack(theme: str) -> Paper:
    tw, th, gap = 64, 66, 5
    x0, y0 = (W - (12 * tw + 11 * gap)) / 2, 30
    fblock_y = y0 + 3 * (th + gap) + 14
    p = Paper(W, int(fblock_y + th + 46), theme, "periodic table of the stack")
    c = p.c

    def pos(row, col):
        y = fblock_y if row == 4 else y0 + (row - 1) * (th + gap)
        return x0 + (col - 1) * (tw + gap), y

    order = sorted(C.ELEMENTS, key=lambda e: (e[0], e[1]))
    for n, (row, col, sym, name, fam) in enumerate(order, 1):
        x, y = pos(row, col)
        hue = c[C.FAMILIES[fam][1]]
        p.add(
            f'<rect x="{x:g}" y="{y:g}" width="{tw}" height="{th}" rx="4" fill="{hue}" fill-opacity=".1" '
            f'stroke="{hue}" stroke-opacity=".55"/>'
        )
        p.text(x + 5, y + 12, str(n), size=8.5, fill="muted")
        p.text(x + tw / 2, y + 41, sym, size=22, font="bold", fill=hue, anchor="middle")
        p.text(
            x + tw / 2,
            y + 58,
            name,
            size=8.5 if len(name) > 10 else 9,
            fill="fg2",
            anchor="middle",
        )

    # the empty block of the real table holds the title and key
    tx, ty = pos(1, 3)
    p.text(
        tx + 4, ty + 26, "periodic table of the stack", size=15, font="bold", fill="fg"
    )
    p.text(
        tx + 4,
        ty + 46,
        "group = family · noble gases are inert and run everything",
        size=10.5,
        fill="muted",
    )
    lx, ly = pos(2, 3)
    for i, (label, hue) in enumerate(C.FAMILIES.values()):
        col, row = divmod(i, 4)
        x, y = lx + 4 + col * 132, ly + 14 + row * 16
        p.add(
            f'<rect x="{x:g}" y="{y - 8:g}" width="9" height="9" rx="2" fill="{c[hue]}" fill-opacity=".85"/>'
        )
        p.text(x + 16, y, label, size=10.5, fill="fg2")
    fx, fy = pos(4, 4)
    p.text(
        fx - 10,
        fy + th / 2 + 4,
        "f-block ⟶",
        size=10,
        font="italic",
        fill="faint",
        anchor="end",
    )
    p.text(
        x0,
        p.h - 18,
        "fig. 2 — periodic table of tools i reach for, arranged by family",
        size=10.5,
        font="italic",
        fill="muted",
    )
    return p


# ── fig. 3: career as a forest plot ───────────────────────────────────────
def career(theme: str, today: date) -> Paper:
    row_h, top = 18, 70
    lines = []  # ("group", name) | ("row", entry)
    for group in C.GROUPS:
        lines.append(("group", group))
        lines += [("row", e) for e in C.CAREER if e[0] == group]
    pooled_y = top + len(lines) * row_h + 14
    axis_y = pooled_y + 18
    p = Paper(W, axis_y + 62, theme, "career, drawn as a forest plot")
    c = p.c

    now = today.year + (today.month - 1) / 12 + (today.day - 1) / 365
    t0, t1 = 2010.4, max(now, 2026.5) + 0.35
    px0, px1 = 420, 748

    def X(t):
        return px0 + (t - t0) / (t1 - t0) * (px1 - px0)

    for x, label, anchor in (
        (40, "role", "start"),
        (254, "where", "start"),
        ((px0 + px1) / 2, "tenure", "middle"),
    ):
        p.text(x, 38, label, size=10, fill="faint", anchor=anchor, spacing=1)
    p.text(862, 38, "dates", size=10, fill="faint", anchor="end", spacing=1)
    p.add(f'<path d="M40 48H862" stroke="{c["line2"]}"/>')

    # year grid + the "now" reference line
    for yr in range(2012, int(t1) + 1, 2):
        p.add(
            f'<path d="M{X(yr):.1f} 56V{axis_y}" stroke="{c["line2"]}" stroke-width=".6" stroke-dasharray="1 3"/>'
        )
    xn = X(now)
    p.add(
        f'<path d="M{xn:.1f} 56V{axis_y}" stroke="{c["muted"]}" stroke-width=".8" stroke-dasharray="3 3"/>'
    )
    p.text(
        xn, axis_y + 28, "now", size=9.5, font="italic", fill="muted", anchor="middle"
    )

    for i, (kind, item) in enumerate(lines):
        y = top + i * row_h
        if kind == "group":
            p.text(40, y + 4, item.upper(), size=9.5, fill=C.GROUPS[item], spacing=1.6)
            continue
        group, role, where, start, end = item
        hue = c[C.GROUPS[group]]
        p.text(
            40, y + 4, role, size=11, fill="fg" if group != "before data" else "muted"
        )
        p.text(254, y + 4, where, size=10.5, fill="muted")
        p.text(
            862,
            y + 4,
            f"{ym_label(start)}–{ym_label(end)}",
            size=10,
            fill="faint",
            anchor="end",
        )
        a, b = years(start), now if end is None else years(end)
        xa, xb = X(a), X(b)
        p.add(
            f'<path d="M{xa:.1f} {y}H{xb:.1f}M{xa:.1f} {y - 3}v6" stroke="{hue}" stroke-width="1.4"/>'
        )
        if end is None:
            p.add(f'<path d="M{xb + 5:.1f} {y}l-6 -3.5v7z" fill="{hue}"/>')
        else:
            p.add(f'<path d="M{xb:.1f} {y - 3}v6" stroke="{hue}" stroke-width="1.4"/>')
        side = min(9, max(3.5, 2.4 + 2.4 * math.sqrt(b - a)))
        p.add(
            f'<rect x="{(xa + xb - side) / 2:.1f}" y="{y - side / 2:.1f}" width="{side:.1f}" height="{side:.1f}" fill="{hue}"/>'
        )

    # pooled estimate diamond
    label, where, start = C.POOLED
    p.add(f'<path d="M40 {pooled_y - 14}H862" stroke="{c["line2"]}"/>')
    a = X(years(start))
    p.add(
        f'<path d="M{a:.1f} {pooled_y}L{(a + xn) / 2:.1f} {pooled_y - 6}L{xn:.1f} {pooled_y}'
        f'L{(a + xn) / 2:.1f} {pooled_y + 6}z" fill="{c["fg"]}"/>'
    )
    p.text(40, pooled_y + 4, label, size=11, font="bold", fill="fg")
    p.text(254, pooled_y + 4, where, size=10.5, fill="muted")
    p.text(
        862, pooled_y + 4, f"{ym_label(start)}–now", size=10, fill="faint", anchor="end"
    )

    # axis
    p.add(f'<path d="M{px0} {axis_y}H{px1}" stroke="{c["muted"]}"/>')
    for yr in range(2012, int(t1) + 1, 2):
        p.add(f'<path d="M{X(yr):.1f} {axis_y}v4" stroke="{c["muted"]}"/>')
        p.text(X(yr), axis_y + 15, str(yr), size=9, fill="faint", anchor="middle")
    p.text(
        40,
        p.h - 16,
        "fig. 3 — career as a forest plot · whiskers span tenure · box size ~ duration · ◆ pooled",
        size=10.5,
        font="italic",
        fill="muted",
    )
    return p


# ── end matter: quote & equation of the day ───────────────────────────────
def footer(theme: str, today: date) -> Paper:
    quote, author = C.of_the_day(C.QUOTES, today)
    formula, eq_name = C.of_the_day(C.EQUATIONS, today, salt=3)
    lines = textwrap.wrap(f"“{quote}”", 78)
    qy, lh = 50, 25
    attr_y = qy + (len(lines) - 1) * lh + 28
    rule1 = attr_y + 20
    eq_y = rule1 + 32
    rule2 = eq_y + 20
    p = Paper(W, rule2 + 40, theme, f"quote of the day: {quote} — {author}")
    c = p.c

    for i, line in enumerate(lines):
        p.text(
            48 if i == 0 else 48 + mono_width("“", 16),
            qy + i * lh,
            line,
            size=16,
            font="italic",
            fill="fg",
        )
    p.text(852, attr_y, f"— {author}", size=12, fill="muted", anchor="end")
    p.add(f'<path d="M48 {rule1}H852M48 {rule2}H852" stroke="{c["line2"]}"/>')
    p.text(48, eq_y, "eq. of the day", size=10, fill="faint", spacing=0.5)
    p.text(186, eq_y + 1, formula, size=17, fill="yellow")
    p.text(852, eq_y, eq_name, size=11.5, font="italic", fill="muted", anchor="end")
    p.text(
        W / 2,
        rule2 + 24,
        f"set in maple mono · gruvbox on grain · rebuilt daily by github actions · last build {today:%Y-%m-%d}",
        size=9.5,
        fill="faint",
        anchor="middle",
    )
    return p


# ── contact chips ─────────────────────────────────────────────────────────
def chip(theme: str, label: str, value: str) -> Paper:
    size, pad = 12, 10
    lw = mono_width(label, size)
    vw = mono_width(value, size)
    w = int(pad + lw + pad + pad + vw + pad)
    p = Paper(w, 28, theme, f"{label}: {value}", radius=6, marks=False)
    c = p.c
    split = pad + lw + pad
    p.add(
        f'<rect width="{split:g}" height="28" fill="{c["orange"]}" fill-opacity=".14"/>'
    )
    p.add(f'<path d="M{split:g} 0V28" stroke="{c["line2"]}"/>')
    p.text(pad, 18.5, label, size=size, fill="orange")
    p.text(split + pad, 18.5, value, size=size, fill="fg")
    return p


# ── projects ──────────────────────────────────────────────────────────────
CARD_W, CARD_H = 440, 232
LOGOS = Path(__file__).resolve().parent.parent / "assets" / "logos"


def logo(name: str, x: float, y: float, size: float, recolor: dict[str, str]) -> str:
    """Inline a 128×128 logo from assets/logos, swapping colors for the theme."""
    svg = (LOGOS / f"{name}.svg").read_text()
    svg = re.sub(r"<!--.*?-->|<title>.*?</title>", "", svg, flags=re.DOTALL)
    inner = svg[svg.index(">", svg.index("<svg")) + 1 : svg.rindex("</svg>")]
    for old, new in recolor.items():
        inner = inner.replace(old, new)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 128 128">{inner}</svg>'


def newspepper(theme: str, latest: tuple[date, str] | None) -> Paper:
    n = C.NEWSLETTER
    p = Paper(CARD_W, CARD_H, theme, f"{n['name']} — {n['kicker']}. Subscribe.")
    c = p.c
    p.add(
        logo(
            "newspepper",
            28,
            26,
            64,
            {
                'fill="#fbfbfd"': f'fill="{c["bg_soft"]}" stroke="{c["line2"]}"',
                "#0b0c0f": c["fg"],
            },
        )
    )
    p.text(106, 56, n["name"], size=20, font="bold")
    p.text(106, 78, n["kicker"], size=11.5, fill="muted")
    p.text(28, 124, n["about"], size=12, fill="fg2")
    if latest:
        day, headline = latest
        lead = f"latest · {day:%d %b}".lower() + " · "
        room = int((CARD_W - 56) / (11 * 0.6)) - len(lead)
        if len(headline) > room:
            headline = headline[: room - 1].rstrip() + "…"
        x = 28 + p.text(28, 148, lead, size=11, fill="faint")
        p.text(x, 148, headline, size=11, fill="muted")

    # drawn like a signup field; the whole card links to the real one
    p.add(
        f'<rect x="28.5" y="168.5" width="262" height="34" rx="5" fill="{c["bg_soft"]}" stroke="{c["line2"]}"/>',
        f'<rect x="298" y="168" width="114" height="35" rx="5" fill="{c["orange"]}"/>',
    )
    p.text(42, 190, "you@example.com", size=12, font="italic", fill="faint")
    p.text(355, 190, "subscribe ↗", size=12, font="bold", fill="bg", anchor="middle")
    return p


def philosophy(theme: str) -> Paper:
    ph = C.PHILOSOPHY
    p = Paper(CARD_W, CARD_H, theme, f"{ph['name']} — {ph['about']}, {ph['status']}")
    c = p.c

    # status pill with a breathing dot
    label = ph["status"]
    pill_w = 28 + mono_width(label, 10.5)
    px = CARD_W - 28 - pill_w
    p.add(
        f'<rect x="{px:g}" y="38" width="{pill_w:g}" height="24" rx="12" fill="{c["yellow"]}" '
        f'fill-opacity=".14" stroke="{c["yellow"]}" stroke-opacity=".5"/>',
        f'<circle cx="{px + 14:g}" cy="50" r="3.5" fill="{c["yellow"]}">'
        '<animate attributeName="opacity" values="1;.2;1" dur="1.8s" repeatCount="indefinite"/>'
        "</circle>",
    )
    p.text(px + 22, 54, label, size=10.5, fill="yellow")
    p.text(28, 56, ph["name"], size=20, font="bold")
    p.text(28, 78, ph["about"], size=11.5, fill="muted")

    # a small constellation of thinkers; three rows keep the labels apart
    rows = (112, 168, 140)
    nodes = {}
    for i, name in enumerate(C.THINKERS):
        x = 54 + i * (CARD_W - 108) / (len(C.THINKERS) - 1)
        y = rows[i % 3] + (6 if i % 2 else -4) * (i % 3 == 2)
        nodes[name] = (x, y)
    edges = []
    for a, b in C.INFLUENCES:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        edges.append(f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}")
    p.add(
        f'<path d="{"".join(edges)}" stroke="{c["faint"]}" stroke-width=".8" opacity=".7"/>'
    )
    for i, (name, (x, y)) in enumerate(nodes.items()):
        hub = sum(name in e for e in C.INFLUENCES) >= 3
        p.add(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.2 if hub else 2.2}" fill="{c["fg2"]}"/>'
        )
        below = i % 3 == 1
        p.text(
            x, y + 15 if below else y - 8, name, size=8.5, fill="muted", anchor="middle"
        )
    # ideas travelling along a few of the edges
    for k, j in enumerate((2, 9, 12)):
        p.add(
            f'<circle r="2" fill="{c["yellow"]}"><animateMotion path="{edges[j]}" dur="2.6s" '
            f'begin="{-k * 0.9:.1f}s" repeatCount="indefinite"/></circle>'
        )

    # indeterminate progress bar (SMIL rather than CSS, so it runs inside <img>)
    p.defs.append(
        f'<clipPath id="track"><rect x="28" y="205" width="{CARD_W - 56}" height="4"/></clipPath>'
    )
    p.add(
        f'<path d="M28 207H{CARD_W - 28}" stroke="{c["line2"]}" stroke-width="2"/>',
        f'<g clip-path="url(#track)"><rect x="-42" y="205" width="70" height="4" rx="2" '
        f'fill="{c["yellow"]}"><animate attributeName="x" values="-42;{CARD_W - 28}" dur="3.2s" '
        'calcMode="spline" keyTimes="0;1" keySplines=".45 0 .55 1" repeatCount="indefinite"/>'
        "</rect></g>",
    )
    return p


def extension(theme: str) -> Paper:
    name, kind = C.EXTENSION
    size, h = 12, 28
    w = int(8 + 18 + 10 + mono_width(f"{name} · {kind}", size) + 12)
    p = Paper(w, h, theme, f"{name}: {kind}", radius=6, marks=False)
    c = p.c
    # the extension's icon: three nodes of a Cayley graph and "jw", redrawn in theme ink
    p.add(
        f'<g transform="translate(8 5) scale({18 / 128:.4f})" stroke="{c["fg"]}" fill="none">'
        '<circle cx="32" cy="32" r="13" stroke-width="7"/><circle cx="32" cy="96" r="13" stroke-width="7"/>'
        '<circle cx="96" cy="96" r="13" stroke-width="7"/><path d="M32 46V82M46 96H82" stroke-width="7"/>'
    )
    p.text(74, 44, "jw", size=34, font="bold", fill="fg", extra=' stroke="none"')
    p.add("</g>")
    x = 36 + p.text(36, 18.5, name, size=size, fill="fg") + mono_width(" ", size)
    p.text(x, 18.5, f"· {kind}", size=size, fill="muted")  # svg drops leading spaces
    return p
