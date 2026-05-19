# Coding Agent Evidence

This project used OpenAI Codex as a coding agent during development.

## Tool Used

- Coding agent: OpenAI Codex
- Role: implementation, verification, documentation, public repository preparation, and submission packaging

## How The Coding Agent Contributed

Codex contributed to the working solution by:

- generating the shared AgentOps event schema and sample event stream
- generating the UiPath-oriented case packet
- building the Maestro-style case room
- building the Action Center-style approval demo
- exporting robot work items and a BPMN-style process blueprint
- creating local verification scripts
- creating the public GitHub Pages demo entry
- creating submission-package documents and draft demo videos
- running repeatable verification commands before public push

## Meaningful Integration

The coding-agent output is not just referenced in a writeup. It is integrated into the repository as runnable artifacts:

- `shared-agentops-engine/scripts/generate_portfolio_artifacts.py`
- `shared-agentops-engine/scripts/verify_artifacts.py`
- `uipath-agenthack/scripts/run_uipath_local_checks.sh`
- `uipath-agenthack/scripts/build_case_room.py`
- `uipath-agenthack/scripts/simulate_maestro_case.py`
- `uipath-agenthack/scripts/export_uipath_blueprint.py`
- `uipath-agenthack/scripts/build_action_center_demo.py`
- `uipath-agenthack/scripts/verify_uipath_package.py`
- `uipath-agenthack/scripts/build_demo_video.sh`
- `index.html`

## Verifiable Evidence

The following can be independently checked:

1. Public commit history in this repository.
2. Local verification command:

```bash
cd uipath-agenthack
bash scripts/run_uipath_local_checks.sh
```

3. Expected verification output:

```text
verify_ok
uipath_verify_ok
json=8
html=2
xml=1
screenshots=2
```

4. Public live demo:

```text
https://daideguchi.github.io/agentops-case-control-room/
```

5. Draft demo video:

```text
uipath-agenthack/media/agentops-case-control-room-demo-draft.mp4
```

## Human Control Boundary

Codex generated and modified implementation artifacts, but the project concept, product direction, final positioning, and submit/no-submit decisions remain human-controlled.

This mirrors the product thesis: AI agents can do valuable work, but important operational decisions need evidence, review, and human accountability.
