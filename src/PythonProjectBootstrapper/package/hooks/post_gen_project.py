# ----------------------------------------------------------------------
#
# Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# Distributed under the MIT License.
#
# ----------------------------------------------------------------------
import shutil
import yaml

from pathlib import Path

from dbrownell_Common import PathEx
from rich import print  # pylint: disable=redefined-builtin
from rich.panel import Panel


# ----------------------------------------------------------------------
def SavePromptValues():
    prompt_val_dict: dict[str, str] = {
        "github_url": "{{ cookiecutter.github_url }}",
        "github_project_name": "{{ cookiecutter.github_project_name }}",
        "github_username": "{{ cookiecutter.github_username }}",
        "pypi_project_name": "{{ cookiecutter.pypi_project_name }}",
        "license": "{{ cookiecutter.license }}",
    }

    yaml_path = Path.cwd() / "PromptPopulateValues.yml"

    prompt_yaml_file = open(yaml_path, "w")
    yaml.dump(prompt_val_dict, prompt_yaml_file)
    prompt_yaml_file.close()


# ----------------------------------------------------------------------
def UpdateBootstrapExecutionPermissions():
    bootstrap_path = Path("./Bootstrap.sh")

    PathEx.EnsureFile(bootstrap_path)
    status = bootstrap_path.stat()
    bootstrap_path.chmod(status.st_mode | 0o700)


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


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

UpdateLicenseFile()
SavePromptValues()
UpdateBootstrapExecutionPermissions()
