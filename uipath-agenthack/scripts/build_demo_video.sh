#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
FONT="/System/Library/Fonts/Supplemental/Arial.ttf"
OUT="$ROOT/media/agentops-case-control-room-demo.mp4"
LEGACY_OUT="$ROOT/media/agentops-case-control-room-demo-draft.mp4"
TMP_DIR="$ROOT/media/.demo_video_tmp"
EDGE_TTS_PYTHON="${EDGE_TTS_PYTHON:-python3.11}"
EDGE_TTS_VOICE="${EDGE_TTS_VOICE:-en-US-AvaNeural}"
EDGE_TTS_RATE="${EDGE_TTS_RATE:--8%}"

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

make_slide() {
  local src="$1"
  local title="$2"
  local subtitle="$3"
  local kicker="$4"
  local out="$5"

  magick "$src" \
    -resize 1920x \
    -crop 1920x1080+0+0 +repage \
    -fill "#031A22D9" -draw "rectangle 0,0 1920,156" \
    -fill "#000000CC" -draw "rectangle 0,770 1920,1080" \
    -font "$FONT" -fill "#9DECF0" -pointsize 30 -annotate +72+62 "$kicker" \
    -font "$FONT" -fill white -pointsize 58 -annotate +72+124 "$title" \
    -font "$FONT" -fill white -pointsize 44 -annotate +72+870 "$subtitle" \
    "$out"
}

make_slide \
  "$ROOT/media/uipath-case-room-full.png" \
  "AI agents need governance" \
  "Speed is not enough. The work must be safe, reviewable, and resumable." \
  "1 / 7  Why this exists" \
  "$TMP_DIR/slide-0.png"

make_slide \
  "$ROOT/media/action-center-demo-full.png" \
  "One shared case" \
  "Human, AI agent, robot, APIs, and approval owners are recorded together." \
  "2 / 7  UiPath-style control room" \
  "$TMP_DIR/slide-1.png"

make_slide \
  "$REPO_ROOT/shared-agentops-engine/media/shared-dashboard-full.png" \
  "Evidence first" \
  "The AI plans. The robot gathers tickets and pull request evidence." \
  "3 / 7  Robot evidence collection" \
  "$TMP_DIR/slide-2.png"

make_slide \
  "$ROOT/media/uipath-case-room-full.png" \
  "Risk is blocked" \
  "A failing regression test stops the production deployment before execution." \
  "4 / 7  Deterministic policy gateway" \
  "$TMP_DIR/slide-3.png"

make_slide \
  "$ROOT/media/action-center-demo-full.png" \
  "Humans decide" \
  "Action Center-style tasks route the decision to the right owners." \
  "5 / 7  Human approval path" \
  "$TMP_DIR/slide-4.png"

make_slide \
  "$REPO_ROOT/shared-agentops-engine/media/shared-dashboard-full.png" \
  "Handoff is inspectable" \
  "Event IDs, risks, transaction logs, decisions, and state are preserved." \
  "6 / 7  Resumable work" \
  "$TMP_DIR/slide-5.png"

make_slide \
  "$ROOT/media/uipath-case-room-full.png" \
  "Ready for UiPath" \
  "A verified local prototype plus a UiPath-ready case package." \
  "7 / 7  Honest submission boundary" \
  "$TMP_DIR/slide-6.png"

cat > "$TMP_DIR/narration.txt" <<'TEXT'
AI agents can move fast. But in business, speed is not enough. We need governance.

AgentOps Case Control Room turns the work into one UiPath-style case. It records the human, the AI agent, the robot, APIs, and approval owners.

In this release exception, the AI creates a read-only plan. A UiPath-style robot gathers ticket and pull request evidence.

The system finds a failing regression test. The production deployment is blocked before it can run.

The human does not approve blindly. Action Center-style tasks ask for more evidence and route the final decision to the service owner.

The service owner rejects the release until the regression is fixed. The handoff keeps event IDs, risk, decisions, transaction logs, and final state.

This is the product idea. AI-agent work should become a governed case that humans and future AI agents can safely resume.
TEXT

"$EDGE_TTS_PYTHON" -m edge_tts \
  --voice "$EDGE_TTS_VOICE" \
  --rate="$EDGE_TTS_RATE" \
  --file "$TMP_DIR/narration.txt" \
  --write-media "$TMP_DIR/narration.mp3"

ffmpeg -y \
  -loop 1 -t 12 -i "$TMP_DIR/slide-0.png" \
  -loop 1 -t 12 -i "$TMP_DIR/slide-1.png" \
  -loop 1 -t 12 -i "$TMP_DIR/slide-2.png" \
  -loop 1 -t 12 -i "$TMP_DIR/slide-3.png" \
  -loop 1 -t 12 -i "$TMP_DIR/slide-4.png" \
  -loop 1 -t 12 -i "$TMP_DIR/slide-5.png" \
  -loop 1 -t 12 -i "$TMP_DIR/slide-6.png" \
  -i "$TMP_DIR/narration.mp3" \
  -filter_complex "[0:v][1:v][2:v][3:v][4:v][5:v][6:v]concat=n=7:v=1:a=0,format=yuv420p[v];[7:a]loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" -r 30 -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"

cp "$OUT" "$LEGACY_OUT"

rm -rf "$TMP_DIR"
echo "$OUT"
