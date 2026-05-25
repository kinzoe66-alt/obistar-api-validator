#!/usr/bin/env bash
set -e

ITERATIONS="${1:-5}"
OBS="runtime/observations/example-observation.yaml"
OUT="runtime/pressure-tests/pressure-run-$(date +%Y%m%d%H%M%S).yaml"

cat > "$OUT" <<EOF2
pressure_test:
  iterations: $ITERATIONS
  framing: governed_validation_only
  external_execution: false
  results:
EOF2

i=1
while [ "$i" -le "$ITERATIONS" ]; do
  START="$(date +%s%3N)"
  ./runtime/bin/run_tunnel_cycle.sh "$OBS" >/tmp/obistar-api-validator-cycle.out
  END="$(date +%s%3N)"
  MS=$((END - START))

  CID="$(grep '^continuity_id:' /tmp/obistar-api-validator-cycle.out | tail -1 | sed 's/.*continuity_id:[[:space:]]*//')"
  CLASSIFICATION="$(grep '^CLASSIFICATION:' /tmp/obistar-api-validator-cycle.out | tail -1 | sed 's/.*CLASSIFICATION:[[:space:]]*//')"

  cat >> "$OUT" <<EOF2
    - iteration: $i
      runtime_ms: $MS
      continuity_id: ${CID:-unknown}
      classification: ${CLASSIFICATION:-unknown}
      terminal_state: queued_for_manual_review
EOF2

  i=$((i + 1))
done

echo "$OUT"
