#!/usr/bin/env python3
import re
import os

def replace_section(content, marker, new_block):
    pattern = re.compile(
        rf"(<!-- AUTO-GENERATED-{marker}-START -->)(.*?)(<!-- AUTO-GENERATED-{marker}-END -->)",
        re.DOTALL,
    )
    new_block = f"\\1\n{new_block.strip()}\n\\3"
    if pattern.search(content):
        return pattern.sub(new_block, content)
    else:
        return (
            content
            + f"\n\n<!-- AUTO-GENERATED-{marker}-START -->\n{new_block.strip()}\n<!-- AUTO-GENERATED-{marker}-END -->\n"
        )

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# Build actions table
actions_md = "| Name | Path | Docs |\n|------|------|------|\n"
if os.path.exists("docs/actions"):
    for file in sorted(os.listdir("docs/actions")):
        if file.endswith(".md"):
            name = file.replace(".md", "")
            actions_md += f"| {name} | actions/{name}/README.md | docs/actions/{file} |\n"
else:
    actions_md = "_No actions documented_"

# Build workflows table
workflows_md = "| Name | Path | Docs |\n|------|------|------|\n"
if os.path.exists("docs/workflows"):
    for file in sorted(os.listdir("docs/workflows")):
        if file.endswith(".md"):
            name = file.replace(".md", "")
            workflows_md += f"| {name} | .github/workflows/{name}.yml | docs/workflows/{file} |\n"
else:
    workflows_md = "_No workflows documented_"

# Build changelog snippet
if os.path.exists("docs/CHANGELOG.md"):
    with open("docs/CHANGELOG.md", "r", encoding="utf-8") as f:
        changelog_lines = f.readlines()
    changelog_md = "".join(changelog_lines[:40]).strip()
    if len(changelog_lines) > 40:
        changelog_md += "\n\n… see [CHANGELOG.md](docs/CHANGELOG.md) for full history"
else:
    changelog_md = "_No changelog available_"

readme = replace_section(readme, "ACTIONS", actions_md)
readme = replace_section(readme, "WORKFLOWS", workflows_md)
readme = replace_section(readme, "CHANGELOG", changelog_md)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("README.md updated ✅")
