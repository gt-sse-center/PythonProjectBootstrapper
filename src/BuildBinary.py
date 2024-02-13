# ----------------------------------------------------------------------
# SPDX-FileCopyrightText: 2024 Scientific Software Engineering Center <ssec-dev@gatech.edu>
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------
"""Builds the binary for this project."""

import datetime
import importlib
import textwrap

from pathlib import Path

from cx_Freeze import setup, Executable
from dbrownell_Common import PathEx


# ----------------------------------------------------------------------
_name = "PythonProjectBootstrapper"
_initial_year: int = 2024
_entry_point_script = PathEx.EnsureFile(
    Path(__file__).parent / "PythonProjectBootstrapper" / "EntryPoint.py",
)
_copyright_template = textwrap.dedent(
    """\

Copyright (c) {year}{year_suffix} Scientific Software Engineering Center

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

""",
).strip()


# ----------------------------------------------------------------------
# Get the version and docstring
mod = importlib.import_module(_name)
_version = mod.__version__

mod = importlib.import_module("{}.{}".format(_name, _entry_point_script.stem))
_docstring = mod.__doc__

del mod


# ----------------------------------------------------------------------
# Create the year suffix
_year = datetime.datetime.now().year

if _year == _initial_year:
    _year_suffix = ""
elif _year // 100 != _initial_year // 100:
    _year_suffix = str(_year)
else:
    _year_suffix = "-{}".format(_year % 100)


# ----------------------------------------------------------------------
setup(
    name=_name,
    version=_version,
    description=_docstring,
    executables=[
        Executable(
            _entry_point_script,
            base="console",
            copyright=_copyright_template.format(
                year=str(_initial_year),
                year_suffix=_year_suffix,
            ),
            # icon=<icon_filename>,
            target_name=_name,
            # trademarks=<trademarks>,
        ),
    ],
    options={
        "build_exe": {
            "excludes": [
                "tcl",
                "tkinter",
            ],
            "no_compress": False,
            "optimize": 0,
            # "packages": [],
            # "include_files": [],
        },
    },
)
