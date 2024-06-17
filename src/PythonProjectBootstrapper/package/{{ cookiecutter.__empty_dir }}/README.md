# {{ cookiecutter.github_project_name }}

<!-- BEGIN: Exclude Package -->
[![CI]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions/workflows/standard.yaml/badge.svg?event=push)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions/workflows/standard.yaml)
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/{{ cookiecutter.gist_username }}/{{ cookiecutter.gist_id }}/raw/{{ cookiecutter.github_project_name }}_coverage.json)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions)
[![License](https://img.shields.io/github/license/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}?color=dark-green)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/master/LICENSE.txt)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}?color=dark-green)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/commits/main/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{{ cookiecutter.pypi_project_name }}?color=dark-green)](https://pypi.org/project/{{ cookiecutter.pypi_project_name | pypi_string }}/)
[![PyPI - Version](https://img.shields.io/pypi/v/{{ cookiecutter.pypi_project_name }}?color=dark-green)](https://pypi.org/project/{{ cookiecutter.pypi_project_name | pypi_string }}/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/{{ cookiecutter.pypi_project_name }})](https://pypistats.org/packages/{{ cookiecutter.pypi_project_name | pypi_string }})
{% if cookiecutter.openssf_best_practices_badge_id.strip().lower() != 'none' -%}
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/{{ cookiecutter.openssf_best_practices_badge_id }}/badge)](https://www.bestpractices.dev/projects/{{ cookiecutter.openssf_best_practices_badge_id }})
{% endif %}
<!-- END: Exclude Package -->

{{ cookiecutter.project_description }}

<!-- BEGIN: Exclude Package -->
## Contents
- [Overview](#overview)
- [Installation](#installation)
- [Development](#development)
- [Additional Information](#additional-information)
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

{% if cookiecutter.minisign_public_key.strip().lower() != 'none' %}
#### Verifying Signed Executables

Executables are signed and validated using [Minisign](https://jedisct1.github.io/minisign/).

The public key for executables in this repository is `{{ cookiecutter.minisign_public_key }}`.

To verify that the executable is valid, download the corresponding `.minisig` file [here]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/releases/latest) and run this command, replacing `<filename>` with the name of your file.

`docker run -i --rm -v .:/host jedisct1/minisign -V -P {{ cookiecutter.minisign_public_key }} -m /host/<filename>`

Instructions for installing [docker](https://docker.com) are available at https://docs.docker.com/engine/install/.

{% endif %}

### Installation via pip

Install the {{ cookiecutter.pypi_project_name }} package via [pip](https://pip.pypa.io/en/stable/) (Package Installer for Python) to use it with your python code.

`pip install {{ cookiecutter.pypi_project_name }}`

## Development

Please visit [Contributing]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/CONTRIBUTING.md) and [Development]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/DEVELOPMENT.md) for information on contributing to this project.

<!-- END: Exclude Package -->

## Additional Information

Additional information can be found at these locations.

| Title | Document | Description |
| --- | --- | --- |
| Code of Conduct | [CODE_OF_CONDUCT.md]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/CODE_OF_CONDUCT.md) | Information about the the norms, rules, and responsibilities we adhere to when participating in this open source community. |
| Contributing | [CONTRIBUTING.md]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/CONTRIBUTING.md) | Information about contributing code changes to this project. |
| Development | [DEVELOPMENT.md]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/DEVELOPMENT.md) | Information about development activities involved in making changes to this project. |
| Governance | [GOVERNANCE.md]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/GOVERNANCE.md) | Information about how this project is governed. |
| Maintainers | [MAINTAINERS.md]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/MAINTAINERS.md) | Information about individuals who maintain this project. |
| Security | [SECURITY.md]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/SECURITY.md) | Information about how to privately report security issues associated with this project. |

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
