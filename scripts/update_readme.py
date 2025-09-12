#!/usr/bin/env python3
import os
import sys
from ruamel.yaml import YAML
from pathlib import Path

WORKFLOWS_DIR = Path(".github/workflows")
DOCS_DIR = Path("docs/workflows")
REPO = os.environ.get("GITHUB_REPOSITORY", "OWNER/REPO")

def md_escape(val):
    if val is None:
        return ""
    s = str(val)
    return s.replace("\n", " ").replace("|", r"\|").strip()

def parse_triggers(on):
    if on is None:
        return []
    if isinstance(on, dict):
        return list(on.keys())
    if isinstance(on, list):
        return on
    if isinstance(on, str):
        return [on]
    return []

def table_inputs(mapping):
    if not mapping:
        return "_None_\n"
    header = "| Name | Required | Default | Description |\n|------|----------|---------|-------------|\n"
    rows = []
    for name, props in mapping.items():
        required = props.get("required", False)
        default = props.get("default", "")
        desc = props.get("description", "")
        rows.append(f"| {md_escape(name)} | {md_escape(required)} | {md_escape(default)} | {md_escape(desc)} |")
    return header + "\n".join(rows) + "\n"

def table_secrets(mapping):
    if not mapping:
        return "_None_\n"
    header = "| Name | Required | Description |\n|------|----------|-------------|\n"
    rows = []
    for name, props in mapping.items():
        required = props.get("required", False)
        desc = props.get("description", "")
        rows.append(f"| {md_escape(name)} | {md_escape(required)} | {md_escape(desc)} |")
    return header + "\n".join(rows) + "\n"

def table_outputs(mapping):
    if not mapping:
        return "_None_\n"
    header = "| Name | Description | Value |\n|------|-------------|-------|\n"
    rows = []
    for name, props in mapping.items():
        desc = props.get("description", "")
        val = props.get("value", "")
        rows.append(f"| {md_escape(name)} | {md_escape(desc)} | `{md_escape(val)}` |")
    return header + "\n".join(rows) + "\n"

def jobs_summary(jobs):
    if not jobs:
        return "_None_\n"
    lines = []
    for jname, j in jobs.items():
        rn = j.get("runs-on")
        uses = j.get("uses")
        steps = j.get("steps") or []
        if uses:
            lines.append(f"- **{jname}**: reuses `{uses}`")
        else:
            lines.append(f"- **{jname}**: runs-on `{rn}` with {len(steps)} step(s)")
    return "\n".join(lines) + "\n"

def example_usage(workflow_file, wf):
    wc = ((wf.get("on") or {}) if isinstance(wf.get("on"), dict) else {}).get("workflow_call")
    if not wc:
        return "_This workflow is not declared as reusable (`on.workflow_call`)._\n"
    lines = []
    lines.append("```yaml")
    lines.append("jobs:")
    lines.append("  call:")
    lines.append(f"    uses: {REPO}/.github/workflows/{workflow_file.name}@v1")
    inputs = wc.get("inputs") or {}
    secrets = wc.get("secrets") or {}
    if inputs:
        lines.append("    with:")
        for name, props in inputs.items():
            default = props.get("default")
            example_val = default if default is not None else "<value>"
            lines.append(f"      {name}: {example_val}")
    if secrets:
        lines.append("    secrets:")
        for name in secrets.keys():
            lines.append(f"      {name}: ${{{{ secrets.{name} }}}}")
    lines.append("```")
    return "\n".join(lines) + "\n"

def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096
    if not WORKFLOWS_DIR.exists():
        print("No .github/workflows directory found; nothing to document.")
        return

    for wf_path in sorted(WORKFLOWS_DIR.iterdir()):
        if not wf_path.suffix.lower() in (".yml", ".yaml"):
            continue
        with wf_path.open("r", encoding="utf-8") as f:
            wf = yaml.load(f) or {}

        title = wf.get("name") or wf_path.stem
        triggers = parse_triggers(wf.get("on"))
        wc = ((wf.get("on") or {}) if isinstance(wf.get("on"), dict) else {}).get("workflow_call", {})

        md = []
        md.append(f"# {title}\n\n")
        md.append(f"**Path:** `{wf_path.as_posix()}`\n\n")

        md.append("## Triggers\n")
        md.append(("\n".join([f"- `{t}`" for t in triggers]) or "_None_") + "\n\n")

        # Reusable workflow interface
        if wc:
            md.append("## Reusable Interface (`on.workflow_call`)\n\n")
            md.append("### Inputs\n")
            md.append(table_inputs(wc.get("inputs")))
            md.append("### Secrets\n")
            md.append(table_secrets(wc.get("secrets")))
            md.append("### Outputs\n")
            md.append(table_outputs(wc.get("outputs")))
        else:
            md.append("## Reusable Interface\n")
            md.append("_Not declared as reusable._\n")

        md.append("\n## Permissions\n")
        perms = wf.get("permissions")
        if perms is None:
            md.append("_Default (inherit from repository or job-level overrides)._")
        elif isinstance(perms, dict):
            md.append("\n".join([f"- `{k}`: `{v}`" for k, v in perms.items()]))
        else:
            md.append(f"`{perms}`")
        md.append("\n\n")

        md.append("## Concurrency\n")
        conc = wf.get("concurrency")
        if conc:
            md.append(f"`{conc}`\n\n")
        else:
            md.append("_None_\n\n")

        md.append("## Jobs\n")
        md.append(jobs_summary(wf.get("jobs")) + "\n")

        md.append("## Example Usage\n")
        md.append(example_usage(wf_path, wf))

        out_path = DOCS_DIR / f"{wf_path.stem}.md"
        with out_path.open("w", encoding="utf-8") as out:
            out.write("".join(md))

if __name__ == "__main__":
    sys.exit(main())
