#!/usr/bin/env python3
"""
Validiert die gespeicherten Demo-Queries gegen Stage 2 und Stage 3.

Voraussetzung:
- Stage 2 läuft auf http://localhost:3000
- Stage 3 läuft auf http://localhost:8000/graphql
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


QUERY_TARGETS = {
    "01_alle_kontakte.graphql": ("stage2", "http://localhost:3000"),
    "02_tatooine_suche.graphql": ("stage2", "http://localhost:3000"),
    "03_han_rohe_ids.graphql": ("stage2", "http://localhost:3000"),
    "04_han_traversierung.graphql": ("stage3", "http://localhost:8000/graphql"),
    "05_rebel_alliance_gruppe.graphql": ("stage2", "http://localhost:3000"),
}


def load_query(file_path: Path) -> str:
    lines = file_path.read_text(encoding="utf-8").splitlines()
    return "\n".join(line for line in lines if not line.lstrip().startswith("#")).strip()


def execute_query(url: str, query: str) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    failures = 0

    for file_name, (stage, url) in QUERY_TARGETS.items():
        file_path = Path("queries") / file_name
        query = load_query(file_path)

        try:
            response = execute_query(url, query)
        except urllib.error.URLError as error:
            failures += 1
            print(f"FAIL {file_name} [{stage}] Endpoint nicht erreichbar: {error}")
            continue
        except Exception as error:
            failures += 1
            print(f"FAIL {file_name} [{stage}] {type(error).__name__}: {error}")
            continue

        if response.get("errors"):
            failures += 1
            print(f"FAIL {file_name} [{stage}] {response['errors'][0]['message']}")
            continue

        print(f"PASS {file_name} [{stage}]")

    if failures:
        print(f"\n{failures} Query-Datei(en) fehlgeschlagen.")
        return 1

    print("\nAlle Query-Dateien erfolgreich validiert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())