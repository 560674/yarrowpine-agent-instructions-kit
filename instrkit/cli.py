from __future__ import annotations

import argparse
import os
import sys

from . import __version__
from .lint import lint_file, load_config, to_json


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="instrkit", description="AGENTS.md checker (free edition)")
    ap.add_argument("--version", action="version", version=f"instrkit {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    lp = sub.add_parser("lint", help="check one or more instruction files")
    lp.add_argument("paths", nargs="*", default=["AGENTS.md"])
    lp.add_argument("--config", default="instrkit.json")
    lp.add_argument("--format", choices=["text", "json"], default="text")
    lp.add_argument("--strict", action="store_true", help="treat warnings as failures")
    a = ap.parse_args(argv)

    cfg = load_config(a.config)
    results = {p: lint_file(p, cfg) for p in a.paths}
    bad = False
    for fs in results.values():
        if any(x.severity == "error" for x in fs) or (a.strict and fs):
            bad = True
    if a.format == "json":
        print(to_json(results))
    else:
        for p, fs in results.items():
            if not fs:
                print(f"{p}: OK")
            for x in fs:
                print(f"{p}:{x.line}: {x.severity} {x.rule} {x.message}")
    return 1 if bad else 0
