#!/usr/bin/env python3
"""Render the DIY perfboard SVG drawings to their checked-in PNG previews."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DRAWING_DIR = PROJECT_ROOT / "DIY_Perfboard"
BROWSER_NAMES = (
    "google-chrome-stable",
    "google-chrome",
    "chromium",
    "chromium-browser",
)
PIXEL_DIMENSION = re.compile(r"^(\d+)(?:px)?$")


def find_browser() -> str:
    override = os.environ.get("DRAWING_BROWSER")
    if override:
        path = shutil.which(override)
        if path:
            return path
        raise RuntimeError(f"DRAWING_BROWSER is not executable: {override}")

    for name in BROWSER_NAMES:
        path = shutil.which(name)
        if path:
            return path

    names = ", ".join(BROWSER_NAMES)
    raise RuntimeError(
        f"Chrome or Chromium is required to render the drawings; tried: {names}"
    )


def svg_dimensions(svg_path: Path) -> tuple[int, int]:
    root = ET.parse(svg_path).getroot()
    values = []
    for attribute in ("width", "height"):
        value = root.get(attribute, "")
        match = PIXEL_DIMENSION.fullmatch(value)
        if not match:
            raise RuntimeError(
                f"{svg_path.name} must have an integer-pixel {attribute} attribute"
            )
        values.append(int(match.group(1)))
    return values[0], values[1]


def render_svg(browser: str, svg_path: Path, png_path: Path) -> None:
    width, height = svg_dimensions(svg_path)
    command = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--window-size={width},{height}",
        f"--screenshot={png_path}",
        svg_path.resolve().as_uri(),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0 or not png_path.is_file():
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"failed to render {svg_path.name}: {detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail instead of updating PNG files when rendered output differs",
    )
    args = parser.parse_args()

    svg_paths = sorted(DRAWING_DIR.glob("*.svg"))
    if not svg_paths:
        print(f"No SVG drawings found in {DRAWING_DIR}", file=sys.stderr)
        return 1

    try:
        browser = find_browser()
        stale: list[Path] = []
        with tempfile.TemporaryDirectory(prefix="lts-drawings-") as temp_name:
            temp_dir = Path(temp_name)
            for svg_path in svg_paths:
                png_path = svg_path.with_suffix(".png")
                rendered_path = temp_dir / png_path.name
                render_svg(browser, svg_path, rendered_path)

                if png_path.is_file() and png_path.read_bytes() == rendered_path.read_bytes():
                    print(f"Current: {png_path.relative_to(PROJECT_ROOT)}")
                    continue

                if args.check:
                    stale.append(png_path)
                else:
                    os.replace(rendered_path, png_path)
                    print(f"Rendered: {png_path.relative_to(PROJECT_ROOT)}")

        if stale:
            for path in stale:
                print(f"Stale: {path.relative_to(PROJECT_ROOT)}", file=sys.stderr)
            print("Run 'make drawings' to update the PNG previews.", file=sys.stderr)
            return 1
    except (OSError, RuntimeError, ET.ParseError) as exc:
        print(f"Drawing render failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
