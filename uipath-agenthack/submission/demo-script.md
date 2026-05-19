# Demo Script — AgentOps Case Control Room

Target length: under 5 minutes.

## 0:00 - 0:25 Opening

Enterprise AI work is becoming a case, not a chat.

This demo shows how UiPath can govern work that moves between a human, an AI coding agent, a robot, APIs, and approval gates.

## 0:25 - 1:10 Case Intake

Show the case room metrics and the AI Agent Operations Exception Review case.

Say:

```text
A release bot proposed a production change. The operations lead opens a case instead of letting the agent act directly.
```

Point to:

- `CASE-AI-OPS-001`
- 11 events
- 3 approval gates
- max risk: critical

## 1:10 - 2:00 Evidence Collection

Show the event timeline.

Say:

```text
The AI agent creates a read-only investigation plan. Then a UiPath robot gathers the change ticket and pull request context. APIs provide additional system evidence.
```

Point to:

- `evt-0002` agent plan
- `evt-0003` UiPath robot task
- `evt-0004` GitHub API evidence

## 2:00 - 2:50 Risk Detection

Show the risk cards and critical event.

Say:

```text
The system finds a failing regression test and blocks a production deployment attempt. This is the core value: AI is allowed to help, but risky action is governed.
```

Point to:

- `evt-0005` failed regression test
- `evt-0006` risk escalation
- `evt-0007` blocked production deploy

## 2:50 - 3:45 Human Approval

Show the Action Center approval demo.

Say:

```text
Instead of approving blindly, the human requests more evidence. The UiPath robot routes the request to the service owner, who rejects the release until the regression is fixed.
```

Point to:

- `evt-0008` human requested more evidence
- `evt-0009` robot requested owner signoff
- `evt-0010` service owner rejected release
- 3 Action Center tasks
- 2 Robot evidence work items
- 1 blocked production action

## 3:45 - 4:35 Handoff

Show `runtime/maestro-simulated-run-report.md` and `uipath-package/package-manifest.json`.

Say:

```text
At the end, another human or another AI can resume the case from facts, not memory. The handoff cites event IDs, risks, approvals, and final decisions.
```

Point to:

- `uipath-package/maestro-process.bpmn`
- `uipath-package/action-center-form-schema.json`
- `runtime/case_execution_trace.jsonl`

## 4:35 - 5:00 Close

Say:

```text
AgentOps Case Control Room makes AI-agent work enterprise-ready by turning it into a UiPath-governed case.
```
