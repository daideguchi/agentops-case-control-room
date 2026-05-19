# Maestro Simulated Run Report

This is a local simulation from the generated UiPath case packet. It is not a live UiPath Cloud execution.

- case: `CASE-AI-OPS-001`
- status: `release_rejected_until_evidence_fixed`
- stages: 6
- blocked stages: 2
- failed stages: 1
- high/critical stages: 2
- Action Center tasks: 3
- Orchestrator transaction events: 6
- Action Center decision events: 9
- final state: `ClosedRejected`

## Stage Results

- `stage-01` Intake: completed, risk=none, decision=none, events=evt-0001
- `stage-02` Agent Investigation: failed, risk=medium, decision=none, events=evt-0002, evt-0005
- `stage-03` Robot/API Evidence Collection: completed, risk=low, decision=none, events=evt-0003, evt-0004, evt-0009
- `stage-04` Risk Review: blocked, risk=critical, decision=blocked_by_policy, events=evt-0006, evt-0007
- `stage-05` Human Approval: blocked, risk=critical, decision=rejected, events=evt-0007, evt-0008, evt-0010
- `stage-06` Handoff: completed, risk=none, decision=none, events=evt-0011

## UiPath Runtime Package

- case state machine: `runtime/case-state-machine.json`
- Orchestrator transaction log: `runtime/orchestrator-transaction-log.jsonl`
- Action Center decision log: `runtime/action-center-decision-log.jsonl`
- Action Center task payloads: `uipath-package/action-center-task-payloads.json`
- import readiness checklist: `uipath-package/import-readiness-checklist.json`

## Claim Boundary

Safe claim: local case packet, process spec, state machine, Action Center task model, robot queue items, transaction lifecycle logs, and simulated case trace exist.

Do not claim: live UiPath Automation Cloud / Maestro / Action Center execution.
