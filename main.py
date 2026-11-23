#!/usr/bin/env python3
"""Copy program for the SUNDAY PAPER news-image-20261122 entry.

Reproduces entry.png byte-identically to /output/entry.png.
Standard library only (os, shutil, hashlib). No network, no drawing:
the image was drawn once by draw.py and is shipped in this repository.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "05983ec790a2f3252923a0cd3a1c75bfe0dbc03254a11b59405ea266a74d2c68"
EXPECTED_SIZE = 177344
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    assert data[:8] == PNG_MAGIC, "entry.png is not a PNG"
    assert len(data) == EXPECTED_SIZE, "entry.png size mismatch"
    digest = hashlib.sha256(data).hexdigest()
    assert digest == EXPECTED_SHA256, "entry.png sha256 mismatch"
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    # verify the copy we just wrote, byte for byte
    with open(dst, "rb") as f:
        written = f.read()
    assert written == data, "written copy differs from source"
    assert hashlib.sha256(written).hexdigest() == EXPECTED_SHA256
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), digest))


if __name__ == "__main__":
    main()
