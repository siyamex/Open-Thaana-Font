#!/usr/bin/env python3
"""
Build every distributable format from the UFO source.

The UFO in sources/ is the source of truth. Edit that, then run this; do
not edit the compiled fonts directly, because the next build overwrites
them.

    pip install -r requirements.txt
    python build.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SOURCES = ROOT / "sources"
FONTS = ROOT / "fonts"


def find_source() -> Path:
    ufos = sorted(SOURCES.glob("*.ufo"))
    if not ufos:
        sys.exit("No .ufo found in sources/")
    return ufos[0]


def compile_binaries(ufo: Path) -> None:
    """fontmake compiles the UFO to TTF and OTF."""
    for fmt, out_dir in (("ttf", FONTS / "ttf"), ("otf", FONTS / "otf")):
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"  building {fmt} ...")
        subprocess.run(
            [
                sys.executable, "-m", "fontmake",
                "-u", str(ufo),
                "-o", fmt,
                "--output-dir", str(out_dir),
                "--verbose", "WARNING",
            ],
            check=True,
        )


def make_webfonts() -> None:
    """Repack the TTF as WOFF and WOFF2. WOFF2 needs the brotli package."""
    from fontTools.ttLib import TTFont

    sources = sorted((FONTS / "ttf").glob("*.ttf"))
    if not sources:
        sys.exit("No TTF to repack; did the compile step run?")

    for flavor in ("woff", "woff2"):
        out_dir = FONTS / flavor
        out_dir.mkdir(parents=True, exist_ok=True)
        for ttf in sources:
            font = TTFont(str(ttf))
            font.flavor = flavor
            target = out_dir / (ttf.stem + "." + flavor)
            font.save(str(target))
            print(f"  wrote {target.relative_to(ROOT)}")


def verify() -> None:
    """Open everything that was built and check Thaana coverage."""
    from fontTools.ttLib import TTFont

    ok = True
    for path in sorted(FONTS.rglob("*")):
        if path.suffix not in (".ttf", ".otf", ".woff", ".woff2"):
            continue
        font = TTFont(str(path))
        cmap = font.getBestCmap()
        missing = [cp for cp in range(0x0780, 0x07B2) if cp not in cmap]
        status = "ok" if not missing else f"MISSING {len(missing)} glyphs"
        if missing:
            ok = False
        print(f"  {path.relative_to(ROOT)}: {status}")
    if not ok:
        sys.exit("Some builds are missing Thaana coverage.")


def main() -> None:
    ufo = find_source()
    print(f"Source: {ufo.relative_to(ROOT)}")

    if FONTS.exists():
        shutil.rmtree(FONTS)

    print("Compiling binaries")
    compile_binaries(ufo)

    print("Building web fonts")
    make_webfonts()

    print("Verifying")
    verify()

    print("\nDone. Installable fonts are in fonts/.")


if __name__ == "__main__":
    main()
