#!/usr/bin/env python3
"""Competition entrypoint for news-image-20261126 (Python 3.13, stdlib only).

Writes the shipped entry.png to the output directory. Before copying it
validates the file so a broken build fails loudly instead of submitting
a corrupt image:

  * PNG magic bytes (89 50 4E 47 0D 0A 1A 0A)
  * IHDR width/height are 1024x1024, bit depth 8, colour type 2 (RGB)
  * file size is at most 1 MiB (1048576 bytes)
  * the IEND chunk is present (whole image, nothing truncated)

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
The program is deterministic: the same input bytes always produce the
same output bytes (a straight copy of a fixed file).
"""
import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print(f"main.py: {msg}", file=sys.stderr)
    raise SystemExit(1)


def validate_png(data):
    if len(data) < 33 or data[:8] != PNG_MAGIC:
        fail("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    width, height, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        fail(f"entry.png is {width}x{height}, expected 1024x1024")
    if (depth, ctype) != (8, 2):
        fail(f"unexpected PNG bit depth {depth} / colour type {ctype}")
    if not data.rstrip(b"\x00").endswith(b"IEND\xaeB`\x82"):
        fail("entry.png has no IEND chunk (truncated image)")
    return width, height


def main():
    if not SRC.is_file():
        fail("entry.png missing next to main.py")
    data = SRC.read_bytes()
    width, height = validate_png(data)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    out.write_bytes(data)
    print(f"wrote {out} ({len(data)} bytes, {width}x{height} PNG)")


if __name__ == "__main__":
    main()
