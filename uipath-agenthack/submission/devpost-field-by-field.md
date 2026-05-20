# Devpost Field-By-Field Draft — AgentOps Case Control Room

Use this file as the copy source for the UiPath AgentHack Devpost form.

Final submitted public page:

```text
https://devpost.com/software/agentops-case-control-room
```

## Project Title

```text
AgentOps Case Control Room
```

## Tagline / Short Description

```text
Turn AI-agent work into a UiPath-governed case with evidence, risk, approval, robot work items, and human handoff.
```

## Submission URLs

Live demo:

```text
https://daideguchi.github.io/agentops-case-control-room/
```

GitHub repository:

```text
https://github.com/daideguchi/agentops-case-control-room
```

Demo video:

```text
https://www.youtube.com/watch?v=BxALGpCLZd4
```

Direct media fallback:

```text
https://raw.githubusercontent.com/daideguchi/agentops-case-control-room/main/uipath-agenthack/media/agentops-case-control-room-demo.mp4
```

Presentation deck:

```text
https://daideguchi.github.io/agentops-case-control-room/uipath-agenthack/submission/agentops-case-control-room-deck.pdf
```

Coding Agent evidence:

```text
https://daideguchi.github.io/agentops-case-control-room/CODING_AGENT_EVIDENCE.md
```

## Inspiration

AI agents are starting to feel like coworkers. They can investigate issues, call tools, run scripts, and suggest production actions. That can save time, but a business cannot approve real work from a chat transcript. It needs a case: evidence, risk, approval gates, robot work items, and a clean handoff.

I built this from inside a real human-AI working rhythm. While building with AI coding agents, the surprising part was not that agents could move quickly. The harder part was knowing what they did, what evidence they used, what was still risky, when a human should stop the work, and how another person or another AI could safely continue later.

That is the world AgentOps Case Control Room is designed for.

AI agents are starting to do real operational work. Real businesses cannot run on trust-me summaries.

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

The result is a case room where a human can understand what the agent did, what evidence was collected, what risk was found, what was blocked, and how the work can be resumed later.

The product is not trying to make agents invisible. It makes their work visible enough that humans can trust, challenge, stop, resume, and eventually delegate more safely.

## How We Built It

The project is built as a verified local prototype plus a UiPath-ready implementation package.

It includes:

- a shared AgentOps event stream
- a UiPath-oriented case packet
- a Maestro-style case room
- an Action Center-style approval task model
- robot evidence work items
- Orchestrator transaction lifecycle logs
- Action Center decision lifecycle logs
- a deterministic case state machine
- a BPMN-style process blueprint
- a case data model
- an approval form schema
- a UiPath import-readiness checklist with an explicit live-platform stopline
- a local runtime simulator
- a captioned narrated demo video
- a presentation deck
- repeatable verification scripts

The main verification command is:

```bash
cd uipath-agenthack
bash scripts/run_uipath_local_checks.sh
```

Observed output:

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

## Built With

```text
Python, HTML, CSS, JSON, JSONL, BPMN-style process artifact, UiPath Maestro case model target, UiPath Robot work-item model target, Action Center-style approval model, OpenAI Codex
```

## Coding Agent Usage

This project used OpenAI Codex as a coding agent.

Codex contributed to:

- generating the shared AgentOps event schema and sample event stream
- generating the UiPath-oriented case packet
- building the Maestro-style case room
- building the Action Center-style approval demo
- exporting robot work items and a BPMN-style process blueprint
- generating case state, Orchestrator transaction, and Action Center decision logs
- creating local verification scripts
- creating the public GitHub Pages demo entry
- creating submission-package documents and demo videos
- running repeatable verification commands before public push

Verifiable evidence is included here:

```text
https://daideguchi.github.io/agentops-case-control-room/CODING_AGENT_EVIDENCE.md
```

## Challenges

The hardest part was turning a broad human-AI operations story into a concrete workflow that judges can inspect quickly.

The solution needed to show real artifacts and verification without overclaiming live platform execution before a UiPath Automation Cloud import has been verified.

That is why the repository includes a clear claim boundary, implementation package, repeatable local checks, and public demo assets.

## Accomplishments

- Built a full case-room demo
- Generated a UiPath-oriented case packet
- Created Action Center-style approval tasks
- Created robot evidence work items
- Added Orchestrator transaction lifecycle logs
- Added Action Center decision lifecycle logs
- Added a deterministic state machine with blocked, more-evidence, owner-signoff, and rejected paths
- Exported a BPMN-style process blueprint
- Added a case data model and approval form schema
- Added local verification scripts
- Added a GitHub Pages live demo
- Added a presentation deck
- Added Coding Agent evidence
- Published a clean public repository

## What We Learned

AI operations need more than autonomy.

They need case structure, approval boundaries, evidence, and resumable handoff.

The strongest role for a platform like UiPath is not just running automation faster. It is making automation and AI-agent work governable.

The future is not just humans using AI tools. It is humans and AI agents sharing work. For that to be useful instead of chaotic, the work needs an operating layer that both humans and future agents can understand.

## What's Next

The next step is to import the generated process, queue, and approval models into UiPath Automation Cloud / Maestro and verify a live case run.

After that, the product can expand from one release-risk case into a reusable case-control pattern for support operations, IT operations, release management, and compliance-heavy automation teams.

## Claim Boundary

```text
This is a verified local prototype and UiPath-ready implementation package.
Live UiPath Automation Cloud execution is not claimed yet.
```

## Media Checklist

Use these assets in the media section if the form allows them:

- `uipath-agenthack/media/uipath-case-room-full.png`
- `uipath-agenthack/media/action-center-demo-full.png`
- `shared-agentops-engine/media/shared-dashboard-full.png`
- `uipath-agenthack/media/generated/devpost-thumbnail.png`
- `uipath-agenthack/media/agentops-case-control-room-demo.mp4`
- `uipath-agenthack/submission/agentops-case-control-room-deck.pdf`

## Final Submit Stopline

DD approved final submission. Devpost now shows the project submitted to UiPath AgentHack, and the public page embeds the Natural English YouTube demo video.
