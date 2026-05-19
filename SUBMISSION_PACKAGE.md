# Submission Package — AgentOps Case Control Room

## Project Title

AgentOps Case Control Room

## Short Description

Turn AI-agent work into a UiPath-governed case with evidence, risk, approval, robot work items, and human handoff.

## Repository

https://github.com/daideguchi/agentops-case-control-room

## Try It Out

Open these local demo files after cloning the repository:

- `uipath-agenthack/prototype/maestro-case-room.html`
- `uipath-agenthack/action-center/action-center-demo.html`
- `shared-agentops-engine/web/index.html`

## Screenshots

- `uipath-agenthack/media/uipath-case-room-full.png`
- `uipath-agenthack/media/action-center-demo-full.png`
- `shared-agentops-engine/media/shared-dashboard-full.png`

## Demo Video

Draft silent video:

- `uipath-agenthack/media/agentops-case-control-room-demo-draft.mp4`

Regenerate:

```bash
cd uipath-agenthack
bash scripts/build_demo_video.sh
```

## Inspiration

AI agents are starting to do real operational work. They investigate issues, call tools, run scripts, and suggest production actions. That can save time, but it also creates a governance problem: real business work cannot be just a chat transcript.

AgentOps Case Control Room was built around a simple idea: when AI helps with operational work, the work should become a governed case with evidence, approval gates, robot work items, and a handoff trail.

## What It Does

AgentOps Case Control Room records human, AI, robot, API, and system actions as structured case events.

The flagship demo is a production release exception:

- a human opens a release-risk case
- an AI coding agent creates a read-only investigation plan
- a UiPath-style robot gathers ticket and pull request evidence
- a policy gateway detects a failing regression test
- a risky production deployment is blocked
- Action Center-style tasks route the decision to humans
- the final handoff preserves event IDs, evidence, risk, and decisions

## How We Built It

- Python standard library artifact generators
- AgentOps event schema
- UiPath-oriented case packet export
- Maestro-style case room HTML
- Action Center-style approval task model
- Robot work-item model
- BPMN-style process blueprint
- Local runtime simulator
- Evidence-linked handoff report

## Built With

- Python
- HTML/CSS
- JSON / JSONL
- BPMN-style process artifact
- UiPath Maestro case model target
- UiPath Robot queue/work-item model target
- UiPath Action Center approval model target

## What Is Working

```text
verify_ok
uipath_verify_ok
json=8
html=2
xml=1
screenshots=2
```

## Verification Commands

```bash
cd uipath-agenthack
bash scripts/run_uipath_local_checks.sh
bash scripts/build_demo_video.sh
```

## Demo Script Summary

1. Show the case room and the production release exception.
2. Show evidence collection by the AI agent, robot, and API.
3. Show the failing regression test and blocked production deployment.
4. Show Action Center-style human approval tasks.
5. Show the handoff report and UiPath implementation package.

## What Makes It Different

Most AI-agent demos focus on speed. This project focuses on governability.

The agent is useful, but it is not allowed to become an invisible operator. Every meaningful action is part of a case. Risky actions are blocked until humans review the evidence.

## Challenges

The main challenge was turning a broad human-AI operations story into a concrete, judge-readable workflow. The project needed enough UiPath mapping to feel real, while staying honest about what has and has not been live-imported into Automation Cloud.

## Accomplishments

- Built a full case-room demo
- Generated a UiPath-oriented case packet
- Created Action Center-style approval tasks
- Created robot work items
- Exported a BPMN-style process blueprint
- Added local verification scripts
- Published a clean public repository

## What We Learned

AI operations need more than autonomy. They need case structure, approval boundaries, evidence, and resumable handoff.

## What's Next

Import the generated process, queue, and approval models into UiPath Automation Cloud / Maestro and verify a live case run.

## Claim Boundary

This is a verified local prototype and UiPath-ready implementation package.

It does not claim live UiPath Automation Cloud execution yet.
