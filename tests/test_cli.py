"""Tests for PulseNote.

Built by Mourad.Soltani
"""
import pytest
from pulsenote.cli import parse_commits, format_standup, get_git_log


def test_parse_commits_empty():
    assert parse_commits("") == []
    assert parse_commits("   \n\n  ") == []


def test_parse_commits():
    raw = "abc123 fix login\ndef456 add feature"
    assert parse_commits(raw) == ["abc123 fix login", "def456 add feature"]


def test_format_standup_markdown():
    out = format_standup(["fix bug"], "ship feature", "none")
    assert "Daily Standup" in out
    assert "fix bug" in out
    assert "ship feature" in out


def test_format_standup_slack():
    out = format_standup(["commit"], "work", "", "slack")
    assert "*Daily Standup*" in out
    assert "*Blockers:*" in out


def test_get_git_log_no_git(monkeypatch):
    monkeypatch.setattr("subprocess.run", lambda *a, **k: type("R", (), {"returncode": 1, "stdout": ""})())
    assert get_git_log("1 day ago") == ""
