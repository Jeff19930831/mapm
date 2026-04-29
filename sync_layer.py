#!/usr/bin/env python3
"""sync_layer.py — Derive agent-layer YAMLs from the General project-status YAML.

Each project's ``docs`` field determines which layer(s) it belongs to based on
the first path segment.  Cross-device projects (multiple docs paths separated
by ``+``) are placed in every matching layer.

Usage:
    python3 sync_layer.py           # Preview: show which projects go where
    python3 sync_layer.py --write   # Actually write the layer YAML files
"""

import argparse
import os
import re
import sys
from collections import OrderedDict

import yaml

# ---------------------------------------------------------------------------
# Layer configuration
# ---------------------------------------------------------------------------

GENERAL_YAML = os.path.expanduser(
    "~/Documents/Jeff1993/.project-status.yaml"
)

LAYER_PREFIXES = OrderedDict(
    [
        (
            "macclaude",
            {
                "prefix": "MacClaude/",
                "output": os.path.expanduser(
                    "~/Documents/Jeff1993/MacClaude/.project-status.yaml"
                ),
            },
        ),
        (
            "maccodex",
            {
                "prefix": "MacCodex/",
                "output": os.path.expanduser(
                    "~/Documents/Jeff1993/MacCodex/.project-status.yaml"
                ),
            },
        ),
        (
            "win_claude_work",
            {
                "prefix": "Win_Claude_Work/",
                "output": os.path.expanduser(
                    "~/Documents/Jeff1993/Win_Claude_Work/.project-status.yaml"
                ),
            },
        ),
        (
            "wincodex",
            {
                "prefix": "WinCodex/",
                "output": os.path.expanduser(
                    "~/Documents/Jeff1993/WinCodex/.project-status.yaml"
                ),
            },
        ),
    ]
)


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


def _parse_doc_prefixes(docs_value: str) -> list[str]:
    """Extract the first path segment from each backtick-quoted docs path.

    Handles backtick-wrapped paths separated by ``+``, e.g.::

        `MacClaude/a/` + `Win_Claude_Work/a/`

    Returns a list of upper-cased first segments like ``["MacClaude", "Win_Claude_Work"]``.
    """
    if not docs_value:
        return []

    # Find all backtick-delimited segments
    segments = re.findall(r"`([^`]+)`", docs_value)
    if not segments:
        # Fallback: treat the whole string as a single path
        segments = [docs_value]

    prefixes: list[str] = []
    for seg in segments:
        seg = seg.strip()
        # Strip leading ~/
        if seg.startswith("~/"):
            seg = seg[2:]
        # Extract first path component
        parts = seg.split("/")
        if parts:
            prefixes.append(parts[0])

    return prefixes


def derive_layers(general_data: dict) -> dict[str, dict]:
    """Derive per-layer project dicts from the General YAML data.

    Parameters
    ----------
    general_data :
        Dict as loaded from the General ``.project-status.yaml``.  Expected
        structure: ``{"projects": {name: {..., "docs": "..."}, ...}}``

    Returns
    -------
    dict
        Mapping of layer_name -> ``{"projects": {name: project_data, ...}}``.
        Every layer key from :data:`LAYER_PREFIXES` is always present; layers
        with no matching projects contain an empty ``projects`` dict.
    """
    # Initialise every layer with an empty projects dict
    layers: dict[str, dict] = {
        name: {"projects": {}} for name in LAYER_PREFIXES
    }

    projects = general_data.get("projects", {})
    for proj_name, proj_data in projects.items():
        docs = proj_data.get("docs", "")
        if not docs:
            continue

        prefixes = _parse_doc_prefixes(docs)
        matched = False

        for prefix in prefixes:
            for layer_name, layer_cfg in LAYER_PREFIXES.items():
                layer_prefix = layer_cfg["prefix"].rstrip("/")
                if prefix == layer_prefix:
                    layers[layer_name]["projects"][proj_name] = proj_data
                    matched = True

        # Special rule: ~/ paths → macclaude
        if not matched and "`~/" in docs or docs.startswith("~/"):
            layers["macclaude"]["projects"][proj_name] = proj_data

    return layers


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _load_general(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _write_layer(path: str, data: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        yaml.dump(data, fh, allow_unicode=True, default_flow_style=False, sort_keys=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Derive agent-layer YAMLs from General project-status YAML"
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Actually write layer YAML files (default: preview only)",
    )
    parser.add_argument(
        "--general",
        default=GENERAL_YAML,
        help="Path to the General .project-status.yaml",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.general):
        print(f"General YAML not found: {args.general}", file=sys.stderr)
        sys.exit(1)

    general_data = _load_general(args.general)
    layers = derive_layers(general_data)

    for layer_name, layer_data in layers.items():
        project_names = list(layer_data["projects"].keys())
        output_path = LAYER_PREFIXES[layer_name]["output"]
        count = len(project_names)
        print(f"\n{layer_name} ({count} projects) -> {output_path}")
        for name in project_names:
            print(f"  - {name}")

        if args.write and count:
            _write_layer(output_path, layer_data)
            print(f"  [written]")

    if not args.write:
        print("\n(dry run — use --write to actually write files)")


if __name__ == "__main__":
    main()
