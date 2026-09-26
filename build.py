#!/usr/bin/env python3
"""Inline style.css into every page so each HTML file is self-contained.

style.css stays the single source of truth. Edit it, run this script, and
every page gets the updated stylesheet embedded. Self-contained pages work
when opened directly from disk, emailed, or previewed on a phone, not just
when served from a folder.

Usage:  python3 build.py
"""

import os
import re
import sys

PAGES = ["index.html", "privacy.html", "releases.html", "404.html"]
CSS_FILE = "style.css"

LINK_RE = re.compile(
    r'[ \t]*<link[^>]+href=["\']style\.css["\'][^>]*>[ \t]*\n?')
STYLE_RE = re.compile(
    r'[ \t]*<style>.*?</style>[ \t]*\n?', re.S)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)

    if not os.path.exists(CSS_FILE):
        sys.exit("error: %s not found" % CSS_FILE)

    with open(CSS_FILE, "r", encoding="utf-8") as fh:
        css = fh.read().strip()

    block = "<style>\n%s\n</style>\n" % css

    for page in PAGES:
        if not os.path.exists(page):
            print("  skip   %s (missing)" % page)
            continue
        with open(page, "r", encoding="utf-8") as fh:
            html = fh.read()

        # Remove whichever form is currently present, then insert fresh.
        had_link = bool(LINK_RE.search(html))
        html = LINK_RE.sub("", html)
        html = STYLE_RE.sub("", html)

        if "</head>" not in html:
            print("  ERROR  %s has no </head>" % page)
            continue
        html = html.replace("</head>", block + "</head>", 1)

        with open(page, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("  inline %s  (%s)" % (page,
                                     "was linked" if had_link else "rebuilt"))

    print("\nDone. %d bytes of CSS embedded per page." % len(css))


if __name__ == "__main__":
    main()
