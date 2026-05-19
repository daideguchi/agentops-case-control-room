# AgentOps Case Control Room

Target: UiPath AgentHack

URL: https://uipath-agenthack.devpost.com/

Status: Devpost joined. P0 flagship lane.

Current local proof:

- UiPath-focused case room: `prototype/maestro-case-room.html`
- UiPath case room screenshot: `media/uipath-case-room-full.png`
- Action Center approval demo: `action-center/action-center-demo.html`
- Action Center screenshot: `media/action-center-demo-full.png`
- Rebuild script: `scripts/build_case_room.py`
- Runtime simulator: `scripts/simulate_maestro_case.py`
- UiPath blueprint exporter: `scripts/export_uipath_blueprint.py`
- State machine: `runtime/case-state-machine.json`
- Orchestrator transaction log: `runtime/orchestrator-transaction-log.jsonl`
- Action Center decision log: `runtime/action-center-decision-log.jsonl`
- Import-readiness checklist: `uipath-package/import-readiness-checklist.json`

![UiPath case room](media/uipath-case-room-full.png)

## Position

P0 flagship.

For the plain-language product explanation, read:

- `PROJECT_BRIEF.md`

This is currently the highest win-probability lane because it combines:

- large prize pool
- lower participant count than Google/FIND EVIL
- strong fit with human-in-the-loop orchestration
- explicit value for coding-agent-powered development
- enterprise workflow relevance

## Product Thesis

AI agents, robots, humans, and APIs are all becoming part of one work process.

The hardest problem is no longer "can we automate a step?"

The harder problem is:

```text
Who did what, what changed, what needs human approval, and how does the case move safely to completion?
```

AgentOps Case Control Room turns a messy human-AI operational workflow into a UiPath-governed case.

## MVP

- case intake
- AI agent investigation step
- UiPath robot/API task step
- human approval gate
- risk/cost signal panel
- final handoff report

## Shared Engine Use

Use the Human-AI Operations Control Plane event schema and adapt it into UiPath case stages.

Current generated prototype:

- Shared engine: `../shared-agentops-engine/`
- Canonical event stream: `../shared-agentops-engine/data/agentops_events.jsonl`
- UiPath case packet: `../shared-agentops-engine/adapters/uipath/case_packet.json`
- Maestro stage outline: `../shared-agentops-engine/adapters/uipath/maestro_case_stages.md`
- Local dashboard: `../shared-agentops-engine/web/index.html`
- Evidence-grounded handoff report: `../shared-agentops-engine/reports/handoff_report.md`
- Dashboard screenshot: `../shared-agentops-engine/media/shared-dashboard-full.png`

![Shared AgentOps dashboard](../shared-agentops-engine/media/shared-dashboard-full.png)

## Rebuild And Verify

Shared engine:

```bash
cd /Users/dd/000_AI組織/__hackason/shared-agentops-engine
python3 scripts/generate_portfolio_artifacts.py
python3 scripts/verify_artifacts.py
```

UiPath case room:

```bash
cd /Users/dd/000_AI組織/__hackason/uipath-agenthack
bash scripts/run_uipath_local_checks.sh
```

Expected proof:

- shared generator returns `status: ok`
- shared verifier returns `verify_ok`
- UiPath case room generator returns `status: ok`
- UiPath simulator returns `status: ok`
- UiPath package verifier returns `uipath_verify_ok`
- verifier reports `json=11`, `jsonl=3`, `state_machine=ClosedRejected`
- case room HTML exists at `prototype/maestro-case-room.html`
- Action Center demo exists at `action-center/action-center-demo.html`
- screenshot exists at `media/uipath-case-room-full.png`
- screenshot exists at `media/action-center-demo-full.png`

## Submission Package

- Plain-language product brief: `PROJECT_BRIEF.md`
- Devpost draft: `submission/devpost-draft.md`
- Demo script: `submission/demo-script.md`
- Submit readiness checklist: `submission/submit-readiness-checklist.md`
- Architecture draft: `architecture/architecture_diagram.md`
- Maestro process spec: `architecture/maestro-process-spec.json`
- Maestro implementation plan: `architecture/maestro-implementation-plan.md`
- Simulated case run: `runtime/maestro-simulated-case-run.json`
- Case state machine: `runtime/case-state-machine.json`
- Orchestrator transaction log: `runtime/orchestrator-transaction-log.jsonl`
- Action Center decision log: `runtime/action-center-decision-log.jsonl`
- Action Center task model: `action-center/action-center-tasks.json`
- Robot work items: `runtime/robot-work-items.json`
- UiPath implementation package: `uipath-package/`
- UiPath official-source notes: `research/uipath-maestro-source-notes.md`

## Why This Can Win

Most automation demos show one happy path.

This product shows the harder enterprise problem: an AI agent tries to move real work forward, but the system catches risk, gathers evidence, routes approval to a human, and preserves a case record that another human or AI can safely resume.

UiPath is not just a backend automation tool here. UiPath is the orchestration and governance layer that makes agentic work usable inside a real business process.

## Demo Story

Scenario:

```text
AI Agent Operations Exception Review
```

Flow:

1. A human opens a release-risk case.
2. A coding agent investigates the release and produces structured AgentOps events.
3. A UiPath robot gathers the ticket, pull request, owner, and deployment context.
4. The control plane detects a failing test and a risky production deploy attempt.
5. The deployment is blocked until human approval.
6. The human asks for more evidence.
7. The service owner rejects the release until the regression is fixed.
8. The system generates a handoff report with event IDs and decisions.

Submission one-liner:

```text
AgentOps Case Control Room turns AI-agent work into a UiPath-governed case, with evidence, risk, approval, and handoff built into the workflow.
```

## Immediate Next Steps

1. Confirm UiPath Automation Cloud access.
2. Confirm UiPath Labs access form.
3. Convert `case_packet.json` into a UiPath Maestro Case data model.
4. Build the first visual case flow and Action Center approval mock.
5. Capture dashboard and case-stage screenshots for README and Devpost.

Stopline:

- Do not claim real UiPath platform integration until it is verified.
- Do not final-submit the hackathon entry until DD explicitly approves.
