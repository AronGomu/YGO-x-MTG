#!/usr/bin/env python3
"""Check hash-locked Python packages against OSV without extra dependencies."""
from __future__ import annotations
import json
import re
import urllib.request
from pathlib import Path

LOCK = Path(__file__).resolve().parents[1] / "requirements-dev.lock"
packages = re.findall(r"(?m)^([A-Za-z0-9_.-]+)==([^\s\\]+)", LOCK.read_text(encoding="utf-8"))
findings: list[str] = []
for name, version in packages:
    request = urllib.request.Request(
        "https://api.osv.dev/v1/query",
        data=json.dumps({"package": {"name": name, "ecosystem": "PyPI"}, "version": version}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    for vulnerability in result.get("vulns", []):
        findings.append(f"{name}=={version}: {vulnerability.get('id', 'unknown')}")
if findings:
    raise SystemExit("Python dependency advisories:\n" + "\n".join(findings))
print(f"python audit: {len(packages)} locked packages clean")
