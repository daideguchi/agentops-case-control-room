# AgentOps Case Control Room — Simple Product Brief

## One Sentence

AgentOps Case Control Room is a UiPath-powered case room that helps companies safely manage work done by humans, AI agents, robots, and APIs together.

## Who Uses It?

Operations teams inside a company.

Examples:

- a support team
- an IT operations team
- a release management team
- an automation team
- a compliance-heavy team using AI agents

## What Problem Do They Have?

AI agents can help with real work, but real work can be risky.

An AI agent might:

- suggest a production deploy
- run a command
- update a file
- call an API
- summarize evidence
- miss an important warning
- sound confident even when evidence is weak

The human team needs to know:

- What did the AI do?
- What evidence did it use?
- Did a robot or API check the facts?
- Was anything risky?
- Did a human approve it?
- Can another person continue the work later?

## How Does This Product Solve It?

It turns agent work into a case.

Each case has stages:

1. Intake
2. Agent Investigation
3. Robot/API Evidence Collection
4. Risk Review
5. Human Approval
6. Handoff

UiPath is the orchestration layer. The AI agent does not just act alone. UiPath keeps the work organized, routes evidence collection to robots/APIs, and sends risky steps to humans for approval.

## Demo Scenario

A coding agent wants to help release a payment-service change.

The system finds:

- the pull request touches payment retry behavior
- a regression test failed
- the agent tried to deploy to production

The production deployment is blocked.

A human asks for more evidence.

The service owner rejects the release until the regression is fixed.

The final handoff report records every important event ID.

## Why It Matters

Companies do not just need faster AI.

They need AI work that can be trusted, paused, checked, approved, rejected, and handed off.

This product makes agentic work safe enough for real enterprise operations.

## Why UiPath Is Essential

Without UiPath, this is just an AI dashboard.

With UiPath, it becomes a governed business case:

- robots gather evidence
- APIs provide system facts
- humans approve or reject risky actions
- the case moves through stages
- the audit trail survives after the AI conversation ends

## Submission Message

```text
AI agents can work fast. UiPath makes their work governable.
```

