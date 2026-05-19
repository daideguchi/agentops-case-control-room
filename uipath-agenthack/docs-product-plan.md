# AgentOps Case Control Room — Product Plan

## Product Thesis

Enterprise AI is moving from chat into operations.

But real business work is not a single prompt. It is a case:

- intake
- investigation
- evidence gathering
- exception handling
- approval
- execution
- handoff
- audit

AgentOps Case Control Room uses UiPath as the orchestration layer for a human-AI case workflow.

## Target User

- operations teams
- enterprise automation teams
- AI platform teams
- compliance-heavy teams adopting agents
- teams that want coding agents in production workflows without losing governance

## Track Fit

Track 1: UiPath Maestro Case.

The product should be shown as an exception-heavy case flow:

```text
AI agent finds problem -> robot gathers records -> API checks system -> human approves risky step -> case completes with evidence handoff.
```

## Demo Scenario

Suggested scenario:

```text
Vendor onboarding / invoice exception / customer escalation case.
```

Best current scenario:

```text
AI Agent Operations Exception Review
```

Why:

- directly shows coding agents
- reuses DD's real human-AI operations theme
- can show risk/cost/approval handoffs clearly
- differentiates from generic invoice demos

## Workflow Stages

1. Intake
   - new agent work request or incident case
   - classify process type and risk

2. Agent Investigation
   - external coding agent gathers evidence
   - outputs structured events

3. Robot/API Evidence Collection
   - UiPath robot/API workflow collects system records
   - normalizes into case packet

4. Risk Review
   - detects destructive command, account mismatch, retry loop, high cost, secret redaction

5. Human Approval
   - human approves, rejects, or requests more evidence

6. Execution / Remediation
   - approved action proceeds
   - unapproved action remains blocked

7. Handoff Report
   - final case summary
   - evidence IDs
   - decisions
   - next steps

## UI Needs

At minimum:

- case timeline
- current stage
- risk queue
- approval queue
- actor map: human / robot / AI agent / API
- final handoff report

## Technical Needs

Local prototype first:

- shared event schema
- sample case generator
- web dashboard
- export format for UiPath

UiPath phase:

- Maestro Case stages
- action center / approval step if available
- robot/API workflow placeholder
- case data object

## Submission Story

This is not just automation.

This is the governance layer for enterprise agentic work:

```text
Agents can work faster, but UiPath makes the work governable.
```

