# UiPath Robot Workflow Pseudocode

Target queue: `AgentOpsEvidenceCollection`

This is the implementation outline for the evidence robot used in the P0 demo.

## Workflow

1. Read `case_id`, `service_name`, and change-ticket ID from the case context.
2. Retrieve change-ticket metadata.
3. Retrieve pull-request metadata and changed files.
4. Attach failed test output if the agent found a regression.
5. Request service-owner signoff when payment behavior or production deployment is involved.
6. Write collected evidence back as AgentOps events.

## Approval Policy

- `production_deploy`: `requires_human_approval`
- `payment_behavior_change`: `requires_owner_signoff`
- `failed_regression`: `blocks_release_until_fixed`
- `missing_evidence`: `route_back_to_robot_collection`

## Claim Boundary

This is a local implementation outline. Do not claim a live UiPath Robot run until the workflow is built and executed in UiPath.
