#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news image (1024x1024 PNG).

Deterministic: fixed fonts, fixed geometry, a fixed-seed star field,
no randomness from the environment, no network. Run:
    python3 draw.py            -> writes entry.png next to this file.

Design (my own, single scene + data strip): a night globe over a Gulf
horizon -- one clean picture of the day -- with the lead story captioned
beneath it and a six-column strip of 54 short headlines below. Every
story was reported on 26 November 2026 (in at least one time zone; several
US-afternoon reports of the 25th fall on the 26th in Asia) and is worded
as reported, without hype or speculation. Claims are labelled as claims.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

# --- palette ---
NAVY = (13, 27, 46)        # masthead / night sky top
SKY_MID = (38, 74, 99)     # sky middle
HORIZON = (214, 148, 74)   # dusk amber at the horizon
SEA = (16, 48, 63)         # sea band
SEA_DK = (10, 34, 46)
CREAM = (246, 241, 230)
PAPER = (250, 247, 238)    # strip background
INK = (24, 26, 30)
MUTED = (92, 96, 104)
GOLD = (198, 148, 52)
GOLD_LT = (232, 196, 110)
CRIMSON = (172, 52, 40)
TEAL = (16, 110, 110)
GREEN = (46, 110, 66)
SLATE = (70, 84, 104)
OCEAN = (31, 78, 121)      # globe ocean
LAND = (127, 176, 105)     # globe land
LAND_DK = (94, 143, 80)
SMOKE = (190, 190, 186)
LEAD_BG = (18, 38, 58)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_sky(d):
    """Night sky gradient, masthead to horizon (y 92..470)."""
    top, mid, bot = NAVY, SKY_MID, HORIZON
    for y in range(92, 471):
        if y < 280:
            t = (y - 92) / (280 - 92)
            c = lerp(top, mid, t)
        else:
            t = (y - 280) / (471 - 280)
            c = lerp(mid, bot, t)
        d.line([(0, y), (W, y)], fill=c)


def draw_stars(d):
    rng = random.Random(20261126)
    for _ in range(46):
        x = rng.randint(8, 1016)
        y = rng.randint(100, 300)
        r = rng.choice([1, 1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 238, 245))
    # a few bright stars with cross sparkle
    for (x, y) in [(120, 140), (905, 210), (700, 120), (250, 250)]:
        d.line([(x - 5, y), (x + 5, y)], fill=(255, 246, 220), width=1)
        d.line([(x, y - 5), (x, y + 5)], fill=(255, 246, 220), width=1)


def draw_moon(d):
    cx, cy, r = 884, 158, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 234, 214))
    d.ellipse([cx - r + 12, cy - r + 4, cx + r - 4, cy + r - 12], fill=(226, 214, 184))
    for (x, y, cr) in [(cx - 12, cy - 8, 5), (cx + 6, cy + 10, 4), (cx - 2, cy - 16, 3)]:
        d.ellipse([x - cr, y - cr, x + cr, y + cr], fill=(214, 200, 168))


def draw_globe(d):
    """One globe: ocean disc, simplified continents, graticule, orbit ring."""
    cx, cy, r = 512, 312, 148
    # orbit ring (tilted ellipse) behind globe
    d.ellipse([cx - 235, cy - 52, cx + 235, cy + 52], outline=GOLD_LT, width=2)
    # ocean
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN)
    # continents: simplified blobs (abstract, recognisable layout)
    # North America
    d.ellipse([cx - 128, cy - 88, cx - 52, cy - 18], fill=LAND)
    d.polygon([(cx - 118, cy - 40), (cx - 66, cy - 52), (cx - 58, cy - 8),
               (cx - 96, cy + 6), (cx - 122, cy - 14)], fill=LAND)
    # South America
    d.polygon([(cx - 62, cy + 18), (cx - 30, cy + 12), (cx - 22, cy + 66),
               (cx - 40, cy + 96), (cx - 58, cy + 58)], fill=LAND_DK)
    # Africa
    d.polygon([(cx - 6, cy - 42), (cx + 46, cy - 48), (cx + 58, cy - 6),
               (cx + 34, cy + 44), (cx + 2, cy + 30), (cx - 12, cy - 6)], fill=LAND)
    # Eurasia
    d.polygon([(cx + 48, cy - 96), (cx + 128, cy - 92), (cx + 138, cy - 40),
               (cx + 96, cy - 18), (cx + 60, cy - 52)], fill=LAND_DK)
    # Australia
    d.ellipse([cx + 96, cy + 52, cx + 132, cy + 82], fill=LAND)
    # graticule: equator + two meridians clipped by the disc edge
    d.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=(255, 255, 255, 60), width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=1)
    d.line([(cx, cy - r), (cx, cy + r)], fill=(255, 255, 255), width=1)
    d.ellipse([cx - 74, cy - r, cx + 74, cy + r], outline=(255, 255, 255), width=1)
    # outline + soft shadow
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(10, 20, 34), width=3)
    # six region dots on the orbit ring (ring: x = 512 + 235*cos t,
    # y = 312 + 52*sin t, at t = -150, -120, -60, -30, 30, 150 degrees)
    for (x, y) in [(308, 286), (395, 267), (630, 267),
                   (715, 286), (715, 338), (308, 338)]:
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=GOLD, outline=(255, 255, 255), width=1)


def draw_sea(d):
    """Sea band with a tanker (left) and a refinery (right) on the horizon."""
    d.rectangle([0, 460, W, 560], fill=SEA)
    for y in (478, 496, 516, 536):
        d.line([(0, y), (W, y)], fill=SEA_DK, width=1)
    # tanker silhouette, left
    d.polygon([(60, 500), (260, 500), (276, 524), (44, 524)], fill=(8, 18, 28))
    d.rectangle([196, 472, 236, 500], fill=(8, 18, 28))
    d.rectangle([206, 458, 226, 472], fill=(8, 18, 28))
    d.line([(150, 500), (150, 470)], fill=(8, 18, 28), width=3)
    # refinery silhouette, right
    d.rectangle([760, 486, 980, 524], fill=(8, 18, 28))
    for x in (790, 830, 870, 910):
        d.rectangle([x, 452, x + 10, 486], fill=(8, 18, 28))
    d.polygon([(950, 486), (962, 440), (974, 486)], fill=(8, 18, 28))
    # flare
    d.ellipse([956, 428, 970, 442], fill=(255, 176, 66))
    d.ellipse([959, 431, 967, 439], fill=(255, 226, 140))
    # thin smoke column over the refinery
    for i, (sx, sy, sr) in enumerate([(968, 420, 7), (972, 398, 9), (968, 374, 11), (974, 350, 12)]):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SMOKE)


def draw_masthead(d):
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.rectangle([0, 88, W, 92], fill=GOLD)
    d.text((24, 14), "THE WORLD IN ONE FRAME", font=SERIF_B(40), fill=CREAM)
    d.text((24, 60), "One day. One picture. The news that mattered.",
           font=SERIF(15), fill=(178, 190, 204))
    d.text((W - 24, 12), "THURSDAY", font=SANS_B(17), fill=GOLD_LT, anchor="ra")
    d.text((W - 24, 34), "26 NOVEMBER 2026", font=SANS_B(24), fill=CREAM, anchor="ra")
    d.text((W - 24, 64), "54 STORIES  ·  6 REGIONS", font=SANS_B(13),
           fill=(178, 190, 204), anchor="ra")


def draw_lead(d):
    d.rectangle([0, 560, W, 648], fill=LEAD_BG)
    d.rectangle([0, 560, 10, 648], fill=GOLD)
    d.text((28, 572), "LEAD  —  THE GULF", font=SANS_B(13), fill=GOLD_LT)
    d.text((28, 592), "Houthis claim Ras Tanura refinery hit; Brent tops $94",
           font=SANS_B(25), fill=(255, 255, 255))
    d.text((28, 622), "Saudi coalition says four drones were shot down; satellite images show smoke over the Gulf coast.",
           font=SANS(14), fill=(198, 208, 220))


COLUMNS = [
    ("MIDDLE EAST", CRIMSON, [
        "Houthis claim Ras Tanura refinery hit; Brent tops $94",
        "Saudi coalition: 4 drones downed, no hit confirmed",
        "Coalition hits Hodeidah; Houthis threaten Jeddah",
        "Iran: 3 tankers hit mines in Hormuz, unconfirmed",
        "Iran signals Hormuz deal via Qatar mediators",
        "Israel kills Hamas chief Abuelouf in Gaza",
        "India condemns Riyadh tower strike; 2 Indians hurt",
        "Cairo fuel-tanker crash kills at least 30",
        "Emirates named the world's top airline",
    ]),
    ("UKRAINE & EUROPE", (31, 78, 121), [
        "Ukraine hits 2 refineries; Putin vows payback",
        "Savasleyka raid hits 5 Russian jets",
        "Russia's own tally: nearly 500,000 war dead",
        "EU drafts new sanctions as refineries burn",
        "Germany adopts Ukraine's DELTA system",
        "Europe's rearmament still depends on US arms",
        "Ukraine seeks 40 more F-16s, Kyiv says",
        "ECB accounts, German confidence data due today",
    ]),
    ("ASIA & PACIFIC", TEAL, [
        "Constitution Day; 18 years since 26/11 attacks",
        "IITs add 6,000 seats in robotics, AI and space",
        "India unveils Rs 15,000-cr Nepal aid",
        "First Pakistani astronaut joins China's Shenzhou-24",
        "Hasina asks to return to Bangladesh on Dec 16",
        "Bangladesh raises garment wage by 36%",
        "N. Korea closes Swiss office in Pyongyang",
        "Taiwan stocks plunge 1,927 pts; NT$ past 33",
        "Solomons-Australia security treaty signed",
        "Xi graft probe shakes Shanghai's rising star",
    ]),
    ("AMERICAS", (146, 104, 24), [
        "US marks Thanksgiving; markets closed for the day",
        "US attorney general dodges Nvidia questions",
        "Meta faces Congress over suspended accounts",
        "Mississippi crash kills 6, incl. 2 children",
        "Colombia police free 20 hostages after 17 hours",
        "UN hails Colombia's decade of peace",
        "Brazil mosquito trial cuts viral infections 68%",
        "US intel hacking probe: early trace points to China",
        "Fed Beige Book: modest growth, sticky prices",
    ]),
    ("MARKETS & TECH", SLATE, [
        "Dow holds 50,000; worst Nov since 2008 looms",
        "Nvidia slides about 5%; chips lead AI sell-off",
        "Anthropic dips below $83 IPO, then recovers",
        "Dell's record $132bn AI backlog can't lift shares",
        "US tariffs: up to 15% on Taiwan, 20% on China eyed",
        "US unveils tariff plan for 14 trading partners",
        "PCE inflation 3.8%; Q3 GDP revised up to 4.3%",
        "US curbs remote AI-chip access; B300s seek buyers",
        "Bitcoin near $59,000 as gold and silver slip",
    ]),
    ("SPORT & SCIENCE", GREEN, [
        "Sooryavanshi, 15, hits record 204 off 53 balls",
        "Gukesh-Sindarov Game 2: 20-move draw",
        "IPL 2027 auction draws 1,220 player entries",
        "BepiColombo reaches Mercury orbit after 8 years",
        "Asteroid close-ups from DART test to be revealed",
        "Duran Duran guitarist Andy Taylor dies at 65",
        "Ramayana passes Rs 1,000 crore on day 20",
        "Flipkart CEO to step down in December",
        "US Air Force unveils F-15EX fighters at Kadena",
    ]),
]


def draw_strip(d):
    d.rectangle([0, 648, W, 978], fill=PAPER)
    d.line([(0, 648), (W, 648)], fill=GOLD, width=2)
    margin, gap = 16, 10
    col_w = (W - 2 * margin - 5 * gap) // 6
    head_f = SANS_B(12)
    item_f = SANS(11)
    y0 = 660
    for i, (title, color, items) in enumerate(COLUMNS):
        x = margin + i * (col_w + gap)
        d.rectangle([x, y0, x + col_w, y0 + 20], fill=color)
        d.text((x + 6, y0 + 4), title, font=head_f, fill=(255, 255, 255))
        y = y0 + 28
        for n, item in enumerate(items, 1):
            lines = wrap(d, f"{n}. {item}", item_f, col_w - 4)
            assert len(lines) <= 2, f"headline too long, truncates: {item}"
            for ln in lines:
                d.text((x + 2, y), ln, font=item_f, fill=INK)
                y += 13
            y += 2
        assert y <= 972, f"column {title} overflows: {y}"


def draw_footer(d):
    d.rectangle([0, 978, W, H], fill=NAVY)
    d.text((16, 988), "All 54 stories reported on 26 November 2026  ·  Sources: Reuters, AP, AFP, NYT, BBC, Investopedia",
           font=SANS(12), fill=(178, 190, 204))
    d.text((W - 16, 988), "news-image-20261126  ·  make.fun  ·  @berkahmuse",
           font=SANS(12), fill=GOLD_LT, anchor="ra")


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    draw_sky(d)
    draw_stars(d)
    draw_moon(d)
    draw_globe(d)
    draw_sea(d)
    draw_masthead(d)
    draw_lead(d)
    draw_strip(d)
    draw_footer(d)
    total = sum(len(items) for _, _, items in COLUMNS)
    assert total == 54, f"story count {total} != 54"
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {total} stories)")


if __name__ == "__main__":
    main()
