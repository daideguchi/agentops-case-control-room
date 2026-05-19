#!/usr/bin/env python3
"""Build the UiPath-focused case room prototype from the shared case packet."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = ROOT.parent / "shared-agentops-engine"
CASE_PACKET_FILE = SHARED_ROOT / "adapters" / "uipath" / "case_packet.json"
OUT_FILE = ROOT / "prototype" / "maestro-case-room.html"

RISK_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def event_lookup(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {event["event_id"]: event for event in events}


def risk_class(risk: str) -> str:
    if risk in {"critical", "high"}:
        return "danger"
    if risk == "medium":
        return "warn"
    if risk == "low":
        return "ok"
    return "quiet"


def build_stage_cards(packet: dict[str, Any]) -> str:
    events_by_id = event_lookup(packet["events"])
    cards: list[str] = []
    for index, stage in enumerate(packet["stages"], start=1):
        evidence_events = [events_by_id[event_id] for event_id in stage["evidence_events"]]
        max_risk = max(evidence_events, key=lambda row: RISK_ORDER[row["risk_level"]])["risk_level"]
        event_items = "\n".join(
            f"""
            <li>
              <span class="event-id">{esc(event["event_id"])}</span>
              <span>{esc(event["summary"])}</span>
            </li>
            """
            for event in evidence_events
        )
        cards.append(
            f"""
            <article class="stage-card {risk_class(max_risk)}">
              <div class="stage-topline">
                <span class="stage-number">{index:02d}</span>
                <span class="risk-pill {risk_class(max_risk)}">{esc(max_risk)}</span>
              </div>
              <h3>{esc(stage["stage"])}</h3>
              <p class="owner">{esc(stage["owner"])}</p>
              <ul class="event-list">{event_items}</ul>
            </article>
            """
        )
    return "\n".join(cards)


def build_approval_rows(events: list[dict[str, Any]]) -> str:
    approvals = [
        row
        for row in events
        if row.get("human_approval_required") or row.get("decision") not in {None, "none"}
    ]
    rows: list[str] = []
    for event in approvals:
        decision = event.get("decision", "none")
        rows.append(
            f"""
            <tr>
              <td><span class="event-id">{esc(event["event_id"])}</span></td>
              <td>{esc(event["phase"])}</td>
              <td><span class="risk-pill {risk_class(event["risk_level"])}">{esc(event["risk_level"])}</span></td>
              <td>{esc(decision)}</td>
              <td>{esc(event["summary"])}</td>
            </tr>
            """
        )
    return "\n".join(rows)


def build_timeline(events: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for event in events:
        rows.append(
            f"""
            <article class="timeline-row">
              <div>
                <span class="event-id">{esc(event["event_id"])}</span>
                <span class="actor">{esc(event["actor_type"])} / {esc(event["actor_name"])}</span>
              </div>
              <div class="timeline-main">
                <strong>{esc(event["event_type"])}</strong>
                <span>{esc(event["summary"])}</span>
              </div>
              <span class="risk-pill {risk_class(event["risk_level"])}">{esc(event["risk_level"])}</span>
            </article>
            """
        )
    return "\n".join(rows)


def build_html(packet: dict[str, Any]) -> str:
    events = packet["events"]
    counter = Counter(event["actor_type"] for event in events)
    approval_count = sum(1 for event in events if event.get("human_approval_required"))
    high_risk_count = sum(1 for event in events if event["risk_level"] in {"high", "critical"})
    blocked_count = sum(1 for event in events if event["status"] == "blocked")
    robot_api_count = counter["robot"] + counter["api"]
    final_event = events[-1]
    stage_cards = build_stage_cards(packet)
    approvals = build_approval_rows(events)
    timeline = build_timeline(events)
    status_label = str(packet["current_status"]).replace("_", " ")

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AgentOps Case Control Room — UiPath Demo</title>
  <style>
    :root {{
      --bg: #f4f6f8;
      --surface: #ffffff;
      --surface-strong: #101828;
      --text: #182230;
      --muted: #667085;
      --line: #d9e0e8;
      --brand: #0f6cbd;
      --brand-soft: #e7f1fb;
      --ok: #087443;
      --ok-soft: #e8f6ef;
      --warn: #b54708;
      --warn-soft: #fff4e5;
      --danger: #b42318;
      --danger-soft: #ffebe9;
      --shadow: 0 18px 42px rgba(16, 24, 40, 0.09);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}

    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 28px 18px 48px;
    }}

    .locator {{
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 12px;
    }}

    .hero {{
      background: var(--surface-strong);
      color: #fff;
      border-radius: 8px;
      padding: 28px;
      box-shadow: var(--shadow);
      display: grid;
      grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr);
      gap: 28px;
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
      margin: 12px 0 4px;
      font-size: 17px;
      letter-spacing: 0;
    }}

    p {{
      margin: 0;
    }}

    .hero-copy {{
      margin-top: 14px;
      color: #d6e3f3;
      font-size: 16px;
      max-width: 760px;
    }}

    .case-meta {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 8px;
      padding: 16px;
      display: grid;
      gap: 12px;
    }}

    .meta-label {{
      color: #bdcbe0;
      display: block;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .meta-value {{
      display: block;
      font-weight: 700;
      margin-top: 2px;
    }}

    .section {{
      margin-top: 22px;
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 8px 24px rgba(16, 24, 40, 0.04);
    }}

    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }}

    .metric {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      min-height: 108px;
    }}

    .metric strong {{
      display: block;
      font-size: 28px;
      line-height: 1;
      margin-bottom: 8px;
    }}

    .metric span {{
      color: var(--muted);
      font-size: 14px;
    }}

    .stage-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }}

    .stage-card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      background: #fff;
      min-height: 254px;
    }}

    .stage-card.danger {{
      border-color: #f2aaa4;
      background: linear-gradient(180deg, #fff, #fff7f6);
    }}

    .stage-card.warn {{
      border-color: #ffd49b;
      background: linear-gradient(180deg, #fff, #fffaf2);
    }}

    .stage-card.ok {{
      border-color: #a9dec5;
      background: linear-gradient(180deg, #fff, #f7fdf9);
    }}

    .stage-topline {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }}

    .stage-number {{
      color: var(--brand);
      font-weight: 800;
      font-size: 13px;
    }}

    .owner {{
      color: var(--muted);
      font-size: 14px;
      margin-bottom: 12px;
    }}

    .event-list {{
      list-style: none;
      padding: 0;
      margin: 0;
      display: grid;
      gap: 10px;
    }}

    .event-list li {{
      display: grid;
      gap: 4px;
      color: var(--text);
      font-size: 13px;
    }}

    .event-id {{
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      color: var(--brand);
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }}

    .risk-pill {{
      display: inline-flex;
      align-items: center;
      width: fit-content;
      min-height: 24px;
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .risk-pill.danger {{
      color: var(--danger);
      background: var(--danger-soft);
    }}

    .risk-pill.warn {{
      color: var(--warn);
      background: var(--warn-soft);
    }}

    .risk-pill.ok {{
      color: var(--ok);
      background: var(--ok-soft);
    }}

    .risk-pill.quiet {{
      color: var(--muted);
      background: #eef2f6;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}

    th {{
      text-align: left;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
    }}

    td {{
      border-bottom: 1px solid var(--line);
      padding: 12px 8px;
      vertical-align: top;
    }}

    .timeline {{
      display: grid;
      gap: 10px;
    }}

    .timeline-row {{
      display: grid;
      grid-template-columns: 210px minmax(0, 1fr) 92px;
      gap: 14px;
      align-items: start;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #fff;
    }}

    .actor {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-top: 4px;
    }}

    .timeline-main {{
      display: grid;
      gap: 4px;
      font-size: 14px;
    }}

    .timeline-main span {{
      color: var(--muted);
    }}

    .handoff {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(260px, 0.42fr);
      gap: 18px;
      align-items: start;
    }}

    .callout {{
      background: var(--brand-soft);
      border: 1px solid #b8d8f3;
      border-radius: 8px;
      padding: 16px;
    }}

    .callout strong {{
      display: block;
      margin-bottom: 6px;
    }}

    @media (max-width: 920px) {{
      .hero,
      .handoff {{
        grid-template-columns: 1fr;
      }}

      .metrics,
      .stage-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      .timeline-row {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 620px) {{
      main {{
        padding: 16px 12px 32px;
      }}

      .hero {{
        padding: 20px;
      }}

      h1 {{
        font-size: 27px;
      }}

      .metrics,
      .stage-grid {{
        grid-template-columns: 1fr;
      }}

      table {{
        display: block;
        overflow-x: auto;
        white-space: nowrap;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="locator">UiPath AgentHack · AgentOps Case Control Room · Demo Artifact</div>

    <section class="hero">
      <div>
        <h1>Turn AI-agent work into a governed UiPath case.</h1>
        <p class="hero-copy">
          This prototype shows how a human, an AI coding agent, UiPath robots, APIs, and an approval owner
          move through one auditable operations case instead of leaving work trapped in a chat transcript.
        </p>
      </div>
      <aside class="case-meta">
        <p><span class="meta-label">Case</span><span class="meta-value">{esc(packet["case_id"])} · {esc(packet["case_name"])}</span></p>
        <p><span class="meta-label">UiPath target</span><span class="meta-value">{esc(packet["recommended_uipath_track"])}</span></p>
        <p><span class="meta-label">Current status</span><span class="meta-value">{esc(status_label)}</span></p>
        <p><span class="meta-label">Max risk</span><span class="meta-value">{esc(packet["max_risk"])}</span></p>
      </aside>
    </section>

    <section class="section metrics">
      <div class="metric"><strong>{len(events)}</strong><span>evidence events in the UiPath case packet</span></div>
      <div class="metric"><strong>{approval_count}</strong><span>human approval gates before sensitive action</span></div>
      <div class="metric"><strong>{robot_api_count}</strong><span>robot/API evidence collection steps</span></div>
      <div class="metric"><strong>{blocked_count}</strong><span>production action blocked by policy</span></div>
    </section>

    <section class="section">
      <h2>Maestro Case Flow</h2>
      <div class="stage-grid">{stage_cards}</div>
    </section>

    <section class="section">
      <h2>Human Approval Queue</h2>
      <table>
        <thead>
          <tr>
            <th>Event</th>
            <th>Phase</th>
            <th>Risk</th>
            <th>Decision</th>
            <th>Reason</th>
          </tr>
        </thead>
        <tbody>{approvals}</tbody>
      </table>
    </section>

    <section class="section handoff">
      <div>
        <h2>Final Handoff</h2>
        <p>
          The release is rejected until the retry regression is fixed. The case remains useful after the AI conversation ends
          because every decision points back to a stable evidence event ID.
        </p>
      </div>
      <aside class="callout">
        <strong>{esc(final_event["event_id"])} · {esc(final_event["event_type"])}</strong>
        <p>{esc(final_event["summary"])}</p>
      </aside>
    </section>

    <section class="section">
      <h2>Evidence Timeline</h2>
      <div class="timeline">{timeline}</div>
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    packet = json.loads(CASE_PACKET_FILE.read_text(encoding="utf-8"))
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(build_html(packet), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "source": str(CASE_PACKET_FILE.relative_to(ROOT.parent)),
                "output": str(OUT_FILE.relative_to(ROOT)),
                "event_count": len(packet["events"]),
                "stage_count": len(packet["stages"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
