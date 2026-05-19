# Submission Package — AgentOps Case Control Room

## Project Title

AgentOps Case Control Room

## Short Description

Turn AI-agent work into a UiPath-governed case with evidence, risk, approval, robot work items, and human handoff.

## Repository

https://github.com/daideguchi/agentops-case-control-room

## Devpost Submission

https://devpost.com/software/agentops-case-control-room

## Live Demo

https://daideguchi.github.io/agentops-case-control-room/

## YouTube Demo

https://www.youtube.com/watch?v=UIofHgD2blw

## Presentation Deck

- HTML deck: `uipath-agenthack/submission/agentops-case-control-room-deck.html`
- PDF deck: `uipath-agenthack/submission/agentops-case-control-room-deck.pdf`

## Devpost Field Draft

- `uipath-agenthack/submission/devpost-field-by-field.md`

## Coding Agent Evidence

- `CODING_AGENT_EVIDENCE.md`
- Coding agent used: OpenAI Codex
- Contribution: implementation, verification, documentation, public repository preparation, and submission packaging
- Evidence: public commit history, runnable scripts, local verification output, and integrated generated artifacts

## Try It Out

Open the live demo or these local demo files after cloning the repository:

- `uipath-agenthack/prototype/maestro-case-room.html`
- `uipath-agenthack/action-center/action-center-demo.html`
- `shared-agentops-engine/web/index.html`

## Screenshots

- `uipath-agenthack/media/uipath-case-room-full.png`
- `uipath-agenthack/media/action-center-demo-full.png`
- `shared-agentops-engine/media/shared-dashboard-full.png`
- `uipath-agenthack/media/generated/devpost-thumbnail.png`

## Demo Video

Captioned narrated video:

- YouTube: `https://www.youtube.com/watch?v=UIofHgD2blw`
- Local file: `uipath-agenthack/media/agentops-case-control-room-demo.mp4`

Regenerate:

```bash
cd uipath-agenthack
bash scripts/build_demo_video.sh
```

## Inspiration

I built this from inside a real human-AI working rhythm. While building with AI coding agents, the surprising part was not that agents could move quickly. The harder part was knowing what they did, what evidence they used, what was still risky, when a human should stop the work, and how another person or another AI could safely continue later.

That is the world AgentOps Case Control Room is designed for. AI agents will help with real operational work, but real businesses cannot run on chat transcripts and trust-me summaries. They need cases, evidence, approval gates, robot work items, and handoffs.

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

The product is not trying to make agents invisible. It makes their work visible enough that humans can trust, challenge, stop, resume, and eventually delegate more safely.

## How We Built It

- Python standard library artifact generators
- AgentOps event schema
- UiPath-oriented case packet export
- Maestro-style case room HTML
- Action Center-style approval task model
- Robot work-item model
- Orchestrator transaction lifecycle log
- Action Center decision lifecycle log
- Deterministic case state machine
- BPMN-style process blueprint
- UiPath import-readiness checklist
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
json=11
jsonl=3
html=2
markdown=2
xml=1
screenshots=2
state_machine=ClosedRejected
transaction_events=6
action_decision_events=9
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
- Added Orchestrator transaction lifecycle logs
- Added Action Center decision lifecycle logs
- Added a case state machine with blocked, more-evidence, owner-signoff, and rejected paths
- Exported a BPMN-style process blueprint
- Added local verification scripts
- Published a clean public repository

## What We Learned

AI operations need more than autonomy. They need case structure, approval boundaries, evidence, and resumable handoff.

The future is not just humans using AI tools. It is humans and AI agents sharing work. For that to be useful instead of chaotic, the work needs an operating layer that both humans and future agents can understand.

## What's Next

Import the generated process, queue, and approval models into UiPath Automation Cloud / Maestro and verify a live case run.

## Claim Boundary

This is a verified local prototype and UiPath-ready implementation package.

It does not claim live UiPath Automation Cloud execution yet.
