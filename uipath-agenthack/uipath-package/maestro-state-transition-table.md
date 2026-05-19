# Maestro State Transition Table

Local deterministic state-machine contract for the UiPath Maestro build. This is not a live UiPath Cloud export.

| From | To | When | Evidence |
|---|---|---|---|
| `Intake` | `AgentInvestigation` | `case_opened` | `evt-0001` |
| `AgentInvestigation` | `RobotEvidenceCollection` | `needs_external_evidence` | `evt-0002` |
| `RobotEvidenceCollection` | `RiskReview` | `evidence_collected` | `evt-0003` |
| `RiskReview` | `HumanApproval` | `max_risk_is_high_or_action_is_blocked` | `evt-0007` |
| `HumanApproval` | `RobotEvidenceCollection` | `needs_more_evidence` | `evt-0008` |
| `RobotEvidenceCollection` | `OwnerSignoff` | `owner_evidence_attached` | `evt-0009` |
| `OwnerSignoff` | `Handoff` | `release_rejected` | `evt-0010` |
| `Handoff` | `ClosedRejected` | `handoff_report_written` | `evt-0011` |
