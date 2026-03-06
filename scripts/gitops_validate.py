#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GITOPS_DIR = REPO_ROOT / "gitops"


def main() -> int:
    if not GITOPS_DIR.exists():
        print("Missing gitops/ directory.")
        return 2

    yaml_files = sorted(p for p in GITOPS_DIR.rglob("*.yaml") if p.is_file())
    if not yaml_files:
        print("No YAML files found under gitops/.")
        return 2

    all_text = "\n".join(p.read_text(encoding="utf-8") for p in yaml_files)

    errors: list[str] = []
    if "kind: NetworkPolicy" not in all_text:
        errors.append("Missing a NetworkPolicy (basic deny-all or scoped policy expected).")
    if "kind: Deployment" not in all_text:
        errors.append("Missing a Deployment (a real workload is expected).")

    required_deployment_markers = [
        "runAsNonRoot: true",
        "allowPrivilegeEscalation: false",
        "readOnlyRootFilesystem: true",
    ]
    for marker in required_deployment_markers:
        if marker not in all_text:
            errors.append(f"Missing required hardening marker in manifests: {marker}")

    if errors:
        print("GitOps validation failed:\n" + "\n".join(f"- {e}" for e in errors))
        return 1

    print("GitOps validation OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

