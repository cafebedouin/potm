#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist"
SRC="$ROOT_DIR/portable/potm_practitioner_kernel_portable.md"
OUT="$OUT_DIR/potm_portable_v1_5.md"

mkdir -p "$OUT_DIR"

if [[ ! -f "$SRC" ]]; then
  echo "ERR: missing $SRC" >&2
  exit 1
fi

cp "$SRC" "$OUT"
echo "✓ Portable bundle → $OUT"
