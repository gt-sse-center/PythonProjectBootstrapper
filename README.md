[![CI](https://github.com/gt-sse-center/PythonProjectBootstrapper/actions/workflows/standard.yaml/badge.svg?event=push)](https://github.com/gt-sse-center/PythonProjectBootstrapper/actions/workflows/standard.yaml)
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/davidbrownell/2f9d770d13e3a148424f374f74d41f4b/raw/PythonProjectBootstrapper_coverage.json)](https://github.com/gt-sse-center/PythonProjectBootstrapper/actions)
[![License](https://img.shields.io/github/license/gt-sse-center/PythonProjectBootstrapper?color=dark-green)](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/master/LICENSE.txt)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/gt-sse-center/PythonProjectBootstrapper?color=dark-green)](https://github.com/gt-sse-center/PythonProjectBootstrapper/commits/main/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PythonProjectBootstrapper?color=dark-green)](https://pypi.org/project/pythonprojectbootstrapper/)
[![PyPI - Version](https://img.shields.io/pypi/v/PythonProjectBootstrapper?color=dark-green)](https://pypi.org/project/pythonprojectbootstrapper/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/PythonProjectBootstrapper)](https://pypistats.org/packages/pythonprojectbootstrapper)


Tool that helps in the creation of python projects.

### Quick Start

1. Install via [executable](#installation-via-executable), [pip](#installation-via-pip), or [local development](#local-development)
2. [Run the executable](#running-the-executable)

### Overview

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
- Optional generation of development environment [docker](https://www.docker.com/) [images](https://aws.amazon.com/compare/the-difference-between-docker-images-and-containers/) in support of [FAIR principles](https://www.go-fair.org/fair-principles/)
- Full [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration), [Continuous Delivery](https://en.wikipedia.org/wiki/Continuous_delivery), and [Continuous Deployment](https://en.wikipedia.org/wiki/Continuous_deployment) (via [GitHub Actions](https://github.com/features/actions)) for everything listed above

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
│ --configuration-filename        FILE                             Filename that contains template configuration values; see                                                      │
│                                                                  <a href="https://cookiecutter.readthedocs.io/en/stable/advanced/user_config.html">https://cookiecutter.readthedocs.io/en/stable/advanced/user_config.html</a> for more info.                         │
│                                                                  [default: None]                                                                                                │
│ --replay                                                         Do not prompt for input, instead read from saved json.                                                         │
│ --yes                                                            Answer yes to all prompts.                                                                                     │
│ --version                                                        Display the current version and exit.                                                                          │
│ --install-completion            [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell. [default: None]                                                    │
│ --show-completion               [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation. [default: None]             │
│ --help                                                           Show this message and exit.                                                                                    │
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

## Installation via Executable

Download an executable for Linux, MacOS, or Windows to use the functionality provided by this repository without a dependency on [Python](https://www.python.org).

1. Download the archive for the latest release [here](https://github.com/gt-sse-center/PythonProjectBootstrapper/releases/latest); the files will begin with `exe.` and contain the name of your operating system.
2. Decompress the archive

## Installation via pip

Install the PythonProjectBootstrapper package via [pip](https://pip.pypa.io/en/stable/) (Package Installer for Python) to use it with your python code.

`pip install PythonProjectBootstrapper`

## Local Development

Follow these steps to prepare the repository for local development activities.

1) Clone this repository
2) Bootstrap the local repository by running...
    | Operating System | Command |
    | --- | --- |
    | Linux / MacOS | <p>Standard:<br/>`Bootstrap.sh`</p><p>Standard + packaging:<br/>`Bootstrap.sh --package`</p> |
    | Windows | <p>Standard:<br/>`Bootstrap.cmd`</p><p>Standard + packaging:<br/>`Bootstrap.cmd --package`</p> |
3) Activate the development environment by running...
    | Operating System | Command |
    | --- | --- |
    | Linux / MacOS | `. ./Activate.sh` |
    | Windows | `Activate.cmd` |
4) Invoke `Build.py`
    | Command | Description | Example | Notes |
    | --- | --- | --- | --- |
    | `black` | Validates that the source code is formatted by [black](https://github.com/psf/black). | <p>Validation:<br/>`python Build.py black`</p><p>Perform formatting:<br/>`python Build.py black --format`</p> | |
    | `pylint` | Validates the source code using [pylint](https://github.com/pylint-dev/pylint). | `python Build.py pylint` | |
    | `pytest` | Runs automated tests using [pytest](https://docs.pytest.org/). | <p>Without Code Coverage:<br/>`python Build.py pytest`</p><p>With Code Coverage:<br/>`python Build.py pytest --code-coverage`</p> | |
    | `update_version` | Updates the [semantic version](https://semver.org/) of the package based on git commits using [AutoGitSemVer](https://github.com/davidbrownell/AutoGitSemVer). | `python Build.py update_version` | |
    | `package` | Creates a Python wheel package for distribution; outputs to the `/dist` directory. | `python Build.py package` | Requires `--package` when bootstrapping in step #2. |
    | `publish` | Publishes a Python wheel package to [PyPi](https://pypi.org/). | <p>https://test.pypi.org:<br/>`python Build.py publish`</p><p>https://pypi.org:<br/>`python Build.py publish --production`</p> | Requires `--package` when bootstrapping in step #2. |
    | `build_binary` | Builds an executable for your package that can be run on machines without a python installation; outputs to the `/build` directory. | `python Build.py build_binary` | Requires `--package` when bootstrapping in step #2. |

5) \[Optional] Deactivate the development environment by running...
    | Operating System | Command |
    | --- | --- |
    | Linux / MacOS | `. ./Deactivate.sh` |
    | Windows | `Deactivate.cmd` |

## Similar Tools

There are other tools available that offer similar functionality, each emphasizing different domains, conventions, or workflows. They are listed here in the event that one of them is a better fit for the specifics of your scenario.

| Tool | Description |
| --- | --- |
| [Scientific Python: guide, cookie, & sp-repo-review](https://github.com/scientific-python/cookie) | A copier/cookiecutter template for new Python projects based on the Scientific Python Developer Guide. |
| [cookiecutter-cms](https://github.com/MolSSI/cookiecutter-cms) | A cookiecutter template for those interested in developing computational molecular packages in Python. |
| [LINCC Frameworks Python Project Template](https://github.com/lincc-frameworks/python-project-template) | This project template codifies LINCC-Framework's best practices for python code organization, testing, documentation, and automation. |
| [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django) | Cookiecutter Django is a framework for jumpstarting production-ready Django projects quickly. |

### Templating Systems

| Tool | Description |
| --- | --- |
| [cookiecutter](https://github.com/cookiecutter/cookiecutter) | A cross-platform command-line utility that creates projects from cookiecutters (project templates), e.g. Python package projects, C projects. |
| [copier](https://github.com/copier-org/copier) | A library and CLI app for rendering project templates. |

## License

PythonProjectBootstrapper is licensed under the <a href="https://choosealicense.com/licenses/mit/" target="_blank">MIT</a> license.
