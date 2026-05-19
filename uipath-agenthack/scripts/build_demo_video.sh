#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
FONT="/System/Library/Fonts/Supplemental/Arial.ttf"
OUT="$ROOT/media/agentops-case-control-room-demo.mp4"
LEGACY_OUT="$ROOT/media/agentops-case-control-room-demo-draft.mp4"
TMP_DIR="$ROOT/media/.demo_video_tmp"

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

make_slide() {
  local src="$1"
  local title="$2"
  local subtitle="$3"
  local out="$4"

  magick "$src" \
    -resize 1920x \
    -crop 1920x1080+0+0 +repage \
    -fill "#000000B3" -draw "rectangle 0,840 1920,1080" \
    -font "$FONT" -fill white -pointsize 58 -annotate +72+920 "$title" \
    -font "$FONT" -fill white -pointsize 34 -annotate +72+992 "$subtitle" \
    "$out"
}

make_slide \
  "$ROOT/media/uipath-case-room-full.png" \
  "AI work needs a case, not a transcript" \
  "AgentOps Case Control Room turns human-AI operations into governed work." \
  "$TMP_DIR/slide-0.png"

make_slide \
  "$ROOT/media/action-center-demo-full.png" \
  "Humans stay in control" \
  "Risky production actions become Action Center-style review tasks." \
  "$TMP_DIR/slide-1.png"

make_slide \
  "$REPO_ROOT/shared-agentops-engine/media/shared-dashboard-full.png" \
  "Evidence becomes operational memory" \
  "Every action, approval, cost signal, and risk signal is preserved." \
  "$TMP_DIR/slide-2.png"

make_slide \
  "$ROOT/media/uipath-case-room-full.png" \
  "The case catches risk before execution" \
  "A failed regression and production deploy attempt route the case to humans." \
  "$TMP_DIR/slide-3.png"

make_slide \
  "$ROOT/media/action-center-demo-full.png" \
  "The final decision is accountable" \
  "The service owner rejects the release until the regression is fixed." \
  "$TMP_DIR/slide-4.png"

make_slide \
  "$ROOT/media/uipath-case-room-full.png" \
  "Another human or AI can resume later" \
  "State machine, transaction logs, decision logs, and handoff keep the work inspectable." \
  "$TMP_DIR/slide-5.png"

cat > "$TMP_DIR/narration.txt" <<'TEXT'
AI agents are becoming operational workers. The problem is no longer only speed. The problem is governance.
AgentOps Case Control Room turns human, AI agent, robot, API, and approval-owner actions into one UiPath-style case.
In this demo, a release bot proposes a production change. The AI investigates, a UiPath-style robot gathers evidence, a failing regression test is found, and the production deployment is blocked before execution.
The human asks for more evidence. The service owner rejects the release until the regression is fixed.
At the end, another human or another AI can resume from facts: event IDs, risk, decisions, transaction logs, and a handoff. This is how AI-agent work becomes enterprise-ready.
TEXT

say -o "$TMP_DIR/narration.aiff" -f "$TMP_DIR/narration.txt"

ffmpeg -y \
  -loop 1 -t 9 -i "$TMP_DIR/slide-0.png" \
  -loop 1 -t 9 -i "$TMP_DIR/slide-1.png" \
  -loop 1 -t 9 -i "$TMP_DIR/slide-2.png" \
  -loop 1 -t 9 -i "$TMP_DIR/slide-3.png" \
  -loop 1 -t 9 -i "$TMP_DIR/slide-4.png" \
  -loop 1 -t 9 -i "$TMP_DIR/slide-5.png" \
  -i "$TMP_DIR/narration.aiff" \
  -filter_complex "[0:v][1:v][2:v][3:v][4:v][5:v]concat=n=6:v=1:a=0,format=yuv420p[v]" \
  -map "[v]" -map 6:a -r 30 -c:a aac -b:a 160k -shortest -movflags +faststart "$OUT"

cp "$OUT" "$LEGACY_OUT"

rm -rf "$TMP_DIR"
echo "$OUT"
