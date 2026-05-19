# UiPath AgentHack Submit Readiness Checklist

Updated: 2026-05-19 21:40 JST

Status: preparing, not finally submitted.

## Current Proof Assets

- Local case room: `prototype/maestro-case-room.html`
- Case room screenshot: `media/uipath-case-room-full.png`
- Action Center approval demo: `action-center/action-center-demo.html`
- Action Center screenshot: `media/action-center-demo-full.png`
- Shared dashboard: `../shared-agentops-engine/web/index.html`
- Shared dashboard screenshot: `../shared-agentops-engine/media/shared-dashboard-full.png`
- UiPath case packet: `../shared-agentops-engine/adapters/uipath/case_packet.json`
- Maestro stage outline: `../shared-agentops-engine/adapters/uipath/maestro_case_stages.md`
- Evidence handoff report: `../shared-agentops-engine/reports/handoff_report.md`
- Simulated Maestro run: `runtime/maestro-simulated-case-run.json`
- Action Center tasks: `action-center/action-center-tasks.json`
- Robot work items: `runtime/robot-work-items.json`
- UiPath implementation package: `uipath-package/`

## Rebuild Commands

```bash
cd /Users/dd/000_AI組織/__hackason/shared-agentops-engine
python3 scripts/generate_portfolio_artifacts.py
python3 scripts/verify_artifacts.py
```

```bash
cd /Users/dd/000_AI組織/__hackason/uipath-agenthack
bash scripts/run_uipath_local_checks.sh
```

## Verified Locally

- Shared artifact generator returns `status: ok`
- Shared verifier returns `verify_ok`
- UiPath case room generator returns `status: ok`
- UiPath simulator returns `status: ok`
- UiPath blueprint exporter returns `status: ok`
- Action Center demo builder returns `status: ok`
- UiPath package verifier returns `uipath_verify_ok`
- UiPath case room screenshot captured at `media/uipath-case-room-full.png`
- Action Center screenshot captured at `media/action-center-demo-full.png`
- HTML smoke check passed for `Maestro Case Flow`, `Human Approval Queue`, and `Evidence Timeline`

## Submit Package Drafts

- Devpost draft: `submission/devpost-draft.md`
- Demo script: `submission/demo-script.md`
- Architecture diagram draft: `architecture/architecture_diagram.md`
- Maestro process spec: `architecture/maestro-process-spec.json`
- Maestro implementation plan: `architecture/maestro-implementation-plan.md`
- Simulated runtime report: `runtime/maestro-simulated-run-report.md`
- UiPath package README: `uipath-package/README.md`
- UiPath official-source notes: `research/uipath-maestro-source-notes.md`
- Plain product brief: `PROJECT_BRIEF.md`

## Not Yet Claimed

- Do not claim real UiPath Automation Cloud integration until it is actually built and verified.
- Do not claim a final Devpost submission until DD explicitly approves and the submission page is saved.
- Do not accept additional platform terms, submit personal forms, or enter billing details without DD approval.

## Next Best Step

Build or verify the real UiPath Automation Cloud / Maestro case implementation. If platform access is blocked, use the generated local case room as the demo backbone and state clearly that it is a prototype export of the intended UiPath case model.
