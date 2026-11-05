# Agent Instructions Kit

*Template & Checker for AGENTS.md™ files*

Free edition: a base template, 3 stack templates (python-package, node-typescript, go-service) and the
`instrkit lint` checker with 6 core rules. Pure Python standard library, Python® 3.9+.

## Use
1. Copy `instrkit/templates/base.md`, one file from `instrkit/templates/stacks/` and `closing.md` into your
   repository's `AGENTS.md`; replace `{{project}}` and the example commands with your own.
2. Check it:
```bash
pip install .            # or: python -m instrkit lint AGENTS.md
instrkit lint AGENTS.md  # exit 1 on errors, --strict also fails on warnings, --format json for CI
```
Rules: R001 empty file · R002 no title · R003 missing commands section · R004 no backticked commands ·
R005 unfilled placeholders · R006 too long.

## Pro edition
Adds 7 more stack templates, 8 task playbooks, `instrkit init` to compose a file, 5 more rules (broken links,
secret-looking strings, empty sections, duplicate headings, vague instructions), a CI workflow example and a
PR review checklist. Available on our Gumroad store.

## Notes
AGENTS.md is an open format (https://agents.md/) stewarded by the Agentic AI Foundation under the Linux
Foundation. AGENTS.md is a trademark of LF Projects, LLC. Independent project, not affiliated with or endorsed by them or by any AI tool vendor.
Built with AI assistance. © 2026 Yarrowpine Studio. MIT licensed (see LICENSE). Python is a registered trademark of the Python Software Foundation.
