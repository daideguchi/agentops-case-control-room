# UiPath AgentHack — Handoff

## 2026-05-19 Start

DD requested running multiple promising hackathons in parallel.

This lane is P0 flagship because it has the best mix of:

- $50,000 prize pool
- observed participant count around 444
- deadline with enough runway: 2026-06-29 11:45pm PDT
- strong alignment with human-in-the-loop orchestration
- explicit bonus for using coding agents such as Codex, Claude Code, Cursor, and Gemini CLI

## Selected Track

Recommended:

```text
Track 1: UiPath Maestro Case
```

Reason:

AgentOps Case Control Room is dynamic and exception-heavy. It should move work through stages, involve handoffs between agents, robots, and people, and keep humans in charge at key decision points.

This exactly matches the observed Track 1 wording.

## Product Direction

AgentOps Case Control Room

One sentence:

```text
An enterprise case-management console that uses UiPath to orchestrate AI agents, robots, APIs, and human approvals while preserving evidence, risk signals, cost signals, and handoff history.
```

## Official Requirements Observed

Submission must include:

- Devpost project page
- demo video max 5 minutes
- public GitHub repository
- solution built on UiPath Automation Cloud
- README with UiPath components, setup, prerequisites, and coding-agent/low-code-agent usage
- presentation deck using provided template

UiPath page also says:

- solutions must run on UiPath Automation Cloud
- UiPath must be the orchestration and governance layer
- external agents/frameworks/LLMs are welcome
- coding agents through UiPath for Coding Agents receive bonus points

## Registration / Access Status

- Devpost registration completed.
- Evidence: `../00_parallel_portfolio/evidence/2026-05-19_uipath-agenthack_joined.png`
- UiPath Labs access form is required after registration.
- Do not submit personal forms or accept new terms without DD approval.

## 2026-05-19 Shared Prototype Built

Created shared engine assets under:

```text
../shared-agentops-engine/
```

Confirmed generation:

- 26 canonical AgentOps events
- 3 reusable cases
- 5 human approval gates
- 1 blocked production action
- 1 redaction event
- static dashboard at `../shared-agentops-engine/web/index.html`
- UiPath adapter at `../shared-agentops-engine/adapters/uipath/case_packet.json`
- Maestro outline at `../shared-agentops-engine/adapters/uipath/maestro_case_stages.md`

Created UiPath submission prep:

- `submission/devpost-draft.md`
- `submission/demo-script.md`
- `architecture/architecture_diagram.md`

## 2026-05-19 UiPath Case Room Built

Created a UiPath-focused local demo screen generated from the shared UiPath case packet:

- generator: `scripts/build_case_room.py`
- HTML output: `prototype/maestro-case-room.html`
- screenshot: `media/uipath-case-room-full.png`
- runtime simulator: `scripts/simulate_maestro_case.py`
- simulated run: `runtime/maestro-simulated-case-run.json`
- simulated run report: `runtime/maestro-simulated-run-report.md`
- Action Center task model: `action-center/action-center-tasks.json`
- Action Center demo: `action-center/action-center-demo.html`
- Action Center screenshot: `media/action-center-demo-full.png`
- UiPath blueprint exporter: `scripts/export_uipath_blueprint.py`
- UiPath package directory: `uipath-package/`
- Maestro process spec: `architecture/maestro-process-spec.json`
- Maestro implementation plan: `architecture/maestro-implementation-plan.md`
- readiness checklist: `submission/submit-readiness-checklist.md`
- official-source notes: `research/uipath-maestro-source-notes.md`

Verification run:

```bash
cd /Users/dd/000_AI組織/__hackason/uipath-agenthack
python3 scripts/build_case_room.py
```

Observed output:

- `status: ok`
- `event_count: 11`
- `stage_count: 6`

This is still a local prototype/export, not verified UiPath Automation Cloud integration.

Additional verification:

```bash
python3 scripts/simulate_maestro_case.py
python3 scripts/export_uipath_blueprint.py
python3 scripts/build_action_center_demo.py
python3 scripts/verify_uipath_package.py
```

Observed output:

- simulator: `status: ok`
- action_center_tasks: 3
- robot_work_items: 2
- blocked_action_count: 1
- verifier: `uipath_verify_ok`

## Immediate Next Steps

1. Confirm UiPath Automation Cloud / Labs access.
2. Convert `case_packet.json` into a real UiPath Maestro Case data model if access allows.
3. Reuse `prototype/maestro-case-room.html` as the fallback demo backbone if platform access blocks.
4. Capture any real UiPath screenshots only after real platform verification.
5. Keep final Devpost submission blocked until DD explicitly approves.
