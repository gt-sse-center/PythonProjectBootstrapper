{%- include "python_header.py" -%}
"""Builds the binary for this project."""

import datetime
import importlib
import textwrap

from functools import cache
from pathlib import Path

from cx_Freeze import setup, Executable
from dbrownell_Common import PathEx


# ----------------------------------------------------------------------
@cache
def _GetName() -> str:
    return "{{ cookiecutter.pypi_project_name }}"


# ----------------------------------------------------------------------
@cache
def _GetVersionAndDocstring() -> tuple[str, str]:
    mod = importlib.import_module(_GetName())
    return mod.__version__, mod.__doc__ or ""


# ----------------------------------------------------------------------
@cache
def _GetEntryPoint() -> Path:
    return PathEx.EnsureFile(Path(__file__).parent / _GetName() / "EntryPoint.py")


# ----------------------------------------------------------------------
@cache
def _GetCopyright() -> str:
    initial_year = {% now 'utc', '%Y' %}
    current_year = datetime.datetime.now().year

    if current_year == initial_year:
        year_suffix = ""
    elif current_year // 100 != initial_year // 100:
        year_suffix = str(current_year)
    else:
        year_suffix = "-{}".format(current_year % 100)
{%+ if cookiecutter.license == "MIT" %}
    return textwrap.dedent(
        f"""\
        Copyright (c) {initial_year}{year_suffix} {{ cookiecutter.name }}

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
    )
{% elif cookiecutter.license == "Apache-2.0" %}
    return textwrap.dedent(
        f"""\
        Copyright {initial_year}{year_suffix} {{ cookiecutter.name }}

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

            http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.
        """,
    )
{% elif cookiecutter.license == "BSD-3-Clause-Clear" %}
    return textwrap.dedent(
        f"""\
        Copyright {initial_year}{year_suffix} {{ cookiecutter.name }}

        Redistribution and use in source and binary forms, with or without
        modification are permitted provided that the following conditions are met:

        1. Redistributions of source code must retain the above copyright notice,
           this list of conditions and the following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright notice,
           this list of condition and the following disclaimer in the documentation
           and/or other materials provided with the distribution.

        3. Neither the name of the copyright holder nor the names of its
           contributors may be used to endorse or promote products derived from this
           software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
        AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
        IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
        ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
        LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
        CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
        SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
        INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
        CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
        ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
        POSSIBILITY OF SUCH DAMAGE.
        """,
    )
{% elif cookiecutter.license == "GPL-3.0-or-later" %}
    return textwrap.dedent(
        f"""\
        {{ cookiecutter.pypi_project_name }}: {{ cookiecutter.project_description }}
        Copyright (C) {initial_year}{year_suffix}  {{ cookiecutter.name }}

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.
        """,
    )
{% elif cookiecutter.license == "BSL-1.0" %}
    return textwrap.dedent(
        f"""\
        Copyright (C) {initial_year}{year_suffix}  {{ cookiecutter.name }}

        Boost Software License - Version 1.0 - August 17th, 2003

        Permission is hereby granted, free of charge, to any person or organization
        obtaining a copy of the software and accompanying documentation covered by
        this license (the "Software") to use, reproduce, display, distribute,
        execute, and transmit the Software, and to prepare derivative works of the
        Software, and to permit third-parties to whom the Software is furnished to
        do so, all subject to the following:

        The copyright notices in the Software and this entire statement, including
        the above license grant, this restriction and the following disclaimer,
        must be included in all copies of the Software, in whole or in part, and
        all derivative works of the Software, unless such copies or derivative
        works are solely in the form of machine-executable object code generated by
        a source language processor.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
        SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
        FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
        ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
        DEALINGS IN THE SOFTWARE.
        """,
    )
{% else %}
    raise Exception("Unknown license")
{% endif %}

# ----------------------------------------------------------------------
setup(
    name=_GetName(),
    version=_GetVersionAndDocstring()[0],
    description=_GetVersionAndDocstring()[1],
    executables=[
        Executable(
            _GetEntryPoint(),
            base="console",
            copyright=_GetCopyright(),
            # icon=<icon_filename>,
            target_name=_GetName(),
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
