#!/usr/bin/env python3
"""Build a printable PDF of DEFINITIONS.md with note space under each question.

Each Q section starts on a fresh page and ends with ruled lines at the foot of the
page for handwritten additions.

    python3 make_printable.py              # -> DEFINITIONS_printable.pdf
    python3 make_printable.py --lines 10     # more note lines per question

Requires pandoc and a LaTeX engine (xelatex).
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SOURCE = HERE / "DEFINITIONS.md"
HEADER = HERE / "printable-header.tex"
OUTPUT = HERE / "DEFINITIONS_printable.pdf"


def preprocess(md: str, lines: int) -> str:
    """Drop screen-only furniture and append a notes block to each Q section."""
    # The "math renders in Cursor/VS Code" note is meaningless on paper.
    md = re.sub(r"^> .*(?:\n> .*)*\n", "", md, flags=re.M)
    # Horizontal rules separated sections on screen; page breaks do that here.
    md = re.sub(r"^---\n", "", md, flags=re.M)

    notes = "\n\n```{=latex}\n\\notesarea{%d}\n```\n\n" % lines
    parts = re.split(r"^(## .*)$", md, flags=re.M)

    out = [parts[0].rstrip() + "\n"]           # title + intro
    for heading, body in zip(parts[1::2], parts[2::2]):
        out.append(f"\n{heading}\n{body.rstrip()}\n{notes}")
    return "".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lines", type=int, default=6, metavar="N",
                    help="ruled note lines under each question (default 6 -- the most that keeps every question on a single page)")
    ap.add_argument("--source", type=Path, default=SOURCE, help="markdown file to convert")
    ap.add_argument("--out", type=Path, default=OUTPUT, help="output PDF")
    args = ap.parse_args()

    for tool in ("pandoc", "xelatex"):
        if not shutil.which(tool):
            sys.exit(f"error: {tool} not found. brew install pandoc / install MacTeX.")
    if not args.source.exists():
        sys.exit(f"error: {args.source} not found")

    md = preprocess(args.source.read_text(encoding="utf-8"), args.lines)
    tmp = HERE / ".printable.md"
    tmp.write_text(md, encoding="utf-8")

    cmd = [
        "pandoc", str(tmp),
        # lists_without_preceding_blankline: the source puts bullets directly under their
        # intro line, which GitHub and VS Code accept but strict markdown folds into the
        # paragraph -- without this the lists render as running text.
        "--from", "markdown+raw_tex+tex_math_dollars+lists_without_preceding_blankline",
        "--pdf-engine", "xelatex",
        "--include-in-header", str(HEADER),
        "--variable", "documentclass=article",
        "--variable", "fontsize=10pt",
        "--variable", "colorlinks=true",
        "--top-level-division=section",
        "--output", str(args.out),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        tmp.unlink(missing_ok=True)

    if proc.returncode != 0:
        sys.exit(f"pandoc failed:\n{proc.stderr[-3000:]}")
    print(f"wrote {args.out.relative_to(Path.cwd()) if args.out.is_relative_to(Path.cwd()) else args.out}"
          f"  ({args.lines} note lines per question)")


if __name__ == "__main__":
    main()
