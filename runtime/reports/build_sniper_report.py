#!/usr/bin/env python3

import sys
from pathlib import Path
import yaml

def load(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}

def write(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")

def main():
    if len(sys.argv) != 3:
        print("usage: build_sniper_report.py <replay-yaml> <score-yaml>")
        sys.exit(1)

    replay_file = Path(sys.argv[1])
    score_file = Path(sys.argv[2])

    replay = load(replay_file).get("replay", {})
    score = load(score_file).get("consequence_score", {})

    cid = replay.get("continuity_id", "unknown")
    out = Path("runtime/reports/sniper") / f"{cid}.md"

    report = f"""# Governed Sniper Tunnel Report

## Continuity ID

{cid}

## Classification

{score.get("classification")}

## Consequence Score

{score.get("score")}

## Active Value Wires

{", ".join(score.get("active_value_wires", []))}

## Active Symbols

{", ".join(replay.get("active_symbols", []))}

## Operational Narrative

A governed authorization-differential observation produced replayable continuity evidence.

The tunnel observed authorization/workflow continuity signals and compressed them into a manual-review evidence path.

## Review State

queued_for_manual_review

## Safety Frame

- governed_validation_only: true
- autonomous_submission: false
- destructive_mutation: false
"""
    write(out, report)
    print(out)

if __name__ == "__main__":
    main()
