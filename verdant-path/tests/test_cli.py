"""Tests for the CLI commands."""

from verdant_path.cli import main


def test_split_command(capsys):
    rc = main(["split", "5"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "5x/week" in out
    assert "Posterior Chain" in out


def test_split_invalid(capsys):
    rc = main(["split", "9"])
    assert rc == 2


def test_checkin_command(capsys):
    rc = main(["checkin", "--energy", "4", "--mood", "3", "--soreness", "2",
               "--sleep", "7", "--hrv", "55"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Fatigue" in out
    assert "🟠" in out  # spec example is amber


def test_habits_command(capsys):
    rc = main(["habits"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "90-Day" in out
    assert "Meditation" in out
    assert "Buildup" in out or "Build" in out


def test_demo_command(capsys):
    rc = main(["demo"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Example Workflow" in out
    assert "TRIMP" in out
    assert "ACWR" in out
    assert "Suggestion" in out
