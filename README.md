# PythonProjectBootstrapper

<!-- BEGIN: Exclude Package -->
[![CI](https://github.com/gt-sse-center/PythonProjectBootstrapper/actions/workflows/standard.yaml/badge.svg?event=push)](https://github.com/gt-sse-center/PythonProjectBootstrapper/actions/workflows/standard.yaml)
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/davidbrownell/2f9d770d13e3a148424f374f74d41f4b/raw/PythonProjectBootstrapper_coverage.json)](https://github.com/gt-sse-center/PythonProjectBootstrapper/actions)
[![License](https://img.shields.io/github/license/gt-sse-center/PythonProjectBootstrapper?color=dark-green)](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/master/LICENSE.txt)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/gt-sse-center/PythonProjectBootstrapper?color=dark-green)](https://github.com/gt-sse-center/PythonProjectBootstrapper/commits/main/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PythonProjectBootstrapper?color=dark-green)](https://pypi.org/project/pythonprojectbootstrapper/)
[![PyPI - Version](https://img.shields.io/pypi/v/PythonProjectBootstrapper?color=dark-green)](https://pypi.org/project/pythonprojectbootstrapper/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/PythonProjectBootstrapper)](https://pypistats.org/packages/pythonprojectbootstrapper)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/9132/badge)](https://www.bestpractices.dev/projects/9132)

<!-- END: Exclude Package -->

Tool that helps in the creation of python projects.

<!-- BEGIN: Exclude Package -->
## Contents
- [Overview](#overview)
- [Installation](#installation)
- [Development](#development)
- [Additional Information](#additional-information)
- [License](#license)
<!-- END: Exclude Package -->

## Overview

`PythonProjectBootstrapper` creates a python project that adheres to modern best practices for python package development. It also generates Continuous Integration / Delivery / Deployment workflows that maximize the free functionality offered by GitHub for open-source solutions.

#### Functionality Provided in Generated Projects

- Simple local development through `Build.py` (see [Local Development](#local-development) for more information)
- Python bootstrapping via [PythonBootstrapper](https://github.com/davidbrownell/PythonBootstrapper)
- Source code formatting via [black](https://github.com/psf/black)
- Static source analysis via [pylint](https://github.com/pylint-dev/pylint)
- Test execution via [pytest](https://docs.pytest.org/)
- Code coverage extraction via [coverage](https://coverage.readthedocs.io/)
- Semantic version generation via [AutoGitSemVer](https://github.com/davidbrownell/AutoGitSemVer)
- Python [wheel](https://pythonwheels.com/) creation
- Wheel deployment to [PyPi](https://pypi.org)
- Executable generation via [cx_Freeze](https://marcelotduarte.github.io/cx_Freeze/)
- Full [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration), [Continuous Delivery](https://en.wikipedia.org/wiki/Continuous_delivery), and [Continuous Deployment](https://en.wikipedia.org/wiki/Continuous_deployment) (via [GitHub Actions](https://github.com/features/actions)) for everything listed above
- GitHub [Recommended Community Standards](https://opensource.guide/) documentation
- GitHub [pull request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- GitHub [issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [Optional] Build artifact signing via [Minisign](https://jedisct1.github.io/minisign/)
- [Optional] Participation in the [Open Source Security Foundation (OpenSSF) Best Practices Badge Program](https://www.bestpractices.dev/)
- [Optional] Generation of development environment [docker](https://www.docker.com/) [images](https://aws.amazon.com/compare/the-difference-between-docker-images-and-containers/) in support of [FAIR principles](https://www.go-fair.org/fair-principles/)

#### Project Content Customization

Please see [DEVELOPMENT.md](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/DEVELOPMENT.md) for information on the generated content and how to make common modifications to that content.

### How to use PythonProjectBootstrapper

#### Running the Executable

From a terminal window, run one of the commands below. You will be asked a series of questions when generating a python project, then guided through configuration activities to ensure that the project is ready for use.

<table>
    <tr>
        <th>Scenario</th>
        <th>Command Line</th>
        <th>Output</th>
    </tr>
    <tr>
        <td>Create a project for a <a href="https://packaging.python.org/en/latest/" target="_blank">python package</a></td>
        <td><code>PythonProjectBootstrapper package &lt;output_dir&gt;</code></td>
        <td>
<pre style="background-color: black; color: #AAAAAA; font-size: .75em">
┌──────────────────────────────────────────────────────────────────────────────── Python Package ─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                                                                                                 │
│ This project creates a Python package hosted on GitHub that uploads a Python wheel to PyPi. It also includes opt-in functionality to create docker images that ensure the exact │
│ reproducibility of all commits (which is especially useful for scientific software).                                                                                            │
│                                                                                                                                                                                 │
│ If you continue, you will be asked a series of questions about your project and given step-by-step instructions on how to set up your project so that it works with 3rd party   │
│ solutions (GitHub, PyPi, etc.).                                                                                                                                                 │
│                                                                                                                                                                                 │
│ The entire process should take about 20 minutes to complete.                                                                                                                    │
│                                                                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
&nbsp;
Enter 'yes' to continue or 'no' to exit:
</pre>
       </td>
    </tr>
    <tr>
        <td>Display Help</td>
        <td><code>PythonProjectBootstrapper --help</code></td>
        <td>
<pre style="background-color: black; color: #AAAAAA; font-size: .75em">&nbsp;
 Usage: PythonProjectBootstrapper [OPTIONS] PROJECT:{package} OUTPUT_DIR
&nbsp;
┌─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ *    project         PROJECT:{package}  Project to build. [default: None] [required]                                                                                            │
│ *    output_dir      DIRECTORY          Directory to populate. [default: None] [required]                                                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
┌─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ --configuration             FILE  Filename that contains template configuration values; see <a href="https://cookiecutter.readthedocs.io/en/stable/advanced/user_config.html">https://cookiecutter.readthedocs.io/en/stable/advanced/user_config.html</a> for more    │
│                                   info.                                                                                                                                         │
│                                   [default: None]                                                                                                                               │
│ --replay                          Do not prompt for input, instead read from saved json.                                                                                        │
│ --yes                             Answer yes to all prompts.                                                                                                                    │
│ --skip-prompts                    Do not display prompts after generating content.                                                                                              │
│ --version                         Display the current version and exit.                                                                                                         │
│ --install-completion              Install completion for the current shell.                                                                                                     │
│ --show-completion                 Show completion for the current shell, to copy it or customize the installation.                                                              │
│ --help                            Show this message and exit.                                                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘</pre>
        </td>
    </tr>
    <tr>
        <td>Version</td>
        <td><code>PythonProjectBootstrapper --version</code></td>
        <td>
<pre style="background-color: black; color: #AAAAAA; font-size: .75em">PythonProjectBootstrapper v0.2.0</pre>
        </td>
    </tr>
</table>

<!-- BEGIN: Exclude Package -->
## Installation

PythonProjectBootstrapper can be installed via one of these methods:

- [Installation via Executable](#installation-via-executable)
- [Installation via pip](#installation-via-pip)

### Installation via Executable

Download an executable for Linux, MacOS, or Windows to use the functionality provided by this repository without a dependency on [Python](https://www.python.org).

1. Download the archive for the latest release [here](https://github.com/gt-sse-center/PythonProjectBootstrapper/releases/latest); the files will begin with `exe.` and contain the name of your operating system.
2. Decompress the archive


#### Verifying Signed Executables

Executables are signed and validated using [Minisign](https://jedisct1.github.io/minisign/).

The public key for executables in this repository is `RWRkzrG0tznlEpemQ9U4aCQU/TO1TXipqycs7G9pRrm/9ab9HBcV/EIf`.

To verify that the executable is valid, download the corresponding `.minisig` file [here](https://github.com/gt-sse-center/PythonProjectBootstrapper/releases/latest) and run this command, replacing `<filename>` with the name of your file.

`docker run -i --rm -v .:/host jedisct1/minisign -V -P RWRkzrG0tznlEpemQ9U4aCQU/TO1TXipqycs7G9pRrm/9ab9HBcV/EIf -m /host/<filename>`

Instructions for installing [docker](https://docker.com) are available at https://docs.docker.com/engine/install/.



### Installation via pip

Install the PythonProjectBootstrapper package via [pip](https://pip.pypa.io/en/stable/) (Package Installer for Python) to use it with your python code.

`pip install PythonProjectBootstrapper`

## Development

Please visit [Contributing](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/CONTRIBUTING.md) and [Development](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/DEVELOPMENT.md) for information on contributing to this project.

<!-- END: Exclude Package -->

## Additional Information

Additional information can be found at these locations.

| Title | Document | Description |
| --- | --- | --- |
| Code of Conduct | [CODE_OF_CONDUCT.md](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/CODE_OF_CONDUCT.md) | Information about the the norms, rules, and responsibilities we adhere to when participating in this open source community. |
| Contributing | [CONTRIBUTING.md](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/CONTRIBUTING.md) | Information about contributing code changes to this project. |
| Development | [DEVELOPMENT.md](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/DEVELOPMENT.md) | Information about development activities involved in making changes to this project. |
| Governance | [GOVERNANCE.md](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/GOVERNANCE.md) | Information about how this project is governed. |
| Maintainers | [MAINTAINERS.md](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/MAINTAINERS.md) | Information about individuals who maintain this project. |
| Security | [SECURITY.md](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/SECURITY.md) | Information about how to privately report security issues associated with this project. |

## License

PythonProjectBootstrapper is licensed under the <a href="https://choosealicense.com/licenses/mit/" target="_blank">MIT</a> license.
