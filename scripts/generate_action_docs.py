#!/usr/bin/env python3
import os
import sys
import glob
import yaml
from pathlib import Path

ACTIONS_DIR = Path("actions")
DOCS_DIR = Path("docs/actions")
REPO = os.environ.get("GITHUB_REPOSITORY", "OWNER/REPO")

def md_escape(val):
    if val is None:
        return ""
    s = str(val)
    return s.replace("\n", " ").replace("|", r"\|").strip()

def make_table_rows(mapping, is_inputs=True):
    if not mapping:
        return "_None_\n"
    header = "| Name | Required | Default | Description |\n|------|----------|---------|-------------|\n"
    rows = []
    for name, props in mapping.items():
        required = props.get("required", False)
        default = props.get("default", "")
        desc = props.get("description", "") or props.get("deprecationMessage", "")
        rows.append(f"| {md_escape(name)} | {md_escape(required)} | {md_escape(default)} | {md_escape(desc)} |")
    return header + "\n".join(rows) + "\n"

def outputs_table(mapping):
    if not mapping:
        return "_None_\n"
    header = "| Name | Description |\n|------|-------------|\n"
    rows = []
    for name, props in mapping.items():
        desc = props.get("description", "")
        rows.append(f"| {md_escape(name)} | {md_escape(desc)} |")
    return header + "\n".join(rows) + "\n"

def runs_summary(runs):
    if not runs:
        return "_Unknown_\n"
    using = runs.get("using", "composite")
    s = f"- **using:** `{using}`\n"
    if using == "composite":
        steps = runs.get("steps", [])
        s += f"- **steps:** {len(steps)}\n"
    elif using.startswith("node"):
        main = runs.get("main", "")
        s += f"- **entry:** `{main}`\n"
    return s + "\n"

def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    if not ACTIONS_DIR.exists():
        print("No actions/ directory found; nothing to document.")
        return

    action_dirs = sorted([p for p in ACTIONS_DIR.iterdir() if p.is_dir()])
    for adir in action_dirs:
        yml_path = adir / "action.yml"
        if not yml_path.exists():
            yml_path = adir / "action.yaml"
        if not yml_path.exists():
            continue

        with yml_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        action_name = data.get("name") or adir.name
        description = data.get("description", "No description provided.")
        readme_path = adir / "README.md"
        readme_rel = os.path.relpath(readme_path.as_posix(), DOCS_DIR.as_posix()) if readme_path.exists() else None

        md = []
        md.append(f"# {action_name}\n")
        md.append(f"**Path:** `{yml_path.as_posix()}`  ")
        if readme_rel:
            md.append(f"**README:** [View full documentation]({readme_rel})\n")
        else:
            md.append("\n")

        md.append("## Description\n")
        md.append(f"{description}\n\n")

        md.append("## Inputs\n")
        md.append(make_table_rows(data.get("inputs", {})))

        md.append("## Outputs\n")
        md.append(outputs_table(data.get("outputs", {})))

        md.append("## Runs\n")
        md.append(runs_summary(data.get("runs", {})))

        md.append("## Example Usage\n")
        md.append("```yaml\n")
        md.append(f"- uses: {REPO}/actions/{adir.name}@v1\n")
        if data.get("inputs"):
            md.append("  with:\n")
            for name, props in (data.get("inputs") or {}).items():
                default = props.get("default")
                example_val = default if default is not None else "<value>"
                md.append(f"    {name}: {example_val}\n")
        md.append("```\n")

        out_path = DOCS_DIR / f"{adir.name}.md"
        with out_path.open("w", encoding="utf-8") as f:
            f.write("".join(md))

if __name__ == "__main__":
    sys.exit(main())
