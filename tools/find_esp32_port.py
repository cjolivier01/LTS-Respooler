#!/usr/bin/env python3
"""Print the most likely ESP32 serial port for Makefile targets."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

try:
    from serial.tools import list_ports
except ImportError as exc:
    print(f"pyserial is required: {exc}", file=sys.stderr)
    sys.exit(1)


ESPRESSIF_VIDS = {0x303A}
COMMON_UART_VIDS = {
    0x0403,  # FTDI
    0x10C4,  # Silicon Labs CP210x
    0x1A86,  # WCH CH34x/CH91xx
}
KEYWORDS = (
    "espressif",
    "esp32",
    "usb jtag",
    "usb-jtag",
    "cp210",
    "ch340",
    "ch910",
    "ch343",
    "ftdi",
)


def stable_symlink(device: str) -> str:
    """Prefer a stable /dev/serial/by-id name when one exists."""
    by_id = Path("/dev/serial/by-id")
    if not by_id.is_dir():
        return device

    try:
        target = os.path.realpath(device)
    except OSError:
        return device

    matches: list[str] = []
    for entry in by_id.iterdir():
        try:
            if os.path.realpath(entry) == target:
                matches.append(str(entry))
        except OSError:
            continue

    if not matches:
        return device

    matches.sort(
        key=lambda path: (
            0 if "Espressif" in path or "esp" in path.lower() else 1,
            path,
        )
    )
    return matches[0]


def score_port(port: object) -> int:
    """Rank native ESP USB first, then common USB-to-UART adapters."""
    text = " ".join(
        value
        for value in (
            getattr(port, "description", None),
            getattr(port, "manufacturer", None),
            getattr(port, "product", None),
            getattr(port, "hwid", None),
        )
        if value
    ).lower()

    score = 0
    if getattr(port, "vid", None) in ESPRESSIF_VIDS:
        score += 100
    if getattr(port, "vid", None) in COMMON_UART_VIDS:
        score += 30
    if any(keyword in text for keyword in KEYWORDS):
        score += 25
    device = getattr(port, "device", "")
    if device.startswith("/dev/ttyACM") or device.startswith("/dev/ttyUSB"):
        score += 10
    if "jtag" in text:
        score += 20
    return score


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="print all candidates")
    args = parser.parse_args()

    candidates = []
    for port in list_ports.comports():
        score = score_port(port)
        if score > 0:
            candidates.append((score, stable_symlink(port.device), port))

    candidates.sort(key=lambda item: (-item[0], item[1]))
    if not candidates:
        return 1

    if args.all:
        for score, path, port in candidates:
            print(f"{path}\tscore={score}\tdescription={port.description}")
    else:
        print(candidates[0][1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
