"""PulseNote CLI — generate standup notes from local Git history.

Built by Mourad.Soltani
"""
import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_git_log(since: str, cwd: str = ".") -> str:
    """Run git log and return formatted output."""
    try:
        result = subprocess.run(
            ["git", "log", f"--since={since}", "--pretty=format:%h %s", "--no-merges"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip()
    except FileNotFoundError:
        return ""


def parse_commits(raw: str) -> list[str]:
    if not raw:
        return []
    return [line for line in raw.splitlines() if line.strip()]


def format_standup(commits: list[str], today: str, blockers: str, fmt: str = "markdown") -> str:
    if fmt == "slack":
        lines = ["*Daily Standup*"]
        lines.append(f"*Yesterday:*\n" + ("\n".join(f"• {c}" for c in commits) if commits else "No commits"))
        lines.append(f"*Today:*\n{today or 'TBD'}")
        lines.append(f"*Blockers:*\n{blockers or 'None'}")
        return "\n\n".join(lines)
    # markdown default
    lines = ["## Daily Standup"]
    lines.append("### Yesterday")
    lines.extend([f"- {c}" for c in commits] or ["- No commits found"])
    lines.append("\n### Today")
    lines.append(today or "TBD")
    lines.append("\n### Blockers")
    lines.append(blockers or "None")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="PulseNote — standup from Git (Built by Mourad.Soltani)")
    sub = parser.add_subparsers(dest="cmd")

    standup = sub.add_parser("standup", help="Generate daily standup")
    standup.add_argument("--format", choices=["markdown", "slack", "plain"], default="markdown")
    standup.add_argument("--hours", type=int, default=24)
    standup.add_argument("--today", default="")
    standup.add_argument("--blockers", default="")
    standup.add_argument("--repo", default=".")

    week = sub.add_parser("week", help="Generate weekly digest")
    week.add_argument("--format", choices=["markdown", "slack"], default="markdown")
    week.add_argument("--repo", default=".")

    args = parser.parse_args(argv)

    if args.cmd == "standup":
        since = f"{args.hours} hours ago"
        raw = get_git_log(since, args.repo)
        commits = parse_commits(raw)
        today = args.today or input("What are you working on today? ")
        blockers = args.blockers or input("Any blockers? ")
        print(format_standup(commits, today, blockers, args.format))
    elif args.cmd == "week":
        raw = get_git_log("7 days ago", args.repo)
        commits = parse_commits(raw)
        print(format_standup(commits, "Weekly summary", "N/A", args.format))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
