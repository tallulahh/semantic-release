import os
from ruamel.yaml import YAML

WORKFLOWS_DIR = ".github/workflows"
DOCS_DIR = "docs/workflows"
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096
os.makedirs(DOCS_DIR, exist_ok=True)

def format_table(obj, kind="Inputs"):
    if not obj:
        return f"_No {kind}_\n"
    md = f"| Name | Required | Type | Description |\n|------|----------|------|-------------|\n"
    for name, props in obj.items():
        required = props.get("required", False)
        typ = props.get("type", "")
        desc = props.get("description", "")
        md += f"| {name} | {required} | {typ} | {desc} |\n"
    return md

for file in os.listdir(WORKFLOWS_DIR):
    if not (file.endswith(".yml") or file.endswith(".yaml")):
        continue

    with open(os.path.join(WORKFLOWS_DIR, file), "r") as f:
        wf_yaml = yaml.load(f)

    name = wf_yaml.get("name", file.replace(".yml", "").replace(".yaml", ""))
    triggers = wf_yaml.get("on", {})

    md = f"# {name}\n\n"
    md += f"**Path:** `{WORKFLOWS_DIR}/{file}`\n\n"

    if isinstance(triggers, dict):
        md += "## Triggers\n"
        for trig, details in triggers.items():
            md += f"- `{trig}`\n"
            if trig == "workflow_call":
                md += "\n### Inputs\n"
                md += format_table(details.get("inputs", {}), "Inputs")

                md += "\n### Secrets\n"
                md += format_table(details.get("secrets", {}), "Secrets")
    else:
        md += f"## Triggers\n- `{triggers}`\n"

    jobs = wf_yaml.get("jobs", {})
    md += "\n## Jobs\n"
    if jobs:
        for j in jobs.keys():
            md += f"- {j}\n"
    else:
        md += "_None_\n"

    out_file = os.path.join(DOCS_DIR, file.replace(".yml", ".md").replace(".yaml", ".md"))
    with open(out_file, "w") as f:
        f.write(md)
