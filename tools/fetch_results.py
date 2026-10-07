#!/usr/bin/env python3
"""Fetch latest lottery results from LotteryUSA and update data/results.json.

All games come from https://www.lotteryusa.com/<game>/ hub pages (verified
2026-10-07). Stdlib only.

- Powerball page also carries the Double Play draw
  (<p class="c-draw-card__ball-title">Double Play</p>).
- Parsing is pinned to stable class names; any markup change or missing
  element exits non-zero so the Actions run visibly fails instead of
  publishing stale/wrong numbers.

Exit 0 on success (changed or not).
"""
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "results.json"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

PAGES = {
    "powerball": "https://www.lotteryusa.com/powerball/",
    "mega_millions": "https://www.lotteryusa.com/mega-millions/",
    "lotto_america": "https://www.lotteryusa.com/lotto-america/",
    "millionaire_for_life": "https://www.lotteryusa.com/millionaire-for-life/",
}

# powerball page section titles -> our game keys
SECTIONS = {"Main draw": "powerball", "Double Play": "double_play"}

MONTHS = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
          "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10",
          "Nov": "11", "Dec": "12"}


def die(msg):
    print(f"FATAL: {msg}", file=sys.stderr)
    sys.exit(1)


def get_html(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            if r.status != 200:
                die(f"GET {url}: HTTP {r.status}")
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        die(f"GET {url} failed: {e}")


def parse_date(s):
    m = re.match(r"(\w{3})\s+(\d{1,2}),\s*(\d{4})", s.strip())
    if not m:
        die(f"unparseable draw date {s!r}")
    return f"{m.group(3)}-{MONTHS[m.group(1)]}-{int(m.group(2)):02d}"


def parse_box(ul_html, where):
    whites = re.findall(
        r'<li[^>]*class="[^"]*c-ball--sm[^"]*"[^>]*>(\d+)</li>', ul_html)
    if len(whites) != 5:
        die(f"{where}: expected 5 white balls, got {len(whites)}")
    bm = re.search(
        r'<abbr[^>]*title="([^"]+)"[^>]*>.*?</abbr>'
        r'.*?<span[^>]*>(\d+)</span>', ul_html, re.S)
    if not bm:
        die(f"{where}: bonus ball not found")
    return {"numbers": whites, "bonus": bm.group(2), "bonus_name": bm.group(1)}


def parse_page(url, game):
    html = get_html(url)
    dm = re.search(r'c-draw-card__draw-date-sub[^>]*>([^<]+)<', html)
    if not dm:
        die(f"{game}: latest draw date not found (markup changed?)")
    iso = parse_date(dm.group(1))
    # window: from the date to the next draw card (or a bounded slice)
    tail = html[dm.end():]
    nxt = re.search(r'c-draw-card__draw-date-sub', tail)
    window = tail[:nxt.start()] if nxt else tail[:12000]

    out = {}
    # titled sections (powerball page: Main draw + Double Play)
    titled = re.findall(
        r'<p[^>]*class="[^"]*c-draw-card__ball-title[^"]*"[^>]*>'
        r'([^<]+)</p>\s*'
        r'<ul[^>]*class="[^"]*c-draw-card__ball-list[^"]*"[^>]*>(.*?)</ul>',
        window, re.S)
    if titled:
        for title, ul_html in titled:
            title = title.strip()
            key = SECTIONS.get(title)
            if not key:
                die(f"{game}: unexpected section title {title!r}")
            rec = parse_box(ul_html, f"{game}/{title}")
            rec["date"] = iso
            out[key] = rec
    else:
        um = re.search(
            r'<ul[^>]*class="[^"]*c-draw-card__ball-list[^"]*"[^>]*>(.*?)</ul>',
            window, re.S)
        if not um:
            die(f"{game}: ball list not found (markup changed?)")
        rec = parse_box(um.group(1), game)
        rec["date"] = iso
        out[game] = rec
    return out


def main():
    prev = json.loads(DATA_FILE.read_text()) if DATA_FILE.exists() else {}
    new = {}
    for game, url in PAGES.items():
        new.update(parse_page(url, game))
        print(f"  fetched {game}: {url}")

    changed = False
    for game in ["powerball", "double_play", "mega_millions",
                 "lotto_america", "millionaire_for_life"]:
        rec = new.get(game)
        if not rec:
            die(f"no data parsed for {game}")
        old = prev.get(game, {})
        if (old.get("date") != rec["date"]
                or old.get("numbers") != rec["numbers"]
                or old.get("bonus") != rec["bonus"]):
            changed = True
        prev[game] = {"date": rec["date"], "numbers": rec["numbers"],
                      "bonus": rec["bonus"]}

    prev["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(prev, indent=2, sort_keys=True) + "\n")
    print("changed:", changed)
    for g in ["powerball", "double_play", "mega_millions",
              "lotto_america", "millionaire_for_life"]:
        r = prev[g]
        print(f"  {g}: {r['date']} {' '.join(r['numbers'])} +{r['bonus']}")


if __name__ == "__main__":
    main()
