#!/usr/bin/env bash
set -euo pipefail

PROFILE=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --profile) PROFILE="$2"; shift 2 ;;
        *) shift ;;
    esac
done

if [ -z "$PROFILE" ]; then
    echo "ERR: No profile specified" >&2
    exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
MANIFEST="$ROOT_DIR/build_manifest.yaml"
OUT_FILE="$DIST_DIR/kernel_${PROFILE}.md"

mkdir -p "$DIST_DIR"

# Read include and exclude lists in declared order
INCLUDES=$(yq -r ".profiles.$PROFILE.include[]" "$MANIFEST")
EXCLUDES=$(yq -r ".profiles.$PROFILE.exclude[]" "$MANIFEST" 2>/dev/null || true)

# Build file list preserving order
FILES=()
for file in $INCLUDES; do
    skip=false
    for ex in $EXCLUDES; do
        [[ "$file" == "$ex" ]] && skip=true && break
    done
    if ! $skip; then
        FILES+=("$ROOT_DIR/$file")
    fi
done

# Concatenate in the same order as manifest
> "$OUT_FILE"
for f in "${FILES[@]}"; do
    if [[ -f "$f" ]]; then
        printf "\n\n---\n# %s\n\n" "$(basename "$f")" >> "$OUT_FILE"
        cat "$f" >> "$OUT_FILE"
    else
        echo "⚠ Missing file: $f" >&2
    fi
done

echo "✓ Built $PROFILE → $OUT_FILE"
