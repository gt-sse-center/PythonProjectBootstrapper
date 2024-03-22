# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for EntryPoint.py"""

from pathlib import Path
from unittest.mock import patch

from dbrownell_Common import PathEx
from typer.testing import CliRunner

from PythonProjectBootstrapper import __version__
from PythonProjectBootstrapper.EntryPoint import app


# ----------------------------------------------------------------------
def test_Version():
    result = CliRunner().invoke(app, ["package", "<output_dir>", "--version"])
    assert result.exit_code == 0
    assert result.stdout == f"PythonProjectBootstrapper {__version__}"


# ----------------------------------------------------------------------
def test_Standard():
    with patch("PythonProjectBootstrapper.EntryPoint.cookiecutter") as mock_cookiecutter:
        repo_root = PathEx.EnsureDir(Path(__file__).parent.parent)

        result = CliRunner().invoke(app, ["package", str(repo_root), "--yes"])

        assert result.exit_code == 0
        assert "This project creates a Python package" in result.stdout
        assert len(mock_cookiecutter.call_args_list) == 1
