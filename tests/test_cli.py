"""Tests for the ouroboros CLI."""

import pytest

from ouroboros.cli import build_parser


def _run(argv, capsys):
    rc = build_parser().parse_args(argv).func(build_parser().parse_args(argv))
    out = capsys.readouterr().out
    return rc, out


def test_validate_valid(capsys):
    rc, out = _run(["validate", "(A ∧ B) → C"], capsys)
    assert rc == 0
    assert "VALID" in out


def test_validate_invalid(capsys):
    rc, out = _run(["validate", "A ∧ B → C"], capsys)
    assert rc == 1
    assert "INVALID" in out


def test_golden_all_pass(capsys):
    rc, out = _run(["golden"], capsys)
    assert rc == 0
    assert "passed" in out


def test_translate(capsys):
    rc, out = _run(["translate", "(A ∧ B) → C"], capsys)
    assert rc == 0
    assert "A and B implies C" in out


def test_anomaly_canonical(capsys):
    rc, out = _run(["anomaly", "--canonical"], capsys)
    assert rc == 0
    assert "Echoing Door" in out


def test_anomaly_batch(capsys):
    rc, out = _run(["anomaly", "-n", "3", "--seed", "1"], capsys)
    assert rc == 0
    assert out.count("🔍") == 3


def test_realm(capsys):
    rc, out = _run(["realm"], capsys)
    assert rc == 0
    assert "Labyrinth of Eternity" in out


def test_demo(capsys):
    rc, out = _run(["demo"], capsys)
    assert rc == 0
    assert "Ouroboros Project" in out
    assert "valid" in out
