#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""The Interrupted Apology — make.fun "Make the AI Judge Laugh".

The joke itself lives in entry.txt next to this script. Running this
script loads that line, checks it against the competition gate (exactly
one line, 1 to 200 characters, not only whitespace, no control
characters) and publishes it as entry.txt inside the output folder the
grader provides through MAKEFUN_OUTPUT_DIR, defaulting to /output.
"""

import os
import sys
from pathlib import Path

GATE_MAX_CHARS = 200
ENTRY_FILENAME = "entry.txt"


def script_dir():
    return Path(__file__).resolve().parent


def load_line():
    raw = (script_dir() / ENTRY_FILENAME).read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as err:
        raise ValueError("entry.txt is not valid UTF-8: %s" % err)


def gate_check(text):
    line = text.strip()
    if not line:
        raise ValueError("entry.txt holds only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("the entry must be a single line")
    if len(line) > GATE_MAX_CHARS:
        raise ValueError(
            "the entry is %d characters, over the %d limit"
            % (len(line), GATE_MAX_CHARS)
        )
    for char in line:
        if ord(char) < 32 or ord(char) == 127:
            raise ValueError("the entry holds a control character")
    return line


def publish(line):
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / ENTRY_FILENAME
    target.write_bytes(line.encode("utf-8"))
    if target.read_bytes() != line.encode("utf-8"):
        raise ValueError("published entry.txt does not match the entry")
    return target


def main():
    try:
        line = gate_check(load_line())
        target = publish(line)
    except ValueError as err:
        print("error: %s" % err, file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(line), target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
