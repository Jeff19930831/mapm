"""Tests for verify-projects.py data health check script."""

import os
import sys
import json
from datetime import datetime, timedelta

import pytest
import yaml

# Add scripts dir to path so we can import the module
sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))

from verify_projects import (
    check_code_path_exists,
    check_cross_yaml_consistency,
    check_last_update_stale,
    check_docs_dir_exists,
    check_layer_assignment,
    load_yaml,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_yaml(path, data):
    """Write a dict as YAML to path."""
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


def _make_general(projects):
    """Build a general YAML structure."""
    return {"projects": projects}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_root(tmp_path):
    """Create a temporary ROOT_DIR with the expected directory layout."""
    root = tmp_path / "Jeff1993"
    root.mkdir()
    # Create layer dirs
    (root / "MacClaude").mkdir()
    (root / "MacCodex").mkdir()
    (root / "Win_Claude_Work").mkdir()
    (root / "WinCodex").mkdir()
    return root


@pytest.fixture
def real_dirs(tmp_path):
    """Create some real directories that code_path / docs will reference."""
    existing = tmp_path / "existing_dir"
    existing.mkdir()
    return {"existing": str(existing), "missing": str(tmp_path / "no_such_dir")}


# ---------------------------------------------------------------------------
# test_check_code_path_exists
# ---------------------------------------------------------------------------

class TestCheckCodePathExists:
    def test_existing_path_is_ok(self, tmp_path, real_dirs):
        projects = {
            "proj-a": {"code_path": real_dirs["existing"]},
        }
        results = check_code_path_exists(projects)
        assert len(results) == 0  # no issues

    def test_missing_path_is_warning(self, tmp_path, real_dirs):
        projects = {
            "proj-b": {"code_path": real_dirs["missing"]},
        }
        results = check_code_path_exists(projects)
        assert len(results) == 1
        assert results[0]["project"] == "proj-b"
        assert results[0]["level"] == "warning"
        assert "missing" in results[0]["message"].lower() or "not found" in results[0]["message"].lower()

    def test_windows_path_is_skipped(self, tmp_path, real_dirs):
        projects = {
            "proj-c": {"code_path": "D:\\ClaudeCode\\some-project\\"},
        }
        results = check_code_path_exists(projects)
        assert len(results) == 0  # skipped, no issues

    def test_dash_code_path_is_skipped(self, tmp_path, real_dirs):
        projects = {
            "proj-d": {"code_path": "\u2014"},  # em-dash
        }
        results = check_code_path_exists(projects)
        assert len(results) == 0

    def test_tilde_expansion(self, tmp_path, real_dirs):
        """Paths with ~ should expand and be checked."""
        projects = {
            "proj-e": {"code_path": "~/nonexistent_test_path_xyz/"},
        }
        results = check_code_path_exists(projects)
        assert len(results) == 1
        assert results[0]["level"] == "warning"

    def test_c_drive_path_is_skipped(self, tmp_path, real_dirs):
        projects = {
            "proj-f": {"code_path": "C:\\Users\\Administrator\\Documents\\proj\\"},
        }
        results = check_code_path_exists(projects)
        assert len(results) == 0

    def test_mixed_paths(self, tmp_path, real_dirs):
        projects = {
            "proj-ok": {"code_path": real_dirs["existing"]},
            "proj-missing": {"code_path": real_dirs["missing"]},
            "proj-win": {"code_path": "D:\\something\\"},
            "proj-dash": {"code_path": "\u2014"},
        }
        results = check_code_path_exists(projects)
        assert len(results) == 1
        assert results[0]["project"] == "proj-missing"


# ---------------------------------------------------------------------------
# test_check_cross_yaml_consistency
# ---------------------------------------------------------------------------

class TestCheckCrossYamlConsistency:
    def test_matching_status_no_issues(self, tmp_root):
        general = _make_general({
            "proj-a": {"status": "\u8fd0\u884c\u4e2d"},  # 运行中
        })
        layer = _make_general({
            "proj-a": {"status": "\u8fd0\u884c\u4e2d"},
        })
        general_path = tmp_root / ".project-status.yaml"
        _write_yaml(str(general_path), general)

        layer_yamls = {"test_layer": str(tmp_root / "layer.yaml")}
        _write_yaml(layer_yamls["test_layer"], layer)

        results = check_cross_yaml_consistency(str(general_path), layer_yamls)
        assert len(results) == 0

    def test_status_mismatch_is_warning(self, tmp_root):
        general = _make_general({
            "proj-a": {"status": "\u8fd0\u884c\u4e2d"},
        })
        layer = _make_general({
            "proj-a": {"status": "\u5df2\u5b8c\u6210"},  # 已完成
        })
        general_path = tmp_root / ".project-status.yaml"
        _write_yaml(str(general_path), general)

        layer_yamls = {"test_layer": str(tmp_root / "layer.yaml")}
        _write_yaml(layer_yamls["test_layer"], layer)

        results = check_cross_yaml_consistency(str(general_path), layer_yamls)
        assert len(results) == 1
        assert results[0]["level"] == "warning"
        assert "status" in results[0]["message"].lower() or "mismatch" in results[0]["message"].lower()

    def test_project_not_in_general_is_error(self, tmp_root):
        general = _make_general({})
        layer = _make_general({
            "orphan-proj": {"status": "\u8fd0\u884c\u4e2d"},
        })
        general_path = tmp_root / ".project-status.yaml"
        _write_yaml(str(general_path), general)

        layer_yamls = {"test_layer": str(tmp_root / "layer.yaml")}
        _write_yaml(layer_yamls["test_layer"], layer)

        results = check_cross_yaml_consistency(str(general_path), layer_yamls)
        assert len(results) == 1
        assert results[0]["level"] == "error"
        assert "not in general" in results[0]["message"].lower() or "not found" in results[0]["message"].lower()

    def test_multiple_layers(self, tmp_root):
        general = _make_general({
            "proj-a": {"status": "\u8fd0\u884c\u4e2d"},
            "proj-b": {"status": "\u5df2\u5b8c\u6210"},
        })
        layer1 = _make_general({
            "proj-a": {"status": "\u8fd0\u884c\u4e2d"},
        })
        layer2 = _make_general({
            "proj-b": {"status": "\u8fd0\u884c\u4e2d"},  # mismatch
            "proj-c": {"status": "\u8fd0\u884c\u4e2d"},  # not in general
        })
        general_path = tmp_root / ".project-status.yaml"
        _write_yaml(str(general_path), general)

        layer_yamls = {
            "layer1": str(tmp_root / "layer1.yaml"),
            "layer2": str(tmp_root / "layer2.yaml"),
        }
        _write_yaml(layer_yamls["layer1"], layer1)
        _write_yaml(layer_yamls["layer2"], layer2)

        results = check_cross_yaml_consistency(str(general_path), layer_yamls)
        assert len(results) == 2  # one mismatch warning + one not-in-general error
        levels = {r["level"] for r in results}
        assert "warning" in levels
        assert "error" in levels


# ---------------------------------------------------------------------------
# test_check_last_update_stale
# ---------------------------------------------------------------------------

class TestCheckLastUpdateStale:
    def test_stale_active_project_is_info(self):
        old_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        projects = {
            "proj-a": {"status": "\u8fd0\u884c\u4e2d", "last_update": old_date},
        }
        results = check_last_update_stale(projects, stale_days=14)
        assert len(results) == 1
        assert results[0]["level"] == "info"
        assert "days old" in results[0]["message"].lower() or "stale" in results[0]["message"].lower()

    def test_recent_active_project_is_ok(self):
        recent_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        projects = {
            "proj-a": {"status": "\u8fd0\u884c\u4e2d", "last_update": recent_date},
        }
        results = check_last_update_stale(projects, stale_days=14)
        assert len(results) == 0

    def test_stale_completed_project_is_ok(self):
        old_date = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")
        projects = {
            "proj-a": {"status": "\u5df2\u5b8c\u6210", "last_update": old_date},
        }
        results = check_last_update_stale(projects, stale_days=14)
        assert len(results) == 0  # completed projects are not checked

    def test_maintaining_project_checked(self):
        old_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        projects = {
            "proj-a": {"status": "\u7ef4\u62a4\u4e2d", "last_update": old_date},
        }
        results = check_last_update_stale(projects, stale_days=14)
        assert len(results) == 1
        assert results[0]["level"] == "info"

    def test_no_last_update_field(self):
        projects = {
            "proj-a": {"status": "\u8fd0\u884c\u4e2d"},
        }
        results = check_last_update_stale(projects, stale_days=14)
        # Missing last_update should be treated as stale or skipped gracefully
        # Design choice: treat as info (stale)
        assert len(results) == 1
        assert results[0]["level"] == "info"


# ---------------------------------------------------------------------------
# test_check_layer_assignment
# ---------------------------------------------------------------------------

class TestCheckLayerAssignment:
    def test_correct_assignment(self, tmp_root):
        projects = {
            "proj-a": {"docs": "`MacClaude/proj-a/`"},
        }
        layer_yamls = {"macclaude": str(tmp_root / "mc.yaml")}
        # Write a layer yaml that contains proj-a
        _write_yaml(layer_yamls["macclaude"], _make_general({"proj-a": {"status": "\u8fd0\u884c\u4e2d"}}))

        results = check_layer_assignment(projects, layer_yamls)
        assert len(results) == 0

    def test_incorrect_assignment(self, tmp_root):
        """Project with docs MacClaude/... but NOT in MacClaude YAML."""
        projects = {
            "proj-a": {"docs": "`MacClaude/proj-a/`"},
        }
        layer_yamls = {"macclaude": str(tmp_root / "mc.yaml")}
        # MacClaude layer is empty -- proj-a is missing from it
        _write_yaml(layer_yamls["macclaude"], _make_general({}))

        results = check_layer_assignment(projects, layer_yamls)
        assert len(results) == 1
        assert results[0]["level"] == "warning"
        assert results[0]["project"] == "proj-a"

    def test_mixed_docs_uses_first_prefix(self, tmp_root):
        """Docs like `MacClaude/a/` + `Win_Claude_Work/b/` should match MacClaude."""
        projects = {
            "proj-a": {"docs": "`MacClaude/proj-a/` + `Win_Claude_Work/proj-a/`"},
        }
        layer_yamls = {
            "macclaude": str(tmp_root / "mc.yaml"),
            "win_claude_work": str(tmp_root / "wcw.yaml"),
        }
        _write_yaml(layer_yamls["macclaude"], _make_general({"proj-a": {"status": "\u8fd0\u884c\u4e2d"}}))
        _write_yaml(layer_yamls["win_claude_work"], _make_general({}))

        results = check_layer_assignment(projects, layer_yamls)
        assert len(results) == 0  # first prefix matches, so OK

    def test_tilde_docs_not_layer_checked(self, tmp_root):
        """Docs starting with ~/ are not expected in any specific layer."""
        projects = {
            "proj-a": {"docs": "`~/projects/wechat-macro-kb/docs/`"},
        }
        layer_yamls = {"macclaude": str(tmp_root / "mc.yaml")}
        _write_yaml(layer_yamls["macclaude"], _make_general({}))

        results = check_layer_assignment(projects, layer_yamls)
        # ~/ paths don't map to a specific layer, so no assignment check
        assert len(results) == 0


# ---------------------------------------------------------------------------
# test_check_docs_dir_exists
# ---------------------------------------------------------------------------

class TestCheckDocsDirExists:
    def test_existing_dir_is_ok(self, tmp_root, real_dirs):
        projects = {
            "proj-a": {"docs": f"`{real_dirs['existing']}/`"},
        }
        results = check_docs_dir_exists(projects, root_dir=str(tmp_root))
        assert len(results) == 0

    def test_missing_dir_is_warning(self, tmp_root, real_dirs):
        projects = {
            "proj-a": {"docs": f"`{real_dirs['missing']}/`"},
        }
        results = check_docs_dir_exists(projects, root_dir=str(tmp_root))
        assert len(results) == 1
        assert results[0]["level"] == "warning"
        assert results[0]["project"] == "proj-a"

    def test_relative_path_resolves(self, tmp_root):
        # Create the actual dir under root
        (tmp_root / "MacClaude" / "proj-x").mkdir(parents=True)
        projects = {
            "proj-a": {"docs": "`MacClaude/proj-x/`"},
        }
        results = check_docs_dir_exists(projects, root_dir=str(tmp_root))
        assert len(results) == 0

    def test_windows_path_is_skipped(self, tmp_root):
        projects = {
            "proj-a": {"docs": "`Win_Claude_Work/proj-a/`"},
        }
        results = check_docs_dir_exists(projects, root_dir=str(tmp_root))
        assert len(results) == 0  # Win_Claude_Work is a Windows layer, skip

    def test_mixed_docs_checks_first(self, tmp_root):
        """`MacClaude/a/` + `Win_Claude_Work/b/` should only check the first."""
        (tmp_root / "MacClaude" / "proj-a").mkdir(parents=True)
        projects = {
            "proj-a": {"docs": "`MacClaude/proj-a/` + `Win_Claude_Work/proj-a/`"},
        }
        results = check_docs_dir_exists(projects, root_dir=str(tmp_root))
        assert len(results) == 0

    def test_tilde_expansion(self, tmp_root):
        projects = {
            "proj-a": {"docs": "`~/nonexistent_docs_dir_xyz/`"},
        }
        results = check_docs_dir_exists(projects, root_dir=str(tmp_root))
        assert len(results) == 1
        assert results[0]["level"] == "warning"
