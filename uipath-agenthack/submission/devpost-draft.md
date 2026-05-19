# Devpost Draft — AgentOps Case Control Room

## Tagline

Turn AI-agent work into a UiPath-governed case with evidence, risk, approval, and handoff.

## What It Does

AgentOps Case Control Room helps operations teams manage work where humans, AI agents, robots, APIs, and business systems all touch the same process.

The prototype records every important step as an AgentOps event:

- who acted
- what tool or robot ran
- what evidence was collected
- what risk was detected
- when human approval was required
- what decision was made
- what should be handed off next

The flagship demo is an AI Agent Operations Exception Review. A coding agent investigates a production release, a UiPath robot gathers ticket and pull-request context, the system detects a failing test and a risky deployment, and the production action is blocked until humans review the evidence.

## Problem

Enterprise teams are adopting AI agents, but real work is not a single prompt. Real work is a case.

When an agent touches production systems, customer data, financial flows, or support cases, teams need more than automation speed. They need control:

- Was the agent acting on current evidence?
- Did it attempt something risky?
- Was a human asked before a sensitive action?
- Can a second human or AI resume the work without guessing?
- Can the company explain what happened after the fact?

## UiPath Fit

UiPath is the orchestration layer.

The case stages map cleanly to a UiPath Maestro Case:

1. Intake
2. Agent Investigation
3. Robot/API Evidence Collection
4. Risk Review
5. Human Approval
6. Handoff

The generated case packet lives at:

```text
../shared-agentops-engine/adapters/uipath/case_packet.json
```

## Built With

- Python standard library artifact generator
- Static HTML dashboard
- AgentOps event schema
- UiPath-oriented case packet export
- Local Maestro runtime simulator
- Action Center task model and approval demo
- BPMN-style Maestro process blueprint
- UiPath Robot queue/work-item model
- Human approval and risk signal model

UiPath implementation target:

- UiPath Automation Cloud
- UiPath Maestro Case
- UiPath Robot task for evidence collection
- Action Center style approval gate

## What Is Working Now

- Canonical event stream generated from one command
- 26 recorded events across 3 cases
- 5 human approval gates
- 1 blocked production action
- 1 redaction event
- Evidence-grounded handoff report
- UiPath case packet export
- Local dashboard in `../shared-agentops-engine/web/index.html`
- UiPath case room in `prototype/maestro-case-room.html`
- Action Center-style approval demo in `action-center/action-center-demo.html`
- Simulated Maestro case run in `runtime/maestro-simulated-case-run.json`
- Robot work-item export in `runtime/robot-work-items.json`
- UiPath implementation package in `uipath-package/`

Local verification:

```bash
bash scripts/run_uipath_local_checks.sh
```

Observed:

- shared verifier: `verify_ok`
- UiPath verifier: `uipath_verify_ok`
- Action Center tasks: 3
- Robot work items: 2
- Blocked action count: 1

## Why It Matters

AI agents can work fast, but companies need work they can govern.

AgentOps Case Control Room lets agents contribute without forcing humans to trust a black box. Every action becomes part of a case. Every risk can be routed to a human. Every final decision has evidence.

## Next Build Step

Import the generated process blueprint and task models into UiPath Automation Cloud / Maestro, then verify a live case run before claiming platform execution.

Current boundary:

```text
The local prototype and UiPath-ready implementation package are verified. Live UiPath Cloud execution is the next verification step.
```
