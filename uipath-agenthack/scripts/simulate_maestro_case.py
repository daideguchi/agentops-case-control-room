#!/usr/bin/env python3
"""Simulate the UiPath Maestro case runtime from the generated case packet.

This does not call UiPath Cloud. It creates deterministic import/implementation
artifacts that mirror what the live Maestro build should persist: case state,
robot work items, Action Center tasks, policy-gateway decisions, and final
handoff output.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = ROOT.parent / "shared-agentops-engine"
CASE_PACKET_FILE = SHARED_ROOT / "adapters" / "uipath" / "case_packet.json"
PROCESS_SPEC_FILE = ROOT / "architecture" / "maestro-process-spec.json"
RUNTIME_DIR = ROOT / "runtime"
PACKAGE_DIR = ROOT / "uipath-package"
ACTION_DIR = ROOT / "action-center"

CASE_RUN_FILE = RUNTIME_DIR / "maestro-simulated-case-run.json"
TRACE_FILE = RUNTIME_DIR / "case_execution_trace.jsonl"
ACTION_TASKS_FILE = ACTION_DIR / "action-center-tasks.json"
ROBOT_QUEUE_FILE = RUNTIME_DIR / "robot-work-items.json"
ORCHESTRATOR_QUEUE_FILE = PACKAGE_DIR / "orchestrator-queues.json"
CASE_SCHEMA_FILE = PACKAGE_DIR / "case-data-model.json"
PACKAGE_MANIFEST_FILE = PACKAGE_DIR / "package-manifest.json"
REPORT_FILE = RUNTIME_DIR / "maestro-simulated-run-report.md"
TRANSACTION_LOG_FILE = RUNTIME_DIR / "orchestrator-transaction-log.jsonl"
ACTION_DECISION_LOG_FILE = RUNTIME_DIR / "action-center-decision-log.jsonl"
STATE_MACHINE_FILE = RUNTIME_DIR / "case-state-machine.json"
ACTION_PAYLOADS_FILE = PACKAGE_DIR / "action-center-task-payloads.json"
IMPORT_READINESS_FILE = PACKAGE_DIR / "import-readiness-checklist.json"
STATE_TRANSITION_TABLE_FILE = PACKAGE_DIR / "maestro-state-transition-table.md"

RISK_WEIGHT = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass(frozen=True)
class StageResult:
    stage_id: str
    stage_name: str
    owner: str
    status: str
    max_risk: str
    event_ids: list[str]
    decision: str


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def max_risk(events: list[dict[str, Any]]) -> str:
    if not events:
        return "none"
    return max(events, key=lambda row: RISK_WEIGHT[row["risk_level"]])["risk_level"]


def stage_status(events: list[dict[str, Any]]) -> str:
    if any(event["status"] == "blocked" for event in events):
        return "blocked"
    if any(event["status"] == "failed" for event in events):
        return "failed"
    if any(event["status"] == "warning" for event in events):
        return "warning"
    return "completed"


def stage_decision(events: list[dict[str, Any]]) -> str:
    decisions = [event.get("decision", "none") for event in events if event.get("decision") not in {None, "none"}]
    return decisions[-1] if decisions else "none"


def build_stage_results(packet: dict[str, Any]) -> list[StageResult]:
    by_id = {event["event_id"]: event for event in packet["events"]}
    results: list[StageResult] = []
    for index, stage in enumerate(packet["stages"], start=1):
        events = [by_id[event_id] for event_id in stage["evidence_events"]]
        results.append(
            StageResult(
                stage_id=f"stage-{index:02d}",
                stage_name=stage["stage"],
                owner=stage["owner"],
                status=stage_status(events),
                max_risk=max_risk(events),
                event_ids=stage["evidence_events"],
                decision=stage_decision(events),
            )
        )
    return results


def build_action_center_tasks(packet: dict[str, Any]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for event in packet["events"]:
        if not event.get("human_approval_required") and event.get("decision") in {None, "none"}:
            continue
        tasks.append(
            {
                "task_id": f"act-{event['event_id']}",
                "case_id": event["case_id"],
                "title": approval_title(event),
                "assigned_to_role": approval_role(event),
                "status": "completed",
                "decision": event.get("decision", "none"),
                "risk_level": event["risk_level"],
                "source_event_id": event["event_id"],
                "summary": event["summary"],
                "available_actions": ["approve", "reject", "request_more_evidence"],
            }
        )
    return tasks


def approval_title(event: dict[str, Any]) -> str:
    if event.get("decision") == "blocked_by_policy":
        return "Production deployment blocked by policy"
    if event.get("decision") == "needs_more_evidence":
        return "Request service-owner evidence"
    if event.get("decision") == "rejected":
        return "Reject release until regression is fixed"
    return "Review case decision"


def approval_role(event: dict[str, Any]) -> str:
    if event.get("actor_name") == "service-owner":
        return "Service Owner"
    return "Operations Lead"


def build_robot_work_items(packet: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for event in packet["events"]:
        if event["actor_type"] != "robot":
            continue
        items.append(
            {
                "queue_item_id": f"robot-{event['event_id']}",
                "queue_name": "AgentOpsEvidenceCollection",
                "case_id": event["case_id"],
                "robot": event["actor_name"],
                "action": event.get("action", "unknown"),
                "target": event.get("target", ""),
                "status": event["status"],
                "duration_ms": event.get("duration_ms", 0),
                "source_event_id": event["event_id"],
                "summary": event["summary"],
            }
        )
    return items


def build_orchestrator_transaction_log(robot_work_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    transactions: list[dict[str, Any]] = []
    for index, item in enumerate(robot_work_items, start=1):
        transaction_id = f"txn-{index:04d}-{item['source_event_id']}"
        final_status = "Successful" if item["status"] == "success" else "BusinessException"
        for step, transaction_status in enumerate(["New", "InProgress", final_status], start=1):
            row: dict[str, Any] = {
                "transaction_id": transaction_id,
                "queue_item_id": item["queue_item_id"],
                "queue_name": item["queue_name"],
                "case_id": item["case_id"],
                "source_event_id": item["source_event_id"],
                "robot": item["robot"],
                "transaction_status": transaction_status,
                "retry_number": 0,
                "step_sequence": step,
            }
            if transaction_status == final_status:
                row["output"] = {
                    "action": item["action"],
                    "target": item["target"],
                    "duration_ms": item["duration_ms"],
                    "summary": item["summary"],
                }
            transactions.append(row)
    return transactions


def build_action_decision_log(action_tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []
    for task in action_tasks:
        for step, task_status in enumerate(["Created", "Assigned", "Completed"], start=1):
            row: dict[str, Any] = {
                "task_id": task["task_id"],
                "case_id": task["case_id"],
                "source_event_id": task["source_event_id"],
                "assigned_to_role": task["assigned_to_role"],
                "task_status": task_status,
                "risk_level": task["risk_level"],
                "step_sequence": step,
            }
            if task_status == "Completed":
                row["decision"] = task["decision"]
                row["decision_summary"] = task["summary"]
            decisions.append(row)
    return decisions


def build_action_payloads(action_tasks: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "form_family": "AgentOpsActionCenterReview",
        "claim_boundary": "local payload contract for UiPath Action Center or Apps import; not live-imported yet",
        "tasks": [
            {
                "task_id": task["task_id"],
                "form_title": task["title"],
                "assigned_to_role": task["assigned_to_role"],
                "source_event_id": task["source_event_id"],
                "available_actions": task["available_actions"],
                "fields": [
                    {"name": "case_id", "type": "Text", "required": True, "value": task["case_id"]},
                    {"name": "risk_level", "type": "SingleSelect", "required": True, "value": task["risk_level"]},
                    {"name": "source_event_id", "type": "Text", "required": True, "value": task["source_event_id"]},
                    {"name": "evidence_summary", "type": "Paragraph", "required": True, "value": task["summary"]},
                    {"name": "moderator_decision", "type": "SingleSelect", "required": True, "value": task["decision"]},
                ],
            }
            for task in action_tasks
        ],
    }


def build_case_state_machine(
    packet: dict[str, Any], process_spec: dict[str, Any], stage_results: list[StageResult]
) -> dict[str, Any]:
    stage_status_by_name = {stage.stage_name: stage.status for stage in stage_results}
    states = [
        {
            "state_id": "Intake",
            "label": "Production release exception opened",
            "owner": "Human",
            "status": stage_status_by_name.get("Intake", "completed"),
            "evidence_events": ["evt-0001"],
        },
        {
            "state_id": "AgentInvestigation",
            "label": "AI agent investigates with read-only tools",
            "owner": "AI Agent",
            "status": stage_status_by_name.get("Agent Investigation", "completed"),
            "evidence_events": ["evt-0002", "evt-0005"],
        },
        {
            "state_id": "RobotEvidenceCollection",
            "label": "UiPath robot gathers ticket, PR, owner, and test evidence",
            "owner": "UiPath Robot",
            "status": stage_status_by_name.get("Robot/API Evidence Collection", "completed"),
            "evidence_events": ["evt-0003", "evt-0004", "evt-0009"],
        },
        {
            "state_id": "RiskReview",
            "label": "Policy gateway reviews risk and evidence completeness",
            "owner": "Control Plane",
            "status": stage_status_by_name.get("Risk Review", "warning"),
            "evidence_events": ["evt-0006", "evt-0007"],
        },
        {
            "state_id": "HumanApproval",
            "label": "Action Center routes blocked production action to a human",
            "owner": "Action Center",
            "status": stage_status_by_name.get("Human Approval", "blocked"),
            "evidence_events": ["evt-0007", "evt-0008"],
        },
        {
            "state_id": "OwnerSignoff",
            "label": "Service owner reviews failed-test evidence",
            "owner": "Service Owner",
            "status": "completed",
            "evidence_events": ["evt-0009", "evt-0010"],
        },
        {
            "state_id": "Handoff",
            "label": "Recorder writes an event-linked handoff",
            "owner": "Recorder",
            "status": stage_status_by_name.get("Handoff", "completed"),
            "evidence_events": ["evt-0011"],
        },
        {
            "state_id": "ClosedRejected",
            "label": "Release rejected until regression evidence is fixed",
            "owner": "Maestro Case",
            "status": "terminal",
            "evidence_events": ["evt-0010", "evt-0011"],
        },
    ]
    transitions = [
        {"from": "Intake", "to": "AgentInvestigation", "when": "case_opened", "source_event_id": "evt-0001"},
        {
            "from": "AgentInvestigation",
            "to": "RobotEvidenceCollection",
            "when": "needs_external_evidence",
            "source_event_id": "evt-0002",
        },
        {
            "from": "RobotEvidenceCollection",
            "to": "RiskReview",
            "when": "evidence_collected",
            "source_event_id": "evt-0003",
        },
        {
            "from": "RiskReview",
            "to": "HumanApproval",
            "when": "max_risk_is_high_or_action_is_blocked",
            "source_event_id": "evt-0007",
        },
        {
            "from": "HumanApproval",
            "to": "RobotEvidenceCollection",
            "when": "needs_more_evidence",
            "source_event_id": "evt-0008",
        },
        {
            "from": "RobotEvidenceCollection",
            "to": "OwnerSignoff",
            "when": "owner_evidence_attached",
            "source_event_id": "evt-0009",
        },
        {
            "from": "OwnerSignoff",
            "to": "Handoff",
            "when": "release_rejected",
            "source_event_id": "evt-0010",
        },
        {"from": "Handoff", "to": "ClosedRejected", "when": "handoff_report_written", "source_event_id": "evt-0011"},
    ]
    return {
        "case_id": packet["case_id"],
        "process_name": process_spec["name"],
        "initial_state": "Intake",
        "final_state": "ClosedRejected",
        "states": states,
        "transitions": transitions,
        "claim_boundary": "local deterministic state machine derived from the case packet; not a live Maestro run yet",
    }


def build_import_readiness_checklist(process_spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "package": process_spec["name"],
        "status": "ready_for_manual_uipath_import_review",
        "stopline": "blocked_until_platform_verification: do not claim live UiPath Automation Cloud execution before import and live run proof",
        "items": [
            {
                "area": "Maestro case flow",
                "status": "ready_local",
                "artifact": "architecture/maestro-process-spec.json",
                "review_note": "Case states, owners, risk gateway, and terminal rejection path are specified.",
            },
            {
                "area": "BPMN-style process",
                "status": "ready_local",
                "artifact": "uipath-package/maestro-process.bpmn",
                "review_note": "Import shape exists as a process blueprint, not a verified UiPath export.",
            },
            {
                "area": "Orchestrator queue",
                "status": "ready_local",
                "artifact": "uipath-package/orchestrator-queues.json",
                "review_note": "Robot queue item payloads include source event IDs and lifecycle logs.",
            },
            {
                "area": "Action Center payloads",
                "status": "ready_local",
                "artifact": "uipath-package/action-center-task-payloads.json",
                "review_note": "Human decision tasks include available actions and evidence fields.",
            },
            {
                "area": "Case data model",
                "status": "ready_local",
                "artifact": "uipath-package/case-data-model.json",
                "review_note": "Core process variables and event references are mapped.",
            },
            {
                "area": "Cloud import",
                "status": "needs_cloud_import",
                "artifact": "UiPath Automation Cloud",
                "review_note": "Requires manual import/build in UiPath Maestro, Orchestrator, and Action Center.",
            },
            {
                "area": "Live execution proof",
                "status": "blocked_until_platform_verification",
                "artifact": "UiPath Automation Cloud run evidence",
                "review_note": "Need a live run ID, queue transaction ID, Action Center task ID, and screenshots before claiming live execution.",
            },
        ],
    }


def build_case_data_model(process_spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": "AgentOpsCase",
        "source": str(PROCESS_SPEC_FILE.relative_to(ROOT)),
        "fields": process_spec["process_variables"]
        + [
            {"name": "current_stage", "type": "String", "example": "Human Approval"},
            {"name": "blocked_action_count", "type": "Int32", "example": 1},
            {"name": "evidence_event_ids", "type": "String[]", "example": ["evt-0005", "evt-0007"]},
            {"name": "orchestrator_transaction_ids", "type": "String[]", "example": ["txn-0001-evt-0003"]},
            {"name": "action_center_task_ids", "type": "String[]", "example": ["act-evt-0007"]},
            {"name": "final_state", "type": "String", "example": "ClosedRejected"},
        ],
        "claim_boundary": "local schema for UiPath build planning; not imported into Automation Cloud yet",
    }


def build_manifest(packet: dict[str, Any], process_spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_name": "AgentOps Case Control Room",
        "version": "0.1.0-local",
        "target": "UiPath Maestro Case + Robot + Action Center",
        "status": "local_implementation_package_not_cloud_verified",
        "source_case_packet": str(CASE_PACKET_FILE.relative_to(ROOT.parent)),
        "source_process_spec": str(PROCESS_SPEC_FILE.relative_to(ROOT)),
        "case_id": packet["case_id"],
        "process_name": process_spec["name"],
        "included_artifacts": [
            str(CASE_RUN_FILE.relative_to(ROOT)),
            str(TRACE_FILE.relative_to(ROOT)),
            str(ACTION_TASKS_FILE.relative_to(ROOT)),
            str(ROBOT_QUEUE_FILE.relative_to(ROOT)),
            str(ORCHESTRATOR_QUEUE_FILE.relative_to(ROOT)),
            str(CASE_SCHEMA_FILE.relative_to(ROOT)),
            str(TRANSACTION_LOG_FILE.relative_to(ROOT)),
            str(ACTION_DECISION_LOG_FILE.relative_to(ROOT)),
            str(STATE_MACHINE_FILE.relative_to(ROOT)),
            str(ACTION_PAYLOADS_FILE.relative_to(ROOT)),
            str(IMPORT_READINESS_FILE.relative_to(ROOT)),
            str(STATE_TRANSITION_TABLE_FILE.relative_to(ROOT)),
            str(REPORT_FILE.relative_to(ROOT)),
        ],
        "stopline": "Do not claim live UiPath Automation Cloud execution until imported and verified.",
    }


def write_trace(stage_results: list[StageResult]) -> None:
    with TRACE_FILE.open("w", encoding="utf-8") as fh:
        for result in stage_results:
            fh.write(
                json.dumps(
                    {
                        "stage_id": result.stage_id,
                        "stage_name": result.stage_name,
                        "owner": result.owner,
                        "status": result.status,
                        "max_risk": result.max_risk,
                        "decision": result.decision,
                        "event_ids": result.event_ids,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_state_transition_table(machine: dict[str, Any]) -> None:
    lines = [
        "# Maestro State Transition Table",
        "",
        "Local deterministic state-machine contract for the UiPath Maestro build. This is not a live UiPath Cloud export.",
        "",
        "| From | To | When | Evidence |",
        "|---|---|---|---|",
    ]
    for transition in machine["transitions"]:
        lines.append(
            f"| `{transition['from']}` | `{transition['to']}` | `{transition['when']}` | `{transition['source_event_id']}` |"
        )
    STATE_TRANSITION_TABLE_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(
    packet: dict[str, Any],
    stage_results: list[StageResult],
    action_tasks: list[dict[str, Any]],
    transaction_log: list[dict[str, Any]],
    action_decision_log: list[dict[str, Any]],
    state_machine: dict[str, Any],
) -> None:
    blocked = sum(1 for stage in stage_results if stage.status == "blocked")
    failed = sum(1 for stage in stage_results if stage.status == "failed")
    high_risk = sum(1 for stage in stage_results if stage.max_risk in {"high", "critical"})
    lines = [
        "# Maestro Simulated Run Report",
        "",
        "This is a local simulation from the generated UiPath case packet. It is not a live UiPath Cloud execution.",
        "",
        f"- case: `{packet['case_id']}`",
        f"- status: `{packet['current_status']}`",
        f"- stages: {len(stage_results)}",
        f"- blocked stages: {blocked}",
        f"- failed stages: {failed}",
        f"- high/critical stages: {high_risk}",
        f"- Action Center tasks: {len(action_tasks)}",
        f"- Orchestrator transaction events: {len(transaction_log)}",
        f"- Action Center decision events: {len(action_decision_log)}",
        f"- final state: `{state_machine['final_state']}`",
        "",
        "## Stage Results",
        "",
    ]
    for stage in stage_results:
        lines.append(
            f"- `{stage.stage_id}` {stage.stage_name}: {stage.status}, risk={stage.max_risk}, decision={stage.decision}, events={', '.join(stage.event_ids)}"
        )
    lines.extend(
        [
            "",
            "## UiPath Runtime Package",
            "",
            f"- case state machine: `{STATE_MACHINE_FILE.relative_to(ROOT)}`",
            f"- Orchestrator transaction log: `{TRANSACTION_LOG_FILE.relative_to(ROOT)}`",
            f"- Action Center decision log: `{ACTION_DECISION_LOG_FILE.relative_to(ROOT)}`",
            f"- Action Center task payloads: `{ACTION_PAYLOADS_FILE.relative_to(ROOT)}`",
            f"- import readiness checklist: `{IMPORT_READINESS_FILE.relative_to(ROOT)}`",
            "",
            "## Claim Boundary",
            "",
            "Safe claim: local case packet, process spec, state machine, Action Center task model, robot queue items, transaction lifecycle logs, and simulated case trace exist.",
            "",
            "Do not claim: live UiPath Automation Cloud / Maestro / Action Center execution.",
        ]
    )
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    packet = load_json(CASE_PACKET_FILE)
    process_spec = load_json(PROCESS_SPEC_FILE)
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    ACTION_DIR.mkdir(parents=True, exist_ok=True)

    stage_results = build_stage_results(packet)
    action_tasks = build_action_center_tasks(packet)
    robot_work_items = build_robot_work_items(packet)
    transaction_log = build_orchestrator_transaction_log(robot_work_items)
    action_decision_log = build_action_decision_log(action_tasks)
    action_payloads = build_action_payloads(action_tasks)
    state_machine = build_case_state_machine(packet, process_spec, stage_results)
    import_readiness = build_import_readiness_checklist(process_spec)

    case_run = {
        "case_id": packet["case_id"],
        "case_name": packet["case_name"],
        "status": packet["current_status"],
        "max_risk": packet["max_risk"],
        "stage_results": [result.__dict__ for result in stage_results],
        "blocked_action_count": sum(1 for event in packet["events"] if event["status"] == "blocked"),
        "human_task_count": len(action_tasks),
        "robot_work_item_count": len(robot_work_items),
        "orchestrator_transaction_event_count": len(transaction_log),
        "action_center_decision_event_count": len(action_decision_log),
        "final_state": state_machine["final_state"],
    }

    CASE_RUN_FILE.write_text(json.dumps(case_run, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    ACTION_TASKS_FILE.write_text(json.dumps(action_tasks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    ROBOT_QUEUE_FILE.write_text(json.dumps(robot_work_items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    ORCHESTRATOR_QUEUE_FILE.write_text(
        json.dumps(
            {
                "queues": [
                    {
                        "name": "AgentOpsEvidenceCollection",
                        "purpose": "collect release, pull-request, owner, and failed-test evidence",
                        "items": robot_work_items,
                    }
                ]
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    CASE_SCHEMA_FILE.write_text(json.dumps(build_case_data_model(process_spec), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    ACTION_PAYLOADS_FILE.write_text(json.dumps(action_payloads, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    STATE_MACHINE_FILE.write_text(json.dumps(state_machine, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    IMPORT_READINESS_FILE.write_text(json.dumps(import_readiness, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    PACKAGE_MANIFEST_FILE.write_text(json.dumps(build_manifest(packet, process_spec), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_trace(stage_results)
    write_jsonl(TRANSACTION_LOG_FILE, transaction_log)
    write_jsonl(ACTION_DECISION_LOG_FILE, action_decision_log)
    write_state_transition_table(state_machine)
    write_report(packet, stage_results, action_tasks, transaction_log, action_decision_log, state_machine)

    print(
        json.dumps(
            {
                "status": "ok",
                "case_id": packet["case_id"],
                "stages": len(stage_results),
                "action_center_tasks": len(action_tasks),
                "robot_work_items": len(robot_work_items),
                "orchestrator_transaction_events": len(transaction_log),
                "action_center_decision_events": len(action_decision_log),
                "final_state": state_machine["final_state"],
                "blocked_action_count": case_run["blocked_action_count"],
                "manifest": str(PACKAGE_MANIFEST_FILE.relative_to(ROOT)),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
