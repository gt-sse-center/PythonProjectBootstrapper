# ----------------------------------------------------------------------
# SPDX-FileCopyrightText: 2024 Scientific Software Engineering Center <ssec-dev@gatech.edu>
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------
"""Unit tests for EntryPoint.py"""

from typer.testing import CliRunner

from PythonProjectBootstrapper import __version__
from PythonProjectBootstrapper.EntryPoint import app


# ----------------------------------------------------------------------
def test_Version():
    result = CliRunner().invoke(app, ["this_value_is_ignored", "--version"])
    assert result.exit_code == 0
    assert result.stdout == __version__
