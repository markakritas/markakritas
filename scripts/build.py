# /// script
# requires-python = ">=3.12"
# dependencies = ["fonttools>=4.50", "brotli>=1.1"]
# ///
"""Re-render the profile figures.

uv run scripts/build.py                   # as the daily workflow does
uv run scripts/build.py --date 2027-01-01
"""

import sys
import argparse
import html
import re
import urllib.request
import xml.etree.ElementTree as ET

from datetime import date
from email.utils import parsedate_to_datetime
from pathlib import Path

import content as C
import figures


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
THEMES = ("dark", "light")


def write(name: str, paper) -> None:
    if missing := paper.missing():
        print(
            f"warning: {name}: no glyph for {''.join(sorted(missing))!r}",
            file=sys.stderr,
        )
    (ASSETS / f"{name}-{paper.theme}.svg").write_text(paper.render(), encoding="utf-8")


def latest_issue() -> tuple[date, str] | None:
    """Date and top story of the newest newsletter issue, from its RSS feed."""
    # the site's CDN turns away urllib's default user agent
    req = urllib.request.Request(
        C.NEWSLETTER["feed"],
        headers={"User-Agent": f"{C.USER}-profile (+https://github.com/{C.USER})"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            item = ET.parse(resp).getroot().find("channel/item")
    except (OSError, ET.ParseError) as err:
        print(f"warning: newsletter feed unavailable ({err})", file=sys.stderr)
        return None
    if item is None:
        return None
    top = re.search(r"<h3>(.*?)</h3>", item.findtext("description", ""), re.DOTALL)
    headline = re.sub(r"<[^>]+>", "", top[1]) if top else item.findtext("title", "")
    day = parsedate_to_datetime(item.findtext("pubDate")).date()
    return day, html.unescape(headline).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=date.fromisoformat, default=date.today())
    today = ap.parse_args().date
    latest = latest_issue()

    for theme in THEMES:
        write("header", figures.header(theme, today))
        write("stack", figures.stack(theme))
        write("career", figures.career(theme, today))
        write("footer", figures.footer(theme, today))
        write("philosophy", figures.philosophy(theme))
        write("jumpwise", figures.extension(theme))
        # on a failed fetch, keep yesterday's card rather than drop the latest issue
        if latest or not (ASSETS / f"newspepper-{theme}.svg").exists():
            write("newspepper", figures.newspepper(theme, latest))
        for label, value in C.CONTACTS:
            write(f"chip-{label}", figures.chip(theme, label, value))


if __name__ == "__main__":
    main()
