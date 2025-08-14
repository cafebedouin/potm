#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 <onboard|tool|max|dev>"
    exit 1
fi

PROFILE="$1"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🔨 Building kernel profile: $PROFILE"
"$ROOT_DIR/scripts/pack_agent.sh" --profile "$PROFILE"

# Only trim onboard
if [ "$PROFILE" = "onboard" ]; then
    "$ROOT_DIR/scripts/onboard_trim_guard.sh"
fi

echo "✅ Build complete for profile: $PROFILE"
