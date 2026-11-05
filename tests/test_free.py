from instrkit.cli import main
from instrkit.lint import lint_text

GOOD = "# AGENTS.md\n\n## Setup and commands\n- Test: `pytest -q`\n"


def test_good():
    assert lint_text(GOOD) == []


def test_core_rules():
    assert {f.rule for f in lint_text("hello TODO")} == {"R002", "R003", "R004", "R005"}


def test_cli(tmp_path, capsys):
    p = tmp_path / "AGENTS.md"
    p.write_text(GOOD)
    assert main(["lint", "--config", str(tmp_path / "x.json"), str(p)]) == 0
    p.write_text("# T\n")
    assert main(["lint", "--config", str(tmp_path / "x.json"), str(p)]) == 1


def test_templates_compose_clean():
    import os
    d = os.path.join(os.path.dirname(__file__), "..", "instrkit", "templates")
    for s in os.listdir(os.path.join(d, "stacks")):
        parts = [open(os.path.join(d, "base.md")).read(), open(os.path.join(d, "stacks", s)).read(),
                 open(os.path.join(d, "closing.md")).read()]
        assert lint_text("\n".join(parts).replace("{{project}}", "YourBrand")) == [], s
