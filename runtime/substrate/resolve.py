#!/usr/bin/env python3

import hashlib
import sys
import time
from pathlib import Path
import yaml

ROOT = Path(".")
STATE = ROOT / "runtime/state/current-state.yaml"

def load_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}

def cid(action_id):
    ts = time.strftime("%Y%m%d%H%M%S")
    h = hashlib.sha256(f"{ts}-{action_id}".encode()).hexdigest()[:12]
    return f"cid-{ts}-{h}-{action_id}"

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main():
    if len(sys.argv) != 2:
        print("usage: resolve.py <action-yaml>")
        sys.exit(1)

    action_file = Path(sys.argv[1])
    action = load_yaml(action_file)

    action_id = action.get("action", {}).get("id", "unknown")
    intent = action.get("intent", {}).get("type", "governed_validation")
    authorized = action.get("scope", {}).get("authorized", False)
    observations = action.get("observations", {}) or {}

    active_symbols = []

    if observations.get("authorization_context_change"):
        active_symbols.append("AUTHORIZATION_CONTEXT_CHANGE")

    if observations.get("workflow_state_transition"):
        active_symbols.append("WORKFLOW_STATE_TRANSITION")

    if observations.get("trust_boundary_shift"):
        active_symbols.append("TRUST_BOUNDARY_SHIFT")

    result = "LAWFUL_FOR_MANUAL_REVIEW"
    classification = "REVIEW_REQUIRED"
    reason = "validated inside governed tunnel"

    if not authorized:
        result = "BLOCKED"
        classification = "AUTHORITY_SCOPE_FAILURE"
        reason = "authorized scope not declared"

    continuity_id = cid(action_id)

    replay_file = ROOT / "runtime/replay" / f"{continuity_id}.yaml"
    write(replay_file, yaml.safe_dump({
        "replay": {
            "continuity_id": continuity_id,
            "action_file": str(action_file),
            "action_id": action_id,
            "intent": intent,
            "authorized_scope": authorized,
            "active_symbols": active_symbols or ["none"],
            "result": result,
            "classification": classification,
            "reason": reason,
            "terminal_state": "queued_for_manual_review",
        }
    }, sort_keys=False))

    write(STATE, yaml.safe_dump({
        "current_state": {
            "continuity_id": continuity_id,
            "tunnel": "governed_authorization_differential_continuity",
            "classification": classification,
            "active_symbols": active_symbols or ["none"],
            "terminal_state": "queued_for_manual_review",
        }
    }, sort_keys=False))

    print("=== OBISTAR GOVERNED AUTHORIZATION DIFFERENTIAL RESOLUTION ===")
    print(f"continuity_id: {continuity_id}")
    print(f"action_id: {action_id}")
    print(f"intent: {intent}")
    print(f"authorized_scope: {str(authorized).lower()}")
    print(f"active_symbols: {','.join(active_symbols) if active_symbols else 'none'}")
    print(f"RESULT: {result}")
    print(f"CLASSIFICATION: {classification}")
    print(f"REPLAY: {replay_file}")
    print("TERMINAL_STATE: queued_for_manual_review")

    if result == "BLOCKED":
        sys.exit(2)

if __name__ == "__main__":
    main()
