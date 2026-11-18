#!/usr/bin/env python3
"""news-image-20261118 entry: copy the artwork to /output/entry.png.

The artwork is entry.png beside this file: a one-page newspaper front
page summing up Wednesday 18 November 2026 in four stories (Iran drones
hit a US radar in Bahrain, Nvidia doubles revenue, UK sanctions
settlement firms, Quad talks open in Manila). Standard library only,
no network, deterministic: the same bytes are written on every run.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # The gate reads exactly the bytes written: refuse a partial copy.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy incomplete")


if __name__ == "__main__":
    main()
