# Maestro Implementation Plan

Updated: 2026-05-19 JST

This is the bridge from the current local prototype to a real UiPath Automation Cloud / Maestro build.

## Current Truth

The local prototype is verified.

- Shared event stream: `../shared-agentops-engine/data/agentops_events.jsonl`
- UiPath case packet: `../shared-agentops-engine/adapters/uipath/case_packet.json`
- Case room UI: `../uipath-agenthack/prototype/maestro-case-room.html`
- Process spec: `architecture/maestro-process-spec.json`

Real UiPath Cloud execution is not verified yet.

## Process Shape

1. `Start Case`
   - Human opens a production release exception.
   - Evidence: `evt-0001`

2. `Agent Investigation`
   - AI agent creates a read-only plan and runs verification.
   - Evidence: `evt-0002`, `evt-0005`

3. `Robot/API Evidence Collection`
   - UiPath robot gathers ticket, pull-request, deployment, failed-test, and owner context.
   - Evidence: `evt-0003`, `evt-0004`, `evt-0009`

4. `Risk Gateway`
   - Route high/critical risk or production deploy attempts to human approval.
   - Evidence: `evt-0006`, `evt-0007`

5. `Human Approval`
   - Operations lead requests more evidence.
   - Service owner rejects the release until the regression is fixed.
   - Evidence: `evt-0008`, `evt-0010`

6. `Handoff`
   - Recorder generates the final handoff report with event IDs.
   - Evidence: `evt-0011`

## Build In UiPath

Use this sequence if UiPath Automation Cloud / Labs access becomes available:

1. Create a Maestro process named `AgentOps Case Control Room`.
2. Add variables from `architecture/maestro-process-spec.json`.
3. Add tasks for agent investigation, robot evidence collection, human approval, owner signoff, and handoff.
4. Add a gateway before any production action.
5. Connect the gateway rule to `max_risk` and `human_approval_required`.
6. Use Action Center / Apps for human approval screens.
7. Attach the event stream and handoff report as case context.
8. Capture screenshots only after the real workflow runs.

## Submission Boundary

Safe claim now:

```text
We built a verified local prototype and UiPath-ready case/process specification.
```

Do not claim yet:

```text
This has been executed inside UiPath Automation Cloud.
```

Claim that only after live platform verification.
