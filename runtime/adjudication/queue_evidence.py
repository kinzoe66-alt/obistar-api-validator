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
        print("usage: queue_evidence.py <evidence-package-yaml>")
        sys.exit(1)

    package_file = Path(sys.argv[1])
    package = load(package_file).get("evidence_package", {})
    cid = package.get("continuity_id", "unknown")

    queued = {
        "manual_review_item": {
            "continuity_id": cid,
            "source_package": str(package_file),
            "classification": package.get("classification"),
            "active_symbols": package.get("active_symbols"),
            "review_state": "queued_for_manual_review",
            "autonomous_submission": False,
        }
    }

    out = Path("runtime/adjudication/queue") / f"{cid}.yaml"
    write(out, queued)
    print(out)

if __name__ == "__main__":
    main()
