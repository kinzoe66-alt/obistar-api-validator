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
        print("usage: observation_to_action.py <observation-yaml>")
        sys.exit(1)

    obs_file = Path(sys.argv[1])
    data = load(obs_file)
    obs = data.get("observation", {})

    action_id = f"AUTH_DIFF_{obs.get('id', 'unknown').upper()}"

    action = {
        "action": {
            "id": action_id
        },
        "intent": {
            "type": "governed_authorization_differential_validation"
        },
        "scope": {
            "authorized": bool(obs.get("authorized_scope"))
        },
        "surface": {
            "id": obs.get("surface_id")
        },
        "observations": {
            "authorization_context_change": bool(obs.get("authorization_context", {}).get("changed")),
            "workflow_state_transition": bool(obs.get("workflow_state", {}).get("changed")),
            "trust_boundary_shift": bool(obs.get("trust_boundary", {}).get("shifted")),
        },
        "evidence": {
            "source": obs.get("source"),
            "reproducible": bool(obs.get("evidence", {}).get("reproducible")),
            "destructive_mutation": bool(obs.get("evidence", {}).get("destructive_mutation")),
            "autonomous_submission": bool(obs.get("evidence", {}).get("autonomous_submission")),
        }
    }

    out = Path("runtime/actions/materialized") / f"{action_id}.yaml"
    write(out, action)
    print(out)

if __name__ == "__main__":
    main()
