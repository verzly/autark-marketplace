#!/usr/bin/env python3
"""Update the marketplace's cached latest GitHub release tags."""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
VERSIONS_PATH = ROOT / "versions.json"


def resolve_version(source: str, token: str | None) -> str:
    """Return the latest version for a version_source value.

    Supported: ``github:owner/repo`` (latest release tag) and
    ``pypi:package`` (latest published version).
    """
    kind, _, target = source.partition(":")
    if not target:
        raise ValueError(f"invalid version_source {source!r}")
    if kind == "pypi":
        request = Request(
            f"https://pypi.org/pypi/{target}/json",
            headers={"Accept": "application/json"},
        )
        with urlopen(request, timeout=30) as response:
            version = json.load(response).get("info", {}).get("version")
        if not isinstance(version, str) or not version:
            raise ValueError("PyPI response has no version")
        return version
    if kind == "github":
        headers = {"Accept": "application/vnd.github+json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = Request(
            f"https://api.github.com/repos/{target}/releases/latest",
            headers=headers,
        )
        with urlopen(request, timeout=30) as response:
            tag = json.load(response).get("tag_name")
        if not isinstance(tag, str) or not tag:
            raise ValueError("release has no tag_name")
        return tag
    raise ValueError(f"unsupported version_source {source!r}")


def main():
    previous = {}
    if VERSIONS_PATH.exists():
        try:
            previous = json.loads(VERSIONS_PATH.read_text(encoding="utf-8")).get(
                "apps", {}
            )
        except (OSError, json.JSONDecodeError, AttributeError):
            print("Cannot read existing versions.json", file=sys.stderr)
            return 1

    token = os.environ.get("GITHUB_TOKEN")
    updated = dict(previous)
    successes = failures = 0
    for manifest_path in sorted((ROOT / "apps").glob("*/app.json")):
        app_id = manifest_path.parent.name
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            upstream = manifest.get("upstream", "")
            source = manifest.get("version_source", "")
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            print(f"{app_id}: cannot read manifest: {exc}", file=sys.stderr)
            failures += 1
            continue
        if not isinstance(source, str) or not source:
            if isinstance(upstream, str) and re.fullmatch(
                r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", upstream
            ):
                source = f"github:{upstream}"
            else:
                continue
        try:
            updated[app_id] = resolve_version(source, token)
            successes += 1
        except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"{app_id}: release lookup failed: {exc}", file=sys.stderr)
            failures += 1

    sorted_apps = dict(sorted(updated.items()))
    if sorted_apps == previous:
        print(f"versions unchanged; retained/failed {failures} app(s).")
        return 0

    payload = {
        "schema": 1,
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
            "+00:00", "Z"
        ),
        "apps": sorted_apps,
    }
    try:
        VERSIONS_PATH.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        print(f"Cannot write versions.json: {exc}", file=sys.stderr)
        return 1

    print(f"Updated {successes} app(s); retained/failed {failures} app(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
