#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 ../shared-agentops-engine/scripts/generate_portfolio_artifacts.py
python3 ../shared-agentops-engine/scripts/verify_artifacts.py
python3 scripts/build_case_room.py
python3 scripts/simulate_maestro_case.py
python3 scripts/export_uipath_blueprint.py
python3 scripts/build_action_center_demo.py
python3 scripts/verify_uipath_package.py
