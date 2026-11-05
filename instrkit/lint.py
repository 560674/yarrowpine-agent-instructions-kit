"""Rule-based checker for AGENTS.md-style instruction files (stdlib only). Free edition: rules R001-R006."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, asdict

DEFAULTS = {"max_lines": 300, "disable": [], "required_sections": ["commands"]}

SECTION_ALIASES = {
    "commands": ["command", "setup", "build", "test", "how to run", "development"],
    "layout": ["layout", "structure", "where things live", "repository map"],
    "validation": ["validation", "before you finish", "definition of done", "checks"],
    "boundaries": ["do not", "don't", "restricted", "boundaries", "never"],
}

HINTS = {"commands": "Setup and commands", "layout": "Repository layout", "validation": "Before you finish", "boundaries": "Do not touch"}

PLACEHOLDER_RE = re.compile(r"(\{\{[^}]*\}\}|\[your [^\]]+\]|<your[- _][^>]+>|\bTODO\b|\bTBD\b|\bFIXME\b|\bXXX\b)", re.I)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


@dataclass
class Finding:
    rule: str
    severity: str  # "error" | "warning"
    line: int
    message: str


def load_config(path: str | None) -> dict:
    cfg = dict(DEFAULTS)
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            cfg.update(json.load(fh))
    return cfg


def _headings(lines):
    out = []
    in_code = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEADING_RE.match(line)
        if m:
            out.append((i, len(m.group(1)), m.group(2)))
    return out


def _has_section(headings, key):
    words = SECTION_ALIASES.get(key, [key])
    return any(any(w in h.lower() for w in words) for _, _, h in headings)


def lint_text(text: str, base_dir: str = ".", config: dict | None = None) -> list[Finding]:
    cfg = dict(DEFAULTS, **(config or {}))
    f: list[Finding] = []
    lines = text.splitlines()
    if not text.strip():
        return [Finding("R001", "error", 1, "file is empty")]
    heads = _headings(lines)
    if not any(level == 1 for _, level, _ in heads):
        f.append(Finding("R002", "error", 1, "no top-level '# ' title"))
    for key in cfg["required_sections"]:
        if not _has_section(heads, key):
            f.append(Finding("R003", "error", 1, f"missing a '{key}' section (e.g. '## {HINTS.get(key, key.title())}')"))
    if "`" not in text:
        f.append(Finding("R004", "warning", 1, "no commands in backticks; agents need exact, copy-pasteable commands"))
    in_code = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
        m = PLACEHOLDER_RE.search(line)
        if m and not in_code:
            f.append(Finding("R005", "error", i, f"unfilled placeholder '{m.group(0)}'"))
    if len(lines) > cfg["max_lines"]:
        f.append(Finding("R006", "warning", len(lines), f"{len(lines)} lines (max {cfg['max_lines']}); long files bury the rules that matter"))
    disabled = set(cfg.get("disable", []))
    return [x for x in f if x.rule not in disabled]


def lint_file(path: str, config: dict | None = None) -> list[Finding]:
    if not os.path.exists(path):
        return [Finding("R001", "error", 0, f"{path} not found")]
    with open(path, encoding="utf-8") as fh:
        return lint_text(fh.read(), os.path.dirname(os.path.abspath(path)), config)


def to_json(results: dict) -> str:
    return json.dumps({p: [asdict(x) for x in fs] for p, fs in results.items()}, indent=2)
