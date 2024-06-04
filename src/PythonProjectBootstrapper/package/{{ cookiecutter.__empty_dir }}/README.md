# {{ cookiecutter.github_project_name }}

<!-- BEGIN: Exclude Package -->
[![CI]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions/workflows/standard.yaml/badge.svg?event=push)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions/workflows/standard.yaml)
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/{{ cookiecutter.gist_username }}/{{ cookiecutter.gist_id }}/raw/{{ cookiecutter.github_project_name }}_coverage.json)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions)
[![License](https://img.shields.io/github/license/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}?color=dark-green)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/master/LICENSE.txt)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}?color=dark-green)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/commits/main/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{{ cookiecutter.pypi_project_name }}?color=dark-green)](https://pypi.org/project/{{ cookiecutter.pypi_project_name | pypi_string }}/)
[![PyPI - Version](https://img.shields.io/pypi/v/{{ cookiecutter.pypi_project_name }}?color=dark-green)](https://pypi.org/project/{{ cookiecutter.pypi_project_name | pypi_string }}/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/{{ cookiecutter.pypi_project_name }})](https://pypistats.org/packages/{{ cookiecutter.pypi_project_name | pypi_string }})
<!-- END: Exclude Package -->

{{ cookiecutter.project_description }}

<!-- BEGIN: Exclude Package -->
## Contents
- [Overview](#overview)
- [Installation](#installation)
- [Contributing](#contributing)
- [Local Development](#local-development)
- [Vulnerability Reporting](#vulnerability-reporting-security-issues)
- [License](#license)
<!-- END: Exclude Package -->

## Overview

TODO: Complete this section

### How to use {{ cookiecutter.github_project_name }}

TODO: Complete this section

<!-- BEGIN: Exclude Package -->
## Installation

{{ cookiecutter.github_project_name }} can be installed via one of these methods:

- [Installation via Executable](#installation-via-executable)
- [Installation via pip](#installation-via-pip)

### Installation via Executable

Download an executable for Linux, MacOS, or Windows to use the functionality provided by this repository without a dependency on [Python](https://www.python.org).

1. Download the archive for the latest release [here]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/releases/latest); the files will begin with `exe.` and contain the name of your operating system.
2. Decompress the archive

### Installation via pip

Install the {{ cookiecutter.pypi_project_name }} package via [pip](https://pip.pypa.io/en/stable/) (Package Installer for Python) to use it with your python code.

`pip install {{ cookiecutter.pypi_project_name }}`

## Contributing
See [CONTRIBUTING.md]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/CONTRIBUTING.md) for information on contributing to {{ cookiecutter.github_project_name }}.

## Local Development

See [DEVELOPMENT.md]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/DEVELOPMENT.md) for information on developing or testing {{ cookiecutter.github_project_name }} on your local Linux, MacOS, or Windows machine.
<!-- END: Exclude Package -->

## Vulnerability Reporting (Security Issues)
Please privately report vulnerabilities you find so we can fix them!

See [SECURITY.md]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/SECURITY.md) for information on how to privately report vulnerabilities.

## License

{{ cookiecutter.github_project_name }} is licensed under the <a href="
{%- if cookiecutter.license == "MIT" -%}
    https://choosealicense.com/licenses/mit/
{%- elif cookiecutter.license == "Apache-2.0" -%}
    https://choosealicense.com/licenses/apache-2.0/
{%- elif cookiecutter.license == "BSD-3-Clause-Clear" -%}
    https://choosealicense.com/licenses/bsd-3-clause-clear/
{%- elif cookiecutter.license == "GPL-3.0-or-later" -%}
    https://choosealicense.com/licenses/gpl-3.0/
{%- elif cookiecutter.license == "BSL-1.0" -%}
    https://choosealicense.com/licenses/bsl-1.0/
{%- endif -%}
" target="_blank">{{ cookiecutter.license }}</a> license.
