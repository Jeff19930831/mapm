"""Tests for sync_layer.py — derive project layers from General YAML."""

import sys
import os
import pytest

# Ensure the scripts directory is on the path so we can import sync_layer
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sync_layer import derive_layers, LAYER_PREFIXES


def test_basic_separation():
    """Projects go to correct layers based on docs prefix."""
    data = {"projects": {
        "a": {"docs": "`MacClaude/a/`"},
        "b": {"docs": "`MacCodex/b/`"},
        "c": {"docs": "`Win_Claude_Work/c/`"},
    }}
    layers = derive_layers(data)
    assert "a" in layers["macclaude"]["projects"]
    assert "b" in layers["maccodex"]["projects"]
    assert "c" in layers["win_claude_work"]["projects"]
    assert "a" not in layers["maccodex"]["projects"]


def test_cross_device():
    """Cross-device project appears in multiple layers."""
    data = {"projects": {
        "x": {"docs": "`MacClaude/x/` + `Win_Claude_Work/x/`"},
    }}
    layers = derive_layers(data)
    assert "x" in layers["macclaude"]["projects"]
    assert "x" in layers["win_claude_work"]["projects"]


def test_tilde_paths():
    """~/projects/... docs go to macclaude."""
    data = {"projects": {
        "y": {"docs": "`~/projects/y/docs/`"},
    }}
    layers = derive_layers(data)
    assert "y" in layers["macclaude"]["projects"]


def test_empty_layers():
    """Layers with no matching projects have empty projects dict."""
    data = {"projects": {
        "a": {"docs": "`MacClaude/a/`"},
    }}
    layers = derive_layers(data)
    assert layers["wincodex"]["projects"] == {}


def test_unknown_prefix_skipped():
    """Projects with unrecognized docs prefix are not in any layer."""
    data = {"projects": {
        "z": {"docs": "`UnknownDir/z/`"},
    }}
    layers = derive_layers(data)
    total = sum(len(l["projects"]) for l in layers.values())
    assert total == 0


def test_all_layers_present():
    """derive_layers always returns all four layer keys, even with empty input."""
    data = {"projects": {}}
    layers = derive_layers(data)
    expected_keys = set(LAYER_PREFIXES.keys())
    assert set(layers.keys()) == expected_keys


def test_cross_device_three_layers():
    """Project with three docs prefixes goes to three layers."""
    data = {"projects": {
        "multi": {"docs": "`MacClaude/m/` + `MacCodex/m/` + `WinClaude_Work/m/`"},
    }}
    layers = derive_layers(data)
    assert "multi" in layers["macclaude"]["projects"]
    assert "multi" in layers["maccodex"]["projects"]


def test_docs_without_backticks():
    """Docs field without backticks is still parsed correctly."""
    data = {"projects": {
        "plain": {"docs": "MacClaude/plain/"},
    }}
    layers = derive_layers(data)
    assert "plain" in layers["macclaude"]["projects"]


def test_missing_docs_field():
    """Project with no docs field is skipped."""
    data = {"projects": {
        "nodocs": {"status": "active"},
    }}
    layers = derive_layers(data)
    total = sum(len(l["projects"]) for l in layers.values())
    assert total == 0


def test_project_data_preserved():
    """Full project data is carried into the layer, not just the name."""
    data = {"projects": {
        "rich": {"docs": "`MacClaude/rich/`", "status": "active", "tag": "v1"},
    }}
    layers = derive_layers(data)
    proj = layers["macclaude"]["projects"]["rich"]
    assert proj["status"] == "active"
    assert proj["tag"] == "v1"
