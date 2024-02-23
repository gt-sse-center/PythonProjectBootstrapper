# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Unit tests for EntryPoint.py"""

from typer.testing import CliRunner

from PythonProjectBootstrapper import __version__
from PythonProjectBootstrapper.EntryPoint import app


# ----------------------------------------------------------------------
def test_Version():
    result = CliRunner().invoke(app, ["python_project", "<output_dir>", "--version"])
    assert result.exit_code == 0
    assert result.stdout == __version__
