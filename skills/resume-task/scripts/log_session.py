#!/usr/bin/env python3
"""
log_session.py — manage chat-session headings in a conversation log file.

Subcommand:
  start   Append a new "## Chat Session N — <date>" heading to the log,
          auto-incrementing N based on the highest existing session number.
          Prints the new session number to stdout.

This is used by:
  - create-task: to open "Chat Session 1" on a brand-new log
  - resume flow: to open the next session ("Chat Session 2", etc.)

Per-turn turns are appended separately (see the skill's heredoc method), so this
script only owns the session heading + numbering, which requires reading the file.

Usage:
    python log_session.py start --log <path-to-log.md> [--date YYYY-MM-DD]
"""

import argparse
import datetime
import os
import re
import sys

SESSION_RE = re.compile(r"^##\s+Chat Session\s+(\d+)\b", re.MULTILINE)


def next_session_number(content):
    nums = [int(m.group(1)) for m in SESSION_RE.finditer(content)]
    return (max(nums) + 1) if nums else 1


def cmd_start(args):
    log_path = args.log
    if not os.path.isfile(log_path):
        print(f"error: log file not found: {log_path}", file=sys.stderr)
        return 1

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    n = next_session_number(content)
    date = args.date or datetime.date.today().isoformat()

    heading = f"\n## Chat Session {n} — {date}\n"
    # Ensure there's a separating newline before the heading.
    if content and not content.endswith("\n"):
        heading = "\n" + heading

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(heading)

    print(n)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Manage chat-session headings.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="Append a new session heading.")
    p_start.add_argument("--log", required=True, help="Path to the conversation log file.")
    p_start.add_argument("--date", help="Override date (YYYY-MM-DD). Defaults to today.")
    p_start.set_defaults(func=cmd_start)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
