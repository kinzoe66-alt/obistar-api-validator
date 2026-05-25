#!/usr/bin/env python3

import sys
from pathlib import Path
import yaml

def load(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}

def write(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

def main():
    if len(sys.argv) != 2:
        print("usage: build_evidence_package.py <replay-yaml>")
        sys.exit(1)

    replay_file = Path(sys.argv[1])
    replay = load(replay_file).get("replay", {})

    cid = replay.get("continuity_id", "unknown")

    package = {
        "evidence_package": {
            "continuity_id": cid,
            "source_replay": str(replay_file),
            "action_id": replay.get("action_id"),
            "authorized_scope": replay.get("authorized_scope"),
            "active_symbols": replay.get("active_symbols"),
            "classification": replay.get("classification"),
            "result": replay.get("result"),
            "review_state": "queued_for_manual_review",
            "autonomous_submission": False,
            "governed_validation_only": True,
        }
    }

    out = Path("runtime/evidence/packages") / f"{cid}.yaml"
    write(out, package)
    print(out)

if __name__ == "__main__":
    main()
