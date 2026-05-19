#!/usr/bin/env python3
"""Build a local Action Center style approval demo from simulated tasks."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASKS_FILE = ROOT / "action-center" / "action-center-tasks.json"
CASE_RUN_FILE = ROOT / "runtime" / "maestro-simulated-case-run.json"
OUT_FILE = ROOT / "action-center" / "action-center-demo.html"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def risk_class(risk: str) -> str:
    if risk in {"critical", "high"}:
        return "danger"
    if risk == "medium":
        return "warn"
    if risk == "low":
        return "ok"
    return "quiet"


def action_buttons(task: dict[str, Any]) -> str:
    decision = task["decision"]
    options = [
        ("Approve", "approve"),
        ("Request Evidence", "needs_more_evidence"),
        ("Reject", "rejected"),
    ]
    if decision == "blocked_by_policy":
        options[0] = ("Blocked By Policy", "blocked_by_policy")
    buttons: list[str] = []
    for label, value in options:
        selected = " selected" if value == decision else ""
        buttons.append(f'<button class="{selected.strip()}">{esc(label)}</button>')
    return "\n".join(buttons)


def task_cards(tasks: list[dict[str, Any]]) -> str:
    cards: list[str] = []
    for index, task in enumerate(tasks, start=1):
        cards.append(
            f"""
            <article class="task-card {risk_class(task["risk_level"])}">
              <div class="task-head">
                <span class="task-number">{index:02d}</span>
                <span class="risk-pill {risk_class(task["risk_level"])}">{esc(task["risk_level"])}</span>
              </div>
              <h3>{esc(task["title"])}</h3>
              <p class="role">{esc(task["assigned_to_role"])}</p>
              <p>{esc(task["summary"])}</p>
              <p class="decision-banner {risk_class(task["risk_level"])}">Recorded decision: {esc(task["decision"])}</p>
              <dl>
                <div><dt>Decision</dt><dd>{esc(task["decision"])}</dd></div>
                <div><dt>Evidence</dt><dd>{esc(task["source_event_id"])}</dd></div>
                <div><dt>Status</dt><dd>{esc(task["status"])}</dd></div>
              </dl>
              <div class="actions">
                {action_buttons(task)}
              </div>
            </article>
            """
        )
    return "\n".join(cards)


def build_html(tasks: list[dict[str, Any]], case_run: dict[str, Any]) -> str:
    cards = task_cards(tasks)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Action Center Approval Demo — AgentOps Case Control Room</title>
  <style>
    :root {{
      --bg: #f4f6f8;
      --surface: #fff;
      --ink: #182230;
      --muted: #667085;
      --line: #d8e0e8;
      --brand: #0f6cbd;
      --brand-soft: #e7f1fb;
      --ok: #087443;
      --ok-soft: #e8f6ef;
      --warn: #b54708;
      --warn-soft: #fff4e5;
      --danger: #b42318;
      --danger-soft: #ffebe9;
      --shadow: 0 16px 36px rgba(24, 34, 48, 0.08);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}

    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 28px 18px 48px;
    }}

    .locator {{
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 12px;
    }}

    .hero {{
      background: #101828;
      color: #fff;
      border-radius: 8px;
      padding: 28px;
      box-shadow: var(--shadow);
      display: grid;
      grid-template-columns: minmax(0, 1.35fr) minmax(260px, .65fr);
      gap: 24px;
      align-items: start;
    }}

    h1 {{
      margin: 0;
      font-size: 34px;
      line-height: 1.12;
      letter-spacing: 0;
    }}

    h2 {{
      margin: 0 0 12px;
      font-size: 20px;
      letter-spacing: 0;
    }}

    h3 {{
      margin: 10px 0 4px;
      font-size: 17px;
      letter-spacing: 0;
    }}

    p {{ margin: 0; }}

    .hero-copy {{
      margin-top: 14px;
      color: #d6e3f3;
      font-size: 16px;
      max-width: 740px;
    }}

    .nav-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 20px;
    }}

    .nav-links a {{
      display: inline-flex;
      align-items: center;
      min-height: 38px;
      padding: 8px 12px;
      border-radius: 7px;
      background: #fff;
      color: #101828;
      text-decoration: none;
      font-weight: 800;
      font-size: 14px;
    }}

    .nav-links a.secondary {{
      background: rgba(255,255,255,.12);
      color: #fff;
      border: 1px solid rgba(255,255,255,.24);
    }}

    .case-card {{
      background: rgba(255,255,255,.08);
      border: 1px solid rgba(255,255,255,.18);
      border-radius: 8px;
      padding: 16px;
    }}

    .case-card strong {{
      display: block;
      margin-bottom: 6px;
    }}

    .task-grid {{
      margin-top: 22px;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }}

    .decision-path {{
      margin-top: 22px;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }}

    .decision-step {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      box-shadow: 0 8px 24px rgba(24, 34, 48, .04);
    }}

    .decision-step span {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 26px;
      height: 26px;
      border-radius: 999px;
      background: var(--brand-soft);
      color: var(--brand);
      font-weight: 900;
      margin-bottom: 8px;
    }}

    .decision-step strong {{
      display: block;
      margin-bottom: 5px;
    }}

    .decision-step p {{
      color: var(--muted);
      font-size: 14px;
    }}

    .task-card {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      min-height: 430px;
      box-shadow: 0 8px 24px rgba(24, 34, 48, .04);
    }}

    .task-card.danger {{ border-color: #f2aaa4; background: linear-gradient(180deg, #fff, #fff7f6); }}
    .task-card.warn {{ border-color: #ffd49b; background: linear-gradient(180deg, #fff, #fffaf2); }}
    .task-card.ok {{ border-color: #a9dec5; background: linear-gradient(180deg, #fff, #f8fdf9); }}

    .task-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
    }}

    .task-number {{
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      color: var(--brand);
      font-weight: 800;
      font-size: 12px;
    }}

    .role {{
      color: var(--muted);
      margin-bottom: 12px;
      font-size: 14px;
    }}

    .decision-banner {{
      margin-top: 14px;
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 13px;
      font-weight: 900;
    }}

    .decision-banner.danger {{ color: var(--danger); background: var(--danger-soft); }}
    .decision-banner.warn {{ color: var(--warn); background: var(--warn-soft); }}
    .decision-banner.ok {{ color: var(--ok); background: var(--ok-soft); }}

    .risk-pill {{
      display: inline-flex;
      width: fit-content;
      min-height: 24px;
      align-items: center;
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}

    .risk-pill.danger {{ color: var(--danger); background: var(--danger-soft); }}
    .risk-pill.warn {{ color: var(--warn); background: var(--warn-soft); }}
    .risk-pill.ok {{ color: var(--ok); background: var(--ok-soft); }}

    dl {{
      display: grid;
      gap: 8px;
      margin: 18px 0 0;
    }}

    dl div {{
      display: grid;
      grid-template-columns: 88px minmax(0, 1fr);
      gap: 10px;
      border-top: 1px solid var(--line);
      padding-top: 8px;
    }}

    dt {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      font-weight: 800;
      letter-spacing: .06em;
    }}

    dd {{
      margin: 0;
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      font-size: 12px;
      overflow-wrap: anywhere;
    }}

    .actions {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 8px;
      margin-top: 18px;
    }}

    button {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      min-height: 38px;
      font-weight: 800;
      color: var(--ink);
    }}

    button.selected {{
      border-color: #7bb7f0;
      background: var(--brand-soft);
      color: var(--brand);
    }}

    @media (max-width: 920px) {{
      .hero,
      .task-grid,
      .decision-path {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 620px) {{
      main {{ padding: 16px 12px 32px; }}
      h1 {{ font-size: 27px; }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="locator">UiPath AgentHack · Action Center Approval Demo · Local Artifact</div>
    <section class="hero">
      <div>
        <h1>Every risky agent action becomes a human approval task.</h1>
        <p class="hero-copy">
          This local Action Center-style view is generated from the same case packet as the Maestro case room.
          It shows exactly what the human sees when the AI tries to move a production release forward.
        </p>
        <nav class="nav-links" aria-label="Demo navigation">
          <a href="../../index.html">Back to overview</a>
          <a class="secondary" href="../prototype/maestro-case-room.html">Open case room</a>
          <a class="secondary" href="../runtime/action-center-decision-log.jsonl">Inspect decision log</a>
        </nav>
      </div>
      <aside class="case-card">
        <strong>{esc(case_run["case_id"])}</strong>
        <p>Status: {esc(case_run["status"])}</p>
        <p>Blocked actions: {esc(case_run["blocked_action_count"])}</p>
        <p>Human tasks: {esc(case_run["human_task_count"])}</p>
      </aside>
    </section>
    <section class="decision-path" aria-label="Decision path">
      <article class="decision-step"><span>1</span><strong>Block risky action</strong><p>The production deploy is stopped before execution because approval is required.</p></article>
      <article class="decision-step"><span>2</span><strong>Request evidence</strong><p>The human reviewer asks for service-owner signoff instead of approving blindly.</p></article>
      <article class="decision-step"><span>3</span><strong>Reject until fixed</strong><p>The owner rejects the release until the regression evidence is resolved.</p></article>
    </section>
    <section class="task-grid">{cards}</section>
  </main>
</body>
</html>
"""


def main() -> None:
    tasks = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    case_run = json.loads(CASE_RUN_FILE.read_text(encoding="utf-8"))
    OUT_FILE.write_text(build_html(tasks, case_run), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "output": str(OUT_FILE.relative_to(ROOT)),
                "tasks": len(tasks),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
