#!/usr/bin/env python3

import sys
from pathlib import Path
import yaml

WEIGHTS = {
    "money": 10,
    "sensitive_data": 9,
    "authorization": 8,
    "workflow_trust": 7,
    "evidence_quality": 6,
}

def load(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}

def main():
    if len(sys.argv) != 2:
        print("usage: consequence_score.py <action-yaml>")
        sys.exit(1)

    action = load(sys.argv[1])
    values = action.get("value_signals", {}) or {}
    evidence = action.get("evidence", {}) or {}
    observations = action.get("observations", {}) or {}

    score = 0
    wires = []

    for wire, active in values.items():
        if active:
            score += WEIGHTS.get(wire, 0)
            wires.append(wire)

    if evidence.get("reproducible"):
        score += WEIGHTS["evidence_quality"]
        wires.append("evidence_quality")

    if observations.get("authorization_context_change") and observations.get("workflow_state_transition"):
        score += 5
        wires.append("continuity_deformation")

    if observations.get("trust_boundary_shift"):
        score += 5
        wires.append("trust_boundary_deformation")

    classification = "LOW_VALUE_NOISE"
    if score >= 25:
        classification = "HIGH_VALUE_REVIEW"
    elif score >= 15:
        classification = "MEDIUM_VALUE_REVIEW"

    print(yaml.safe_dump({
        "consequence_score": {
            "score": score,
            "classification": classification,
            "active_value_wires": wires or ["none"]
        }
    }, sort_keys=False))

if __name__ == "__main__":
    main()
