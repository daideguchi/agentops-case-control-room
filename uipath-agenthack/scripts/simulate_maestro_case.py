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


def build_case_data_model(process_spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": "AgentOpsCase",
        "source": str(PROCESS_SPEC_FILE.relative_to(ROOT)),
        "fields": process_spec["process_variables"]
        + [
            {"name": "current_stage", "type": "String", "example": "Human Approval"},
            {"name": "blocked_action_count", "type": "Int32", "example": 1},
            {"name": "evidence_event_ids", "type": "String[]", "example": ["evt-0005", "evt-0007"]},
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


def write_report(packet: dict[str, Any], stage_results: list[StageResult], action_tasks: list[dict[str, Any]]) -> None:
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
            "## Claim Boundary",
            "",
            "Safe claim: local case packet, process spec, Action Center task model, robot queue items, and simulated case trace exist.",
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

    case_run = {
        "case_id": packet["case_id"],
        "case_name": packet["case_name"],
        "status": packet["current_status"],
        "max_risk": packet["max_risk"],
        "stage_results": [result.__dict__ for result in stage_results],
        "blocked_action_count": sum(1 for event in packet["events"] if event["status"] == "blocked"),
        "human_task_count": len(action_tasks),
        "robot_work_item_count": len(robot_work_items),
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
    PACKAGE_MANIFEST_FILE.write_text(json.dumps(build_manifest(packet, process_spec), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_trace(stage_results)
    write_report(packet, stage_results, action_tasks)

    print(
        json.dumps(
            {
                "status": "ok",
                "case_id": packet["case_id"],
                "stages": len(stage_results),
                "action_center_tasks": len(action_tasks),
                "robot_work_items": len(robot_work_items),
                "blocked_action_count": case_run["blocked_action_count"],
                "manifest": str(PACKAGE_MANIFEST_FILE.relative_to(ROOT)),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
