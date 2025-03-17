#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import subprocess
import sys

from pathlib import Path

import compress_image_fb2


DIR = Path(__file__).resolve().parent

for f in (DIR / "examples").glob("*.fb2"):
    if f.name.startswith("compress_"):
        continue

    print(f"RUN: {f}")
    try:
        result: str = subprocess.check_output(
            args=[
                sys.executable,
                compress_image_fb2.__file__,
                f,
            ],
            encoding="utf-8",
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        result: str = e.output

    print(result)

    print("\n" + ("-" * 10) + "\n")
