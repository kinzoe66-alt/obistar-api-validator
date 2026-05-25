#!/usr/bin/env bash
set -e

OBSERVATION_FILE="$1"

if [ -z "$OBSERVATION_FILE" ] || [ ! -f "$OBSERVATION_FILE" ]; then
  echo "usage: ./runtime/bin/run_tunnel_cycle.sh <observation-yaml>"
  exit 1
fi

ACTION_FILE="$(python runtime/materialize/observation_to_action.py "$OBSERVATION_FILE")"
python runtime/substrate/resolve.py "$ACTION_FILE"

LATEST_REPLAY="$(find runtime/replay -type f | sort | tail -1)"
EVIDENCE_PACKAGE="$(python runtime/evidence/build_evidence_package.py "$LATEST_REPLAY")"
REVIEW_ITEM="$(python runtime/adjudication/queue_evidence.py "$EVIDENCE_PACKAGE")"

echo "=== END TO END GOVERNED TUNNEL CYCLE COMPLETE ==="
echo "OBSERVATION: $OBSERVATION_FILE"
echo "ACTION: $ACTION_FILE"
echo "REPLAY: $LATEST_REPLAY"
echo "EVIDENCE_PACKAGE: $EVIDENCE_PACKAGE"
echo "REVIEW_ITEM: $REVIEW_ITEM"
echo "TERMINAL_STATE: queued_for_manual_review"
