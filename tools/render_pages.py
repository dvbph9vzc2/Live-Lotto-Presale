#!/usr/bin/env python3
"""Render the 5 lottery drawing-time pages + sitemap from data/results.json.

Run: python3 tools/render_pages.py   (from repo root)
Reads data/results.json (written by tools/fetch_results.py).
"""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "results.json"
BASE = "https://dvbph9vzc2.github.io/Live-Lotto-Presale"

GAMES = {
    "powerball": {
        "name": "Powerball",
        "slug": "powerball-drawing-time",
        "meta_title": "What Time Is the Powerball Drawing Tonight? 2026 Schedule & Live Countdown",
        "meta_desc": "Powerball drawings are every Monday, Wednesday and Saturday at 10:59 PM ET. See tonight's drawing time in your timezone with a live countdown, plus cutoff times and how to check results.",
        "h1": 'What Time Is the <span>Powerball Drawing</span> Tonight?',
        "intro": 'Powerball draws every <strong>Monday, Wednesday and Saturday</strong> — here is tonight\'s time in your timezone, with a live countdown.',
        "days": [1, 3, 6], "hour": 22, "minute": 59,
        "label": "10:59 PM ET",
        "tz": [("Eastern (ET)", "10:59 PM"), ("Central (CT)", "9:59 PM"),
               ("Mountain (MT)", "8:59 PM"), ("Pacific (PT)", "7:59 PM"),
               ("Alaska (AKT)", "6:59 PM"), ("Hawaii (HT)", "4:59 PM")],
        "cutoff": "<strong>Ticket cutoff:</strong> sales close 1–2 hours before draw time depending on your state — don't wait until the last minute. Double Play drawings follow at approximately 11:30 PM ET.",
        "bonus": "Powerball",
        "howto": [
            ("<strong>Use an app</strong> — the <a href=\"index.html\" style=\"color:var(--red-700);font-weight:600\">Live Lotto app</a> posts winning numbers the second balls drop, with jackpot and cash value.",),
            ("<strong>Scan your ticket</strong> — point your phone camera at any ticket for instant win/lose matching instead of comparing numbers by hand.",),
            ("<strong>Save your numbers</strong> — get an automatic alert the moment your numbers hit, so you never miss a win.",),
        ],
        "cta": "Live results for Powerball, Mega Millions and 100+ games in all 50 states — plus ticket scanner and win alerts. Pre-order lifetime access for $9.9.",
        "faq": [
            ("What time is the Powerball drawing tonight?",
             "Powerball draws every Monday, Wednesday and Saturday at 10:59 PM Eastern Time (9:59 PM CT / 8:59 PM MT / 7:59 PM PT). Use the live countdown above for the exact time remaining."),
            ("What time is the ticket sales cutoff?",
             "Cutoff times vary by state but are typically 1 to 2 hours before the 10:59 PM ET drawing. Check your official state lottery site for the exact cutoff where you play."),
            ("Where can I watch the drawing live?",
             "Drawings stream on Powerball.com and many state lottery websites. Results are also posted instantly in the Live Lotto app with jackpot amounts, prize breakdowns and a ticket scanner."),
        ],
    },
    "double_play": {
        "name": "Powerball Double Play",
        "slug": "double-play-drawing-time",
        "meta_title": "What Time Is the Powerball Double Play Drawing? 2026 Schedule & Countdown",
        "meta_desc": "Double Play drawings follow every Powerball drawing — Monday, Wednesday and Saturday around 11:30 PM ET. See the next drawing time in your timezone with a live countdown.",
        "h1": 'What Time Is the <span>Double Play Drawing</span>?',
        "intro": 'Double Play draws right after every Powerball drawing — <strong>Monday, Wednesday and Saturday</strong>, around 11:30 PM ET.',
        "days": [1, 3, 6], "hour": 23, "minute": 30,
        "label": "11:30 PM ET",
        "tz": [("Eastern (ET)", "11:30 PM"), ("Central (CT)", "10:30 PM"),
               ("Mountain (MT)", "9:30 PM"), ("Pacific (PT)", "8:30 PM"),
               ("Alaska (AKT)", "7:30 PM"), ("Hawaii (HT)", "5:30 PM")],
        "cutoff": "<strong>How it works:</strong> Double Play is a second drawing using the same Powerball numbers format, held after each main Powerball drawing. Add it to your ticket for $1 more per play — times shown are approximate.",
        "bonus": "Powerball",
        "howto": [
            ("<strong>Use an app</strong> — the <a href=\"index.html\" style=\"color:var(--red-700);font-weight:600\">Live Lotto app</a> posts Double Play numbers right after each drawing.",),
            ("<strong>Scan your ticket</strong> — point your phone camera at any ticket for instant win/lose matching.",),
            ("<strong>Save your numbers</strong> — get an automatic alert the moment your numbers hit.",),
        ],
        "cta": "Live results for Powerball, Double Play, Mega Millions and 100+ games in all 50 states — plus ticket scanner and win alerts. Pre-order lifetime access for $9.9.",
        "faq": [
            ("What time is the Double Play drawing?",
             "Double Play drawings are held after each Powerball drawing — Monday, Wednesday and Saturday, at approximately 11:30 PM Eastern Time."),
            ("How is Double Play different from Powerball?",
             "Double Play uses the same 5/69 + 1/26 format but is a separate drawing with its own $10 million top prize. It costs an extra $1 per play, added to a Powerball ticket."),
            ("Where can I check Double Play results?",
             "Results post on Powerball.com after each drawing. The Live Lotto app posts winning numbers instantly, with a ticket scanner and win alerts."),
        ],
    },
    "mega_millions": {
        "name": "Mega Millions",
        "slug": "mega-millions-drawing-time",
        "meta_title": "What Time Is the Mega Millions Drawing? 2026 Schedule & Live Countdown",
        "meta_desc": "Mega Millions drawings are every Tuesday and Friday at 11:00 PM ET. See the next drawing time in your timezone with a live countdown, plus tonight's results and cutoff times.",
        "h1": 'What Time Is the <span>Mega Millions Drawing</span>?',
        "intro": 'Mega Millions draws every <strong>Tuesday and Friday</strong> — here is the next drawing time in your timezone, with a live countdown.',
        "days": [2, 5], "hour": 23, "minute": 0,
        "label": "11:00 PM ET",
        "tz": [("Eastern (ET)", "11:00 PM"), ("Central (CT)", "10:00 PM"),
               ("Mountain (MT)", "9:00 PM"), ("Pacific (PT)", "8:00 PM"),
               ("Alaska (AKT)", "7:00 PM"), ("Hawaii (HT)", "5:00 PM")],
        "cutoff": "<strong>Ticket cutoff:</strong> sales close before draw time depending on your state — commonly 10:45 PM ET, but as early as 9:00 PM ET in some states. Don't wait until the last minute.",
        "bonus": "Mega Ball",
        "howto": [
            ("<strong>Use an app</strong> — the <a href=\"index.html\" style=\"color:var(--red-700);font-weight:600\">Live Lotto app</a> posts winning numbers the second they drop, with jackpot and cash value.",),
            ("<strong>Scan your ticket</strong> — point your phone camera at any ticket for instant win/lose matching instead of comparing numbers by hand.",),
            ("<strong>Save your numbers</strong> — get an automatic alert the moment your numbers hit, so you never miss a win.",),
        ],
        "cta": "Live results for Mega Millions, Powerball and 100+ games in all 50 states — plus ticket scanner and win alerts. Pre-order lifetime access for $9.9.",
        "faq": [
            ("What time is the Mega Millions drawing tonight?",
             "Mega Millions draws every Tuesday and Friday at 11:00 PM Eastern Time (10:00 PM CT / 9:00 PM MT / 8:00 PM PT). Use the live countdown above for the exact time remaining until the next drawing."),
            ("What time is the ticket sales cutoff?",
             "Cutoff times vary by state — commonly 10:45 PM ET on draw nights, but some states close sales earlier. Check your official state lottery site for the exact cutoff where you play."),
            ("Where can I check Mega Millions results?",
             "Results post on megamillions.com and state lottery sites right after each drawing. The Live Lotto app also posts winning numbers instantly, with jackpot amounts and a ticket scanner."),
        ],
    },
    "lotto_america": {
        "name": "Lotto America",
        "slug": "lotto-america-drawing-time",
        "meta_title": "What Time Is the Lotto America Drawing? 2026 Schedule & Live Countdown",
        "meta_desc": "Lotto America drawings are every Monday, Wednesday and Saturday around 10:15 PM ET. See the next drawing time in your timezone with a live countdown and latest results.",
        "h1": 'What Time Is the <span>Lotto America Drawing</span>?',
        "intro": 'Lotto America draws every <strong>Monday, Wednesday and Saturday</strong> — here is the next drawing time in your timezone, with a live countdown.',
        "days": [1, 3, 6], "hour": 22, "minute": 15,
        "label": "10:15 PM ET",
        "tz": [("Eastern (ET)", "10:15 PM"), ("Central (CT)", "9:15 PM"),
               ("Mountain (MT)", "8:15 PM"), ("Pacific (PT)", "7:15 PM"),
               ("Alaska (AKT)", "6:15 PM"), ("Hawaii (HT)", "4:15 PM")],
        "cutoff": "<strong>Ticket cutoff:</strong> sales typically close about an hour before draw time, varying by state. Times shown are approximate — drawings occur around 10:15 PM ET.",
        "bonus": "Star Ball",
        "howto": [
            ("<strong>Use an app</strong> — the <a href=\"index.html\" style=\"color:var(--red-700);font-weight:600\">Live Lotto app</a> posts winning numbers the second they drop.",),
            ("<strong>Scan your ticket</strong> — point your phone camera at any ticket for instant win/lose matching.",),
            ("<strong>Save your numbers</strong> — get an automatic alert the moment your numbers hit.",),
        ],
        "cta": "Live results for Lotto America, Powerball, Mega Millions and 100+ games in all 50 states — plus ticket scanner and win alerts. Pre-order lifetime access for $9.9.",
        "faq": [
            ("What time is the Lotto America drawing?",
             "Lotto America drawings are held every Monday, Wednesday and Saturday at approximately 10:15 PM Eastern Time."),
            ("How do you win Lotto America?",
             "Match 5 numbers from 1–52 plus the Star Ball (1–10) to win the jackpot, which starts at $2 million. There are 9 prize tiers in total."),
            ("Where can I check Lotto America results?",
             "Results post on official state lottery sites after each drawing. The Live Lotto app posts winning numbers instantly, with a ticket scanner and win alerts."),
        ],
    },
    "millionaire_for_life": {
        "name": "Millionaire for Life",
        "slug": "millionaire-for-life-drawing-time",
        "meta_title": "What Time Is the Millionaire for Life Drawing? 2026 Schedule & Countdown",
        "meta_desc": "Millionaire for Life drawings are held nightly at 11:15 PM ET. See tonight's drawing time in your timezone with a live countdown and the latest winning numbers.",
        "h1": 'What Time Is the <span>Millionaire for Life Drawing</span>?',
        "intro": 'Millionaire for Life draws <strong>every night</strong> — here is tonight\'s drawing time in your timezone, with a live countdown.',
        "days": [0, 1, 2, 3, 4, 5, 6], "hour": 23, "minute": 15,
        "label": "11:15 PM ET",
        "tz": [("Eastern (ET)", "11:15 PM"), ("Central (CT)", "10:15 PM"),
               ("Mountain (MT)", "9:15 PM"), ("Pacific (PT)", "8:15 PM"),
               ("Alaska (AKT)", "7:15 PM"), ("Hawaii (HT)", "5:15 PM")],
        "cutoff": "<strong>Ticket cutoff:</strong> sales typically close shortly before draw time, varying by state. The top prize is $1,000,000 a year for life.",
        "bonus": "Millionaire Ball",
        "howto": [
            ("<strong>Use an app</strong> — the <a href=\"index.html\" style=\"color:var(--red-700);font-weight:600\">Live Lotto app</a> posts winning numbers the second they drop.",),
            ("<strong>Scan your ticket</strong> — point your phone camera at any ticket for instant win/lose matching.",),
            ("<strong>Save your numbers</strong> — get an automatic alert the moment your numbers hit.",),
        ],
        "cta": "Live results for Millionaire for Life, Powerball, Mega Millions and 100+ games in all 50 states — plus ticket scanner and win alerts. Pre-order lifetime access for $9.9.",
        "faq": [
            ("What time is the Millionaire for Life drawing?",
             "Millionaire for Life drawings are held every night at 11:15 PM Eastern Time."),
            ("What happened to Lucky for Life and Cash4Life?",
             "Both games were retired in February 2026 and replaced by Millionaire for Life, a multi-state game with a $1,000,000-a-year-for-life top prize."),
            ("Where can I check Millionaire for Life results?",
             "Results post on official state lottery sites after each nightly drawing. The Live Lotto app posts winning numbers instantly, with a ticket scanner and win alerts."),
        ],
    },
}

ORDER = ["powerball", "double_play", "mega_millions", "lotto_america",
         "millionaire_for_life"]

CSS = """<style>
:root{--red-950:#220b0b;--red-900:#3f1010;--red-800:#7f1d1d;--red-700:#b91c1c;--gold:#f0a92e;--ink:#1a1212;--muted:#6a5e5e;--line:#ece5e5;--bg:#fdfbfb;--card:#fff}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Inter',system-ui,sans-serif;color:var(--ink);background:var(--bg);line-height:1.7}
h1,h2{font-family:'Plus Jakarta Sans',system-ui,sans-serif;letter-spacing:-.02em;line-height:1.2}
.wrap{max-width:820px;margin:0 auto;padding:0 24px}
.topbar{background:var(--red-950);color:#fff;padding:14px 0}
.topbar .wrap{display:flex;align-items:center;justify-content:space-between}
.topbar a{color:#fff;font-weight:700;font-size:15px}
.topbar a.cta{background:linear-gradient(135deg,#f7be55,#f0a92e);color:#3d2703;padding:9px 18px;border-radius:10px}
header.hero{background:linear-gradient(160deg,var(--red-950),var(--red-900));color:#fff;padding:64px 0 56px;text-align:center}
header.hero h1{font-size:clamp(30px,5vw,46px);margin-bottom:14px}
header.hero h1 span{color:#f7be55}
header.hero p{color:#f2d9d9;font-size:18px;max-width:620px;margin:0 auto}
.answer{background:var(--card);border:1px solid var(--line);border-radius:18px;box-shadow:0 20px 60px -20px rgba(64,16,16,.25);margin:-34px auto 0;max-width:820px;padding:34px 30px;text-align:center;position:relative}
.answer .label{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--red-700);margin-bottom:8px}
.answer .when{font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(22px,3.6vw,32px);font-weight:800;margin-bottom:14px}
.count{display:flex;justify-content:center;gap:10px;margin-top:6px}
.cd{background:var(--red-950);color:#fff;border-radius:12px;min-width:66px;padding:10px 6px}
.cd b{font-family:'Plus Jakarta Sans',sans-serif;font-size:24px;display:block}
.cd span{font-size:11px;letter-spacing:.08em;color:#d9b3b3}
section{padding:56px 0}
h2{font-size:clamp(24px,3.4vw,32px);margin-bottom:16px}
p{margin-bottom:14px;color:#3a3232}
table{width:100%;border-collapse:collapse;margin:22px 0;background:var(--card);border-radius:14px;overflow:hidden;box-shadow:0 8px 24px -12px rgba(64,16,16,.18)}
th{background:var(--red-900);color:#fff;text-align:left;padding:13px 18px;font-size:14px}
td{padding:13px 18px;border-top:1px solid var(--line);font-size:15px}
td:first-child{font-weight:700}
.note{background:#fdf3df;border:1px solid #f0d9a8;border-radius:14px;padding:18px 22px;font-size:15px;margin:20px 0}
.note strong{color:#7a5410}
.results{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 26px;margin:20px 0}
.results .nums{font-family:'Plus Jakarta Sans',sans-serif;font-size:26px;font-weight:800;letter-spacing:.04em;margin:8px 0}
.results .nums span{color:var(--red-700)}
.cta-box{background:linear-gradient(150deg,var(--red-900),var(--red-800));border-radius:20px;color:#fff;padding:44px 36px;text-align:center;margin:20px 0}
.cta-box h2{color:#fff;margin-bottom:10px}
.cta-box p{color:#f2d9d9;max-width:520px;margin:0 auto 24px}
.btn{display:inline-block;font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;background:linear-gradient(135deg,#f7be55,#f0a92e);color:#3d2703;padding:15px 32px;border-radius:14px;font-size:16px}
.faq{border:1px solid var(--line);border-radius:14px;margin-bottom:12px;background:#fff}
.faq summary{cursor:pointer;font-weight:700;font-size:16px;padding:20px 24px;list-style:none;display:flex;justify-content:space-between;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-size:22px;color:var(--red-700)}
.faq[open] summary::after{content:"–"}
.faq .a{padding:0 24px 22px;color:var(--muted);font-size:15px}
footer{background:var(--red-950);color:#a17f7f;font-size:13px;padding:40px 0;line-height:1.7}
footer strong{color:#f2d9d9}
footer nav a{color:#f7be55;margin-right:14px}
</style>"""

JS_TMPL = """<script>
function etParts(ms){
  var map={Sun:0,Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6};
  var p=Object.fromEntries(new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',weekday:'short',year:'numeric',month:'numeric',day:'numeric',hour:'numeric',minute:'numeric',hour12:false}).formatToParts(new Date(ms)).map(function(x){return [x.type,x.value];}));
  return {wd:map[p.weekday],y:+p.year,mo:+p.month,d:+p.day};
}
function etOffsetMs(ms){
  var dtf=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false});
  var p=Object.fromEntries(dtf.formatToParts(new Date(ms)).map(function(x){return [x.type,x.value];}));
  var asUTC=Date.UTC(+p.year,+p.month-1,+p.day,(+p.hour)%24,+p.minute,+p.second);
  return ms-asUTC;
}
function nextDraw(){
  var now=Date.now(),days=__DAYS__;
  for(var i=0;i<8;i++){
    var probe=now+i*864e5, ep=etParts(probe);
    if(days.indexOf(ep.wd)===-1) continue;
    var drawMs=Date.UTC(ep.y,ep.mo-1,ep.d,__H__,__M__,0)+etOffsetMs(probe);
    if(drawMs>now) return {ms:drawMs,y:ep.y,mo:ep.mo,d:ep.d};
  }
  return null;
}
var DAYS=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
var MON=['January','February','March','April','May','June','July','August','September','October','November','December'];
var nd=nextDraw();
if(nd){
  var ep=etParts(nd.ms);
  var today=etParts(Date.now());
  var label=(ep.y===today.y&&ep.mo===today.mo&&ep.d===today.d)?"Tonight":DAYS[ep.wd];
  document.getElementById('when').textContent=label+', '+MON[ep.mo-1]+' '+ep.d+' at __LABEL__';
  (function tick(){
    var diff=Math.max(0,nd.ms-Date.now());
    var d=Math.floor(diff/864e5),h=Math.floor(diff%864e5/36e5),m=Math.floor(diff%36e5/6e4),s=Math.floor(diff%6e4/1e3);
    document.getElementById('cd-d').textContent=String(d).padStart(2,'0');
    document.getElementById('cd-h').textContent=String(h).padStart(2,'0');
    document.getElementById('cd-m').textContent=String(m).padStart(2,'0');
    document.getElementById('cd-s').textContent=String(s).padStart(2,'0');
    setTimeout(tick,1000);
  })();
}
</script>"""

PAGE_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__META_TITLE__</title>
<meta name="description" content="__META_DESC__">
<link rel="canonical" href="__BASE__/__SLUG__.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
__CSS__
__FAQ_JSONLD__
</head>
<body>
<div class="topbar"><div class="wrap"><a href="index.html">← Live Lotto</a><a class="cta" href="index.html#pricing">Get the App — $9.9</a></div></div>
<header class="hero"><div class="wrap">
<h1>__H1__</h1>
<p>__INTRO__</p>
</div></header>
<div class="wrap"><div class="answer">
<div class="label">Next drawing</div>
<div class="when" id="when">—</div>
<div class="count"><div class="cd"><b id="cd-d">00</b><span>DAYS</span></div><div class="cd"><b id="cd-h">00</b><span>HOURS</span></div><div class="cd"><b id="cd-m">00</b><span>MIN</span></div><div class="cd"><b id="cd-s">00</b><span>SEC</span></div></div>
</div></div>
<section><div class="wrap">
<h2>__NAME__ drawing schedule by timezone</h2>
<p>Every drawing happens at the same moment nationwide — <strong>__LABEL__</strong>. Here is what that means where you live:</p>
<table><tr><th>Timezone</th><th>Drawing time</th></tr>
__TZ_ROWS__</table>
<div class="note">__CUTOFF__</div>
__RESULTS_BLOCK__
<h2>How to check results fast</h2>
__HOWTO__
<div class="cta-box">
<h2>Never miss a drawing again</h2>
<p>__CTA__</p>
<a class="btn" href="index.html#pricing">Get Lifetime Access — $9.9</a>
</div>
<h2>__NAME__ drawing FAQs</h2>
__FAQ_HTML__
<p style="font-size:13px;color:var(--muted);margin-top:18px">Results updated __UPDATED__. Numbers shown are for informational purposes — always verify with your official state lottery.</p>
</div></section>
<footer><div class="wrap">
<nav>__FOOTNAV__</nav><br>
<strong>Disclaimer:</strong> This page is for informational purposes only and is not affiliated with any lottery organization or state lottery. Always verify winning numbers with your official state lottery. Must be 18+ (21+ in some states). Play responsibly — <strong>1-800-GAMBLER</strong>.<br><br>
© 2026 Live Lotto Draw Results · <a href="index.html" style="color:#f7be55">Back to pre-sale page</a>
</div></footer>
__JS__
</body>
</html>
"""


def faq_jsonld(g):
    items = []
    for q, a in g["faq"]:
        qe = q.replace('"', '\\"')
        ae = a.replace('"', '\\"')
        items.append(f'{{"@type":"Question","name":"{qe}","acceptedAnswer":{{"@type":"Answer","text":"{ae}"}}}}')
    return ('<script type="application/ld+json">\n{"@context":"https://schema.org",'
            '"@type":"FAQPage","mainEntity":[' + ",".join(items) + "]}\n</script>")


def fmt_date(iso):
    dt = datetime.strptime(iso, "%Y-%m-%d")
    return dt.strftime("%A, %B %-d, %Y")


def render(key, g, results):
    rec = results.get(key)
    if rec:
        nums = " &nbsp;".join(rec["numbers"])
        results_block = (
            '<h2>Latest results — ' + fmt_date(rec["date"]) + '</h2>\n'
            '<div class="results">\n'
            '<div class="label" style="font-size:13px;font-weight:700;letter-spacing:.12em;'
            'text-transform:uppercase;color:var(--red-700)">Winning numbers</div>\n'
            f'<div class="nums">{nums} &nbsp;<span>● {rec["bonus"]}</span></div>\n'
            '</div>\n'
        )
        updated = fmt_date(rec["date"])
    else:
        results_block = ""
        updated = "recently"
    tz_rows = "\n".join(f"<tr><td>{t}</td><td>{v}</td></tr>" for t, v in g["tz"])
    howto = "\n".join(f"<p>{i + 1}. {h[0]}</p>" for i, h in enumerate(g["howto"]))
    faq_html = "\n".join(
        f'<details class="faq"><summary>{q}</summary><div class="a">{a}</div></details>'
        for q, a in g["faq"])
    footnav = "\n".join(
        f'<a href="{GAMES[k]["slug"]}.html">{GAMES[k]["name"]}</a>'
        for k in ORDER if k != key)
    js = (JS_TMPL.replace("__DAYS__", str(g["days"]))
                .replace("__H__", str(g["hour"]))
                .replace("__M__", str(g["minute"]))
                .replace("__LABEL__", g["label"]))
    page = PAGE_TMPL
    for token, val in [
        ("__META_TITLE__", g["meta_title"]), ("__META_DESC__", g["meta_desc"]),
        ("__BASE__", BASE), ("__SLUG__", g["slug"]), ("__CSS__", CSS),
        ("__FAQ_JSONLD__", faq_jsonld(g)), ("__H1__", g["h1"]),
        ("__INTRO__", g["intro"]), ("__NAME__", g["name"]),
        ("__LABEL__", g["label"]), ("__TZ_ROWS__", tz_rows),
        ("__CUTOFF__", g["cutoff"]), ("__RESULTS_BLOCK__", results_block),
        ("__HOWTO__", howto), ("__CTA__", g["cta"]),
        ("__FAQ_HTML__", faq_html), ("__UPDATED__", updated),
        ("__FOOTNAV__", footnav), ("__JS__", js),
    ]:
        page = page.replace(token, val)
    return page


def main():
    results = json.loads(DATA_FILE.read_text()) if DATA_FILE.exists() else {}
    for key in ORDER:
        g = GAMES[key]
        html = render(key, g, results)
        out = ROOT / f'{g["slug"]}.html'
        out.write_text(html)
        print("wrote", out.name, len(html), "bytes")
    # sitemap
    urls = [(f"{BASE}/", "weekly", "1.0")] + [
        (f'{BASE}/{GAMES[k]["slug"]}.html', "daily", "0.8") for k in ORDER]
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{u}</loc><changefreq>{c}</changefreq>"
                    f"<priority>{p}</priority></url>\n" for u, c, p in urls)
          + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(sm)
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
