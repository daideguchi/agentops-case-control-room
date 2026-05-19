#!/usr/bin/env python3
"""Verify UiPath lane local artifacts."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

JSON_FILES = [
    "architecture/maestro-process-spec.json",
    "runtime/maestro-simulated-case-run.json",
    "runtime/case-state-machine.json",
    "action-center/action-center-tasks.json",
    "runtime/robot-work-items.json",
    "uipath-package/orchestrator-queues.json",
    "uipath-package/case-data-model.json",
    "uipath-package/package-manifest.json",
    "uipath-package/action-center-form-schema.json",
    "uipath-package/action-center-task-payloads.json",
    "uipath-package/import-readiness-checklist.json",
]

JSONL_FILES = [
    "runtime/case_execution_trace.jsonl",
    "runtime/orchestrator-transaction-log.jsonl",
    "runtime/action-center-decision-log.jsonl",
]

HTML_CHECKS = {
    "prototype/maestro-case-room.html": ["Maestro Case Flow", "Human Approval Queue"],
    "action-center/action-center-demo.html": ["Every risky agent action becomes a human approval task", "Production deployment blocked by policy"],
}

SCREENSHOTS = [
    "media/uipath-case-room-full.png",
    "media/action-center-demo-full.png",
]

XML_FILES = [
    ("uipath-package/maestro-process.bpmn", ["<bpmn:definitions", "<bpmn:process", "Process_AgentOpsCaseControlRoom"]),
]

MD_FILES = [
    ("runtime/maestro-simulated-run-report.md", ["Orchestrator transaction log", "Action Center decision log", "ClosedRejected"]),
    ("uipath-package/maestro-state-transition-table.md", ["HumanApproval", "OwnerSignoff", "ClosedRejected"]),
]


def load_json(path: Path, rel_path: str, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid json {rel_path}: {exc}")
        return {}


def load_jsonl(path: Path, rel_path: str, errors: list[str]) -> list[dict]:
    rows: list[dict] = []
    try:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                errors.append(f"invalid jsonl {rel_path}:{line_number}: {exc}")
    except OSError as exc:
        errors.append(f"cannot read jsonl {rel_path}: {exc}")
    return rows


def main() -> None:
    errors: list[str] = []
    loaded_json: dict[str, dict] = {}
    loaded_jsonl: dict[str, list[dict]] = {}

    for rel_path in JSON_FILES:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing json: {rel_path}")
            continue
        loaded_json[rel_path] = load_json(path, rel_path, errors)

    for rel_path in JSONL_FILES:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing jsonl: {rel_path}")
            continue
        rows = load_jsonl(path, rel_path, errors)
        loaded_jsonl[rel_path] = rows
        if not rows:
            errors.append(f"empty jsonl: {rel_path}")

    parser = HTMLParser()
    for rel_path, needles in HTML_CHECKS.items():
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing html: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        parser.feed(text)
        for needle in needles:
            if needle not in text:
                errors.append(f"missing text in {rel_path}: {needle}")

    for rel_path, needles in XML_FILES:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing xml: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"missing xml marker in {rel_path}: {needle}")

    for rel_path, needles in MD_FILES:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing markdown: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"missing markdown marker in {rel_path}: {needle}")

    for rel_path in SCREENSHOTS:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing screenshot: {rel_path}")
        elif path.stat().st_size < 10_000:
            errors.append(f"screenshot too small: {rel_path}")

    case_run = loaded_json.get("runtime/maestro-simulated-case-run.json", {})
    if case_run.get("final_state") != "ClosedRejected":
        errors.append("case run final_state must be ClosedRejected")

    state_machine = loaded_json.get("runtime/case-state-machine.json", {})
    transition_targets = {transition.get("to") for transition in state_machine.get("transitions", [])}
    if state_machine.get("final_state") != "ClosedRejected":
        errors.append("state machine final_state must be ClosedRejected")
    if "RobotEvidenceCollection" not in transition_targets or "OwnerSignoff" not in transition_targets:
        errors.append("state machine must include more-evidence and owner-signoff paths")

    queue_model = loaded_json.get("uipath-package/orchestrator-queues.json", {})
    queue_items = [item for queue in queue_model.get("queues", []) for item in queue.get("items", [])]
    if not queue_items:
        errors.append("orchestrator queue must include robot queue items")
    for item in queue_items:
        if not item.get("source_event_id"):
            errors.append(f"queue item missing source_event_id: {item.get('queue_item_id')}")
        if item.get("status") not in {"success", "failed", "blocked", "warning"}:
            errors.append(f"queue item has unexpected source status: {item.get('queue_item_id')}")

    transaction_rows = loaded_jsonl.get("runtime/orchestrator-transaction-log.jsonl", [])
    transaction_statuses = {row.get("transaction_status") for row in transaction_rows}
    if not {"New", "InProgress", "Successful"}.issubset(transaction_statuses):
        errors.append("orchestrator transaction log must include New, InProgress, and Successful states")
    if any(not row.get("source_event_id") for row in transaction_rows):
        errors.append("orchestrator transaction log rows must include source_event_id")

    decision_rows = loaded_jsonl.get("runtime/action-center-decision-log.jsonl", [])
    decisions = {row.get("decision") for row in decision_rows if row.get("task_status") == "Completed"}
    if not {"blocked_by_policy", "needs_more_evidence", "rejected"}.issubset(decisions):
        errors.append("Action Center decision log must include blocked_by_policy, needs_more_evidence, and rejected")

    payloads = loaded_json.get("uipath-package/action-center-task-payloads.json", {})
    payload_tasks = payloads.get("tasks", [])
    if len(payload_tasks) < 3:
        errors.append("Action Center payloads must include at least three task payloads")
    if any(not task.get("source_event_id") for task in payload_tasks):
        errors.append("Action Center payload tasks must include source_event_id")

    checklist = loaded_json.get("uipath-package/import-readiness-checklist.json", {})
    checklist_text = json.dumps(checklist, ensure_ascii=False)
    if "blocked_until_platform_verification" not in checklist_text:
        errors.append("import readiness checklist must include the cloud verification stopline")

    manifest = loaded_json.get("uipath-package/package-manifest.json", {})
    included = set(manifest.get("included_artifacts", []))
    required_manifest_artifacts = {
        "runtime/orchestrator-transaction-log.jsonl",
        "runtime/action-center-decision-log.jsonl",
        "runtime/case-state-machine.json",
        "uipath-package/action-center-task-payloads.json",
        "uipath-package/import-readiness-checklist.json",
        "uipath-package/maestro-state-transition-table.md",
    }
    missing_from_manifest = sorted(required_manifest_artifacts - included)
    if missing_from_manifest:
        errors.append(f"manifest missing artifacts: {', '.join(missing_from_manifest)}")

    if errors:
        print("uipath_verify_failed")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("uipath_verify_ok")
    print(f"json={len(JSON_FILES)}")
    print(f"jsonl={len(JSONL_FILES)}")
    print(f"html={len(HTML_CHECKS)}")
    print(f"markdown={len(MD_FILES)}")
    print(f"xml={len(XML_FILES)}")
    print(f"screenshots={len(SCREENSHOTS)}")
    print("state_machine=ClosedRejected")
    print(f"transaction_events={len(transaction_rows)}")
    print(f"action_decision_events={len(decision_rows)}")


if __name__ == "__main__":
    main()
