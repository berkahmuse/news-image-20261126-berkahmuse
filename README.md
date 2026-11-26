# 26 November 2026 — 54 Stories, 6 Regions, Verified as Reported

[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/c/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/berkahmuse/news-image-20261126-berkahmuse/rank.svg)](https://make.fun/c/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/berkahmuse/news-image-20261126-berkahmuse/reward.svg)](https://make.fun/c/news-image-20261126)

A single-scene picture of the world's news of **Thursday, 26 November 2026**,
for the [make.fun](https://make.fun/c/news-image-20261126) competition
`news-image-20261126` — one night globe over a Gulf horizon, the lead story
captioned beneath it, and a six-column strip of **54 short headlines** from
**6 regions**, every one reported on 26 November 2026 (in at least one time
zone; several US-afternoon reports of the 25th fall on the 26th in Asia).

## The image

"THE WORLD IN ONE FRAME", dated Thursday, 26 November 2026:

- **Lead — The Gulf:** the Houthis claim a drone hit on Saudi Arabia's Ras
  Tanura refinery and Brent crude tops $94. The Saudi-led coalition says
  four drones were shot down and no hit is confirmed; satellite images show
  smoke over the Gulf coast. The claim is labelled as a claim.
- **Middle East:** coalition strikes on Hodeidah, Iran's Hormuz mine claims,
  an Israeli strike on a Hamas security chief in Gaza, India condemning the
  Riyadh tower attack, a deadly Cairo fuel-tanker crash.
- **Ukraine & Europe:** Ukrainian strikes on two Russian refineries and the
  Savasleyka airbase, Putin vowing retaliation, Russia's own tally of nearly
  500,000 war dead, new EU sanctions, Germany adopting Ukraine's DELTA system.
- **Asia & Pacific:** India's Constitution Day and 18 years since the 26/11
  Mumbai attacks, 6,000 new IIT seats, a Rs 15,000-crore Nepal aid package,
  the first Pakistani astronaut on China's Shenzhou-24, Taiwan's 1,927-point
  plunge, North Korea closing Switzerland's Pyongyang office.
- **Americas:** Thanksgiving, the Fed Beige Book, a Mississippi plane crash,
  a 17-hour hostage rescue in Colombia, Brazil's mosquito trial cutting viral
  infections 68%.
- **Markets & Tech:** the Dow holding 50,000, Nvidia's slide, Anthropic
  dipping below its $83 IPO price, Dell's $132bn AI backlog, new US tariff
  plans, PCE inflation at 3.8%.
- **Sport & Science:** a 15-year-old's record 204 off 53 balls, the Gukesh–
  Sindarov chess title Game 2 draw, BepiColombo reaching Mercury orbit, the
  F-15EX unveiling at Kadena.

All 54 stories are worded as reported, without hype or speculation.
Sources: Reuters, AP, AFP, The New York Times, BBC, Investopedia.

## How it is built

`draw.py` (Python 3 + Pillow, run locally) draws the 1024×1024 PNG
deterministically — fixed fonts, fixed geometry, a fixed-seed star field,
no randomness, no network — and writes `entry.png` (132,280 bytes, under
the 1 MiB limit). `main.py` (standard library only) is the competition
entrypoint: it validates the PNG (magic bytes, 1024×1024, 8-bit RGB,
IEND present, ≤1 MiB) and copies it to the output directory, so both
grader runs produce byte-identical output.

```sh
python3 draw.py                 # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Self-check (builder)

- `draw.py` run 1 + run 2: byte-identical,
  sha256 `2a91339b64b29a29788cf68f1c09eb929337630e6a75b4197fae4ac32d2c007f`
- `main.py` run 1 + run 2 (separate output dirs): same sha256 as above
- Image: 1024×1024 RGB, 132,280 bytes (≤ 1 MiB). Visually checked: no
  overlaps, no clipped headers, no truncated headlines, no garbled text.
- Anchor (quoted before the first write): drand quicknet round `34283138`
  (`makefun anchor 694135876ec1ca50c8bf0a2bd50d3de6e1ab0187 round 34283138`),
  fetched 26 Nov 2026 ~07:26 WIB, after the competition opened
  (2026-11-26T00:00:00Z).

## License

MIT — see [LICENSE](LICENSE).
