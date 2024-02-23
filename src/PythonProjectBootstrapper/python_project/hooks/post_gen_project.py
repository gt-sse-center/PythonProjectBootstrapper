# ----------------------------------------------------------------------
#
# Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# Distributed under the MIT License.
#
# ----------------------------------------------------------------------
import shutil
import sys
import textwrap

from pathlib import Path
from typing import Callable

from dbrownell_Common import PathEx
from rich import print


# ----------------------------------------------------------------------
def UpdateLicenseFile():
    this_dir = Path.cwd()
    licenses_dir = PathEx.EnsureDir(this_dir / "Licenses")

    license_name = "{{ cookiecutter.license }}"

    if license_name == "BSL-1.0":
        source_file = licenses_dir / "BST-1.0_LICENSE_1_0.txt"
    else:
        source_file = licenses_dir / "{}_LICENSE.txt".format(license_name)

    PathEx.EnsureFile(source_file)
    dest_file = this_dir / source_file.name[len(license_name) + 1 :]

    shutil.copy(source_file, dest_file)
    shutil.rmtree(licenses_dir)


UpdateLicenseFile()


print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
