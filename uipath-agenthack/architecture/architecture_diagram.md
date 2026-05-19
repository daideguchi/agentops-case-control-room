# Architecture Diagram Draft

```text
Human Operations Lead
        |
        v
UiPath Maestro Case
        |
        +--> Case Intake
        |
        +--> AI Agent Investigation
        |       |
        |       v
        |   AgentOps Event Stream
        |
        +--> UiPath Robot Evidence Collection
        |       |
        |       +--> Change Ticket
        |       +--> Pull Request
        |       +--> Service Owner
        |
        +--> API Evidence Collection
        |       |
        |       +--> GitHub API
        |       +--> Test Results
        |
        +--> Risk Review
        |       |
        |       +--> failing test detected
        |       +--> production deploy blocked
        |       +--> cost/risk signals recorded
        |
        +--> Human Approval Gate
        |       |
        |       +--> approve
        |       +--> reject
        |       +--> request more evidence
        |
        +--> Action Center Task Model
        |       |
        |       +--> 3 human approval tasks
        |
        +--> Orchestrator Queue Model
        |       |
        |       +--> 2 robot evidence work items
        |
        v
Evidence-Grounded Handoff Report
        |
        v
Next Human or AI Worker
```

## Data Objects

- Case packet: `../shared-agentops-engine/adapters/uipath/case_packet.json`
- Canonical events: `../shared-agentops-engine/data/agentops_events.jsonl`
- Handoff report: `../shared-agentops-engine/reports/handoff_report.md`
- Simulated runtime: `../uipath-agenthack/runtime/maestro-simulated-case-run.json`
- Action Center tasks: `../uipath-agenthack/action-center/action-center-tasks.json`
- Robot work items: `../uipath-agenthack/runtime/robot-work-items.json`
- BPMN blueprint: `../uipath-agenthack/uipath-package/maestro-process.bpmn`

## Judging Message

UiPath is the place where agentic work becomes governable work.
