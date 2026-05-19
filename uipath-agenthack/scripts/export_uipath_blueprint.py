#!/usr/bin/env python3
"""Export UiPath implementation blueprint files from the Maestro process spec."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPEC_FILE = ROOT / "architecture" / "maestro-process-spec.json"
PACKAGE_DIR = ROOT / "uipath-package"
BPMN_FILE = PACKAGE_DIR / "maestro-process.bpmn"
FORM_FILE = PACKAGE_DIR / "action-center-form-schema.json"
ROBOT_README = PACKAGE_DIR / "robot-workflow-pseudocode.md"
PACKAGE_README = PACKAGE_DIR / "README.md"

BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"
ET.register_namespace("bpmn", BPMN)


def tag(name: str) -> str:
    return f"{{{BPMN}}}{name}"


def load_spec() -> dict[str, Any]:
    return json.loads(SPEC_FILE.read_text(encoding="utf-8"))


def node_type(flow_type: str) -> str:
    if flow_type == "start_event":
        return "startEvent"
    if flow_type == "end_event":
        return "endEvent"
    if flow_type == "exclusive_gateway":
        return "exclusiveGateway"
    return "task"


def build_bpmn(spec: dict[str, Any]) -> ET.ElementTree:
    definitions = ET.Element(
        tag("definitions"),
        {
            "id": "Definitions_AgentOpsCaseControlRoom",
            "targetNamespace": "https://example.local/agentops-case-control-room",
        },
    )
    process = ET.SubElement(
        definitions,
        tag("process"),
        {
            "id": "Process_AgentOpsCaseControlRoom",
            "name": spec["name"],
            "isExecutable": "false",
        },
    )
    flow = spec["flow"]
    for step in flow:
        node = ET.SubElement(
            process,
            tag(node_type(step["type"])),
            {
                "id": step["id"],
                "name": step["label"],
            },
        )
        if step.get("evidence_events"):
            doc = ET.SubElement(node, tag("documentation"))
            doc.text = "Evidence events: " + ", ".join(step["evidence_events"])
    for index, (source, target) in enumerate(zip(flow, flow[1:]), start=1):
        ET.SubElement(
            process,
            tag("sequenceFlow"),
            {
                "id": f"Flow_{index:02d}",
                "sourceRef": source["id"],
                "targetRef": target["id"],
            },
        )
    return ET.ElementTree(definitions)


def write_form_schema(spec: dict[str, Any]) -> None:
    schema = {
        "name": "AgentOpsApprovalTask",
        "target": "UiPath Action Center / Apps approval form",
        "fields": [
            {
                "name": "case_id",
                "type": "readonlyText",
                "label": "Case ID",
                "source": "case.case_id",
            },
            {
                "name": "risk_level",
                "type": "badge",
                "label": "Risk level",
                "source": "task.risk_level",
            },
            {
                "name": "evidence_summary",
                "type": "textarea",
                "label": "Evidence summary",
                "source": "task.summary",
                "readonly": True,
            },
            {
                "name": "decision",
                "type": "choice",
                "label": "Decision",
                "options": ["approve", "request_more_evidence", "reject"],
                "required": True,
            },
            {
                "name": "moderator_comment",
                "type": "textarea",
                "label": "Decision note",
                "required": False,
            },
        ],
        "policy": spec["approval_policy"],
        "claim_boundary": "local form schema only; not published to UiPath Action Center yet",
    }
    FORM_FILE.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_robot_readme(spec: dict[str, Any]) -> None:
    lines = [
        "# UiPath Robot Workflow Pseudocode",
        "",
        "Target queue: `AgentOpsEvidenceCollection`",
        "",
        "This is the implementation outline for the evidence robot used in the P0 demo.",
        "",
        "## Workflow",
        "",
        "1. Read `case_id`, `service_name`, and change-ticket ID from the case context.",
        "2. Retrieve change-ticket metadata.",
        "3. Retrieve pull-request metadata and changed files.",
        "4. Attach failed test output if the agent found a regression.",
        "5. Request service-owner signoff when payment behavior or production deployment is involved.",
        "6. Write collected evidence back as AgentOps events.",
        "",
        "## Approval Policy",
        "",
    ]
    for key, value in spec["approval_policy"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "This is a local implementation outline. Do not claim a live UiPath Robot run until the workflow is built and executed in UiPath.",
        ]
    )
    ROBOT_README.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_package_readme(spec: dict[str, Any]) -> None:
    lines = [
        "# UiPath Implementation Package",
        "",
        "This directory contains local implementation artifacts for turning the AgentOps case model into a UiPath Maestro / Robot / Action Center build.",
        "",
        "## Files",
        "",
        "- `package-manifest.json` — generated by `scripts/simulate_maestro_case.py`",
        "- `case-data-model.json` — case variable model",
        "- `orchestrator-queues.json` — robot queue shape",
        "- `maestro-process.bpmn` — BPMN-style process blueprint",
        "- `action-center-form-schema.json` — approval form schema",
        "- `robot-workflow-pseudocode.md` — evidence robot implementation outline",
        "",
        "## Process",
        "",
        f"- Name: `{spec['name']}`",
        f"- Target: `{spec['uipath_target']}`",
        f"- Boundary: `{spec['status_boundary']}`",
        "",
        "## Stopline",
        "",
        "These files are local build artifacts. Do not claim live UiPath Automation Cloud execution until imported, run, and verified.",
    ]
    PACKAGE_README.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    spec = load_spec()
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    tree = build_bpmn(spec)
    tree.write(BPMN_FILE, encoding="utf-8", xml_declaration=True)
    write_form_schema(spec)
    write_robot_readme(spec)
    write_package_readme(spec)
    print(
        json.dumps(
            {
                "status": "ok",
                "bpmn": str(BPMN_FILE.relative_to(ROOT)),
                "form_schema": str(FORM_FILE.relative_to(ROOT)),
                "robot_outline": str(ROBOT_README.relative_to(ROOT)),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
