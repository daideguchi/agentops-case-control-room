#!/usr/bin/env python3
"""Verify UiPath lane local artifacts."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

JSON_FILES = [
    "architecture/maestro-process-spec.json",
    "runtime/maestro-simulated-case-run.json",
    "action-center/action-center-tasks.json",
    "runtime/robot-work-items.json",
    "uipath-package/orchestrator-queues.json",
    "uipath-package/case-data-model.json",
    "uipath-package/package-manifest.json",
    "uipath-package/action-center-form-schema.json",
]

HTML_CHECKS = {
    "prototype/maestro-case-room.html": ["Maestro Case Flow", "Human Approval Queue"],
    "action-center/action-center-demo.html": ["Every risky agent action becomes a human approval task", "Production deployment blocked by policy"],
}

SCREENSHOTS = [
    "media/uipath-case-room-full.png",
    "media/action-center-demo-full.png",
]

XML_FILES = [
    ("uipath-package/maestro-process.bpmn", ["<bpmn:definitions", "<bpmn:process", "Process_AgentOpsCaseControlRoom"]),
]


def main() -> None:
    errors: list[str] = []

    for rel_path in JSON_FILES:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing json: {rel_path}")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid json {rel_path}: {exc}")

    parser = HTMLParser()
    for rel_path, needles in HTML_CHECKS.items():
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing html: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        parser.feed(text)
        for needle in needles:
            if needle not in text:
                errors.append(f"missing text in {rel_path}: {needle}")

    for rel_path, needles in XML_FILES:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing xml: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"missing xml marker in {rel_path}: {needle}")

    for rel_path in SCREENSHOTS:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing screenshot: {rel_path}")
        elif path.stat().st_size < 10_000:
            errors.append(f"screenshot too small: {rel_path}")

    if errors:
        print("uipath_verify_failed")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("uipath_verify_ok")
    print(f"json={len(JSON_FILES)}")
    print(f"html={len(HTML_CHECKS)}")
    print(f"xml={len(XML_FILES)}")
    print(f"screenshots={len(SCREENSHOTS)}")


if __name__ == "__main__":
    main()
