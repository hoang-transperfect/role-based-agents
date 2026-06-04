#!/usr/bin/env python3
"""
list_in_progress_tasks.py

Lists tasks found in a project's `in-progress-tasks/` folder by reading the
frontmatter (id, description) of each task markdown file.

Used by the gather-needs skill to detect whether an existing task matches the
user's stated needs (so it can route to "resume task" instead of "create task").

Usage:
    # List tasks for a single project
    python list_in_progress_tasks.py --project ~/projects/my-project

    # Scan all projects under a base directory (each subfolder is a project)
    python list_in_progress_tasks.py --base ~/projects

    # Output as JSON (for programmatic use / matching)
    python list_in_progress_tasks.py --project ~/projects/my-project --json
"""

import argparse
import json
import os
import sys


def parse_frontmatter(path):
    """Extract id and description from a markdown file's YAML frontmatter.

    Returns a dict with 'id' and 'description' (values may be empty strings).
    Does not require a YAML library — parses the simple key: value block.
    """
    fields = {"id": "", "description": ""}
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return fields

    if not content.startswith("---"):
        return fields

    # Grab the block between the first two '---' lines
    parts = content.split("---", 2)
    if len(parts) < 3:
        return fields
    block = parts[1]

    for line in block.splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in fields:
            fields[key] = value
    return fields


def list_tasks_in_project(project_dir):
    """Return a list of task dicts for one project."""
    tasks_dir = os.path.join(project_dir, "in-progress-tasks")
    tasks = []
    if not os.path.isdir(tasks_dir):
        return tasks

    for name in sorted(os.listdir(tasks_dir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(tasks_dir, name)
        if not os.path.isfile(path):
            continue
        fm = parse_frontmatter(path)
        tasks.append({
            "id": fm["id"] or os.path.splitext(name)[0],
            "description": fm["description"],
            "file": path,
            "project": os.path.basename(os.path.abspath(project_dir)),
        })
    return tasks


def find_projects(base_dir):
    """Return subdirectories of base_dir that look like projects
    (i.e. contain an in-progress-tasks/ folder)."""
    projects = []
    if not os.path.isdir(base_dir):
        return projects
    for name in sorted(os.listdir(base_dir)):
        candidate = os.path.join(base_dir, name)
        if os.path.isdir(candidate) and os.path.isdir(
                os.path.join(candidate, "in-progress-tasks")
        ):
            projects.append(candidate)
    return projects


def main():
    parser = argparse.ArgumentParser(
        description="List in-progress tasks from project folder(s)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--project", help="Path to a single project folder")
    group.add_argument("--base", help="Base directory containing multiple projects")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    all_tasks = []
    if args.project:
        all_tasks = list_tasks_in_project(args.project)
    else:
        for project_dir in find_projects(args.base):
            all_tasks.extend(list_tasks_in_project(project_dir))

    if args.json:
        print(json.dumps(all_tasks, indent=2))
        return

    if not all_tasks:
        print("No in-progress tasks found.")
        return

    for t in all_tasks:
        desc = t["description"] or "(no description)"
        print(f"- [{t['project']}] {t['id']} — {desc}")


if __name__ == "__main__":
    main()

