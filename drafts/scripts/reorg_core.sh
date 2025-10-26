#!/usr/bin/env bash
# WSL-friendly, verbose, no early-exit. Run from repo root.
set -u  # (no -e so we don't bail on a single failure)
DRY_RUN="${DRY_RUN:-1}"

CORE_ROOT="core"; EXP_ROOT="experimental"; DEP_ROOT="deprecated"
mkdir -p "$EXP_ROOT" "$DEP_ROOT"

KEEPERS="$(cat <<'KEOF'
core/README.md
core/index.md
core/coordination/kernel_mode_user.md
core/coordination/microkernel_self_diagnostic_protocol.md
core/diagnostics/blind_kernel_pass_diagnostic.md
core/diagnostics/contextual_drift_sensor.md
core/diagnostics/epistemic_integrity_checklist.md
core/diagnostics/memory_drift_diagnostic.md
core/diagnostics/relational_dignity_filter.md
core/docs/README.md
core/docs/index.md
core/docs/onboarding/00_MANIFEST.md
core/docs/onboarding/00_MANIFEST_BOOTSTRAP_PROMPT.md
core/docs/onboarding/persistence_prompt.md
core/docs/onboarding/welcome_gpt5.md
core/docs/living_maxims.md
core/docs/potm_bootpack_quick_start.md
core/frameworks/potm_framework.md
core/guardian/discernment_integrity_protocol.md
core/guidelines/potm_repo_upgrade_checklist.md
core/practices/protocols/ai_integrity_protocol.md
core/practices/protocols/elements_of_refusal_protocol.md
core/practices/protocols/mirror_protocol.md
KEOF
)"

DEPRECATED_GLOBS=(
  "core/diagnostics/results/*"
  "core/logs/*"
  "core/docs/peer_reviews/*"
)

is_keeper()    { grep -Fxq -- "$1" <<<"$KEEPERS"; }
is_deprecated(){ local f="$1"; for g in "${DEPRECATED_GLOBS[@]}"; do [[ "$f" == $g ]] && return 0; done; return 1; }

mv_git() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")" || { echo "MKDIR FAIL: $(dirname "$dest")"; return 1; }
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[DRY] git mv -k \"$src\" \"$dest\""
  else
    if ! git mv -k "$src" "$dest"; then
      echo "[WARN] git mv failed, falling back to mv: $src -> $dest"
      mv -f "$src" "$dest" || { echo "[ERR] mv failed: $src -> $dest"; return 1; }
    fi
  fi
}

echo "=== Reorg '$CORE_ROOT' ==="
echo "Mode: $([[ "$DRY_RUN" == "1" ]] && echo DRY-RUN || echo EXECUTE)"
echo

# Process via NUL-delimited read (avoids mapfile quirks)
keep=0 dep=0 exp=0 n=0
git ls-files -z -- "$CORE_ROOT" | while IFS= read -r -d '' f; do
  n=$((n+1))
  [[ -z "${f:-}" ]] && continue
  echo ">> [$n] $f"

  if is_keeper "$f"; then
    echo "KEEP      : $f"; keep=$((keep+1)); continue
  fi

  rel="${f#${CORE_ROOT}/}"
  if is_deprecated "$f"; then
    echo "DEPRECATE : $f"
    mv_git "$f" "$DEP_ROOT/$rel" || echo "[ERR] move->deprecated failed for $f"
    dep=$((dep+1))
  else
    echo "EXPERIMENT: $f"
    mv_git "$f" "$EXP_ROOT/$rel" || echo "[ERR] move->experimental failed for $f"
    exp=$((exp+1))
  fi
done

echo
echo "=== Done (see counts above in stream). After run: git status ==="
