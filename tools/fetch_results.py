#!/usr/bin/env python3
"""Fetch latest lottery results and update data/results.json. Stdlib only.

Sources (all verified 2026-10-07):
- NY Open Data Socrata (no auth): Powerball+Double Play, Mega Millions,
  Millionaire for Life.
- lotteryusa.com HTML scrape: Lotto America (no free JSON API exists).

Exit 0 on success (changed or not). Exit non-zero on any fetch/parse
failure so the Actions run visibly fails instead of publishing stale data.
"""
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "results.json"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) LiveLottoResultsBot/1.0"}


def die(msg):
    print(f"FATAL: {msg}", file=sys.stderr)
    sys.exit(1)


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        die(f"GET {url} failed: {e}")


def get_html(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        die(f"GET {url} failed: {e}")


def socrata(dataset, limit=5):
    url = (f"https://data.ny.gov/resource/{dataset}.json"
           f"?$order=draw_date%20DESC&$limit={limit}")
    rows = get_json(url)
    if not rows:
        die(f"socrata {dataset}: empty response")
    return rows


def norm_date(s):
    # "2026-10-05T00:00:00.000" -> "2026-10-05"
    return s[:10]


def split_nums(s, n):
    parts = s.strip().split()
    if len(parts) != n:
        die(f"expected {n} numbers, got {len(parts)} in {s!r}")
    return [p.lstrip("0") or "0" for p in parts]


def fetch_powerball():
    rows = socrata("d6yy-54nr")
    out = {}
    for row in rows:
        try:
            nums = split_nums(row["winning_numbers"], 6)
            dp = split_nums(row["double_play_winning_numbers"], 6)
        except KeyError as e:
            die(f"powerball row missing key: {e} (row={row})")
        d = norm_date(row["draw_date"])
        out.setdefault("powerball", {"date": d, "numbers": nums[:5], "bonus": nums[5]})
        out.setdefault("double_play", {"date": d, "numbers": dp[:5], "bonus": dp[5]})
        # keep the newest only
        break
    # newest row is first (DESC); but be explicit:
    newest = max(rows, key=lambda r: r["draw_date"])
    nums = split_nums(newest["winning_numbers"], 6)
    dp = split_nums(newest["double_play_winning_numbers"], 6)
    d = norm_date(newest["draw_date"])
    return {
        "powerball": {"date": d, "numbers": nums[:5], "bonus": nums[5]},
        "double_play": {"date": d, "numbers": dp[:5], "bonus": dp[5]},
    }


def fetch_mega():
    rows = socrata("5xaw-6ayf")
    newest = max(rows, key=lambda r: r["draw_date"])
    try:
        nums = split_nums(newest["winning_numbers"], 5)
        mb = (newest["mega_ball"] or "").strip().lstrip("0") or "0"
    except KeyError as e:
        die(f"mega millions row missing key: {e}")
    return {"mega_millions": {"date": norm_date(newest["draw_date"]),
                              "numbers": nums, "bonus": mb}}


def fetch_mfl():
    rows = socrata("a4w9-a3tp")
    newest = max(rows, key=lambda r: r["draw_date"])
    try:
        nums = split_nums(newest["winning_numbers"], 5)
        mb = (newest["mill_ball"] or "").strip().lstrip("0") or "0"
    except KeyError as e:
        die(f"millionaire-for-life row missing key: {e}")
    return {"millionaire_for_life": {"date": norm_date(newest["draw_date"]),
                                    "numbers": nums, "bonus": mb}}


MONTHS = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
          "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10",
          "Nov": "11", "Dec": "12"}


def fetch_lotto_america():
    html = get_html("https://www.lotteryusa.com/lotto-america/")
    m = re.search(r'<tr[^>]*class="[^"]*c-draw-card[^"]*"[^>]*>(.*?)</tr>',
                  html, re.S)
    if not m:
        die("lotto america: no tr.c-draw-card found (markup changed?)")
    block = m.group(1)
    dm = re.search(r'c-draw-card__draw-date-sub[^>]*>([^<]+)<', block)
    if not dm:
        die("lotto america: draw date not found")
    date_s = dm.group(1).strip()  # e.g. "Oct 5, 2026"
    dm2 = re.match(r"(\w{3})\s+(\d{1,2}),\s*(\d{4})", date_s)
    if not dm2:
        die(f"lotto america: unparseable date {date_s!r}")
    iso = f"{dm2.group(3)}-{MONTHS[dm2.group(1)]}-{int(dm2.group(2)):02d}"
    balls = re.findall(r'<li[^>]*class="[^"]*c-ball--sm[^"]*"[^>]*>(\d+)<', block)
    if len(balls) < 5:
        die(f"lotto america: found only {len(balls)} balls")
    star = None
    sm = re.search(r'<abbr[^>]*title="Star Ball"[^>]*>.*?</abbr>\s*<?\w*[^>]*>?(\d+)',
                   block, re.S)
    if sm:
        star = sm.group(1)
    else:
        # fallback: 6th ball in card
        allb = re.findall(r'c-ball[^"]*"[^>]*>(\d+)<', block)
        if len(allb) >= 6:
            star = allb[5]
    if not star:
        die("lotto america: star ball not found")
    return {"lotto_america": {"date": iso, "numbers": balls[:5], "bonus": star}}


def main():
    prev = {}
    if DATA_FILE.exists():
        prev = json.loads(DATA_FILE.read_text())

    new = {}
    new.update(fetch_powerball())
    new.update(fetch_mega())
    new.update(fetch_mfl())
    new.update(fetch_lotto_america())

    changed = False
    for game, rec in new.items():
        old = prev.get(game, {})
        if old.get("date") != rec["date"] or old.get("numbers") != rec["numbers"]:
            changed = True
        prev[game] = rec

    prev["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(prev, indent=2, sort_keys=True) + "\n")
    print("changed:" , changed)
    for g, r in new.items():
        print(f"  {g}: {r['date']} {' '.join(r['numbers'])} +{r['bonus']}")


if __name__ == "__main__":
    main()
