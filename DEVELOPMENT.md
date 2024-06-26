# Local Development

## Enlistment
Enlistment in this repository involves these steps.

| Step | Command Line | Description |
| --- | --- | --- |
| 1. Clone the repository locally | `git clone https://github.com/gt-sse-center/PythonProjectBootstrapper` | https://git-scm.com/docs/git-clone |
| 2. Bootstrap the repository | <table><tr><td>Linux / MacOS:</td><td><code>./Bootstrap.sh [--python-version &lt;python version&gt;] [--package]</code></td></tr><tr><td>Windows:</td><td><code>Bootstrap.cmd [--python-version &lt;python version&gt;] [--package]</code></td></tr></table> | <p>Prepares the repository for local development by enlisting in all dependencies.</p>The `--package` argument is required to run the [Python Package Creation](#python-package-creation) and [Python Package Publising](#python-package-publishing) steps below. |
| 3. Activate the environment | <table><tr><td>Linux / MacOS:</td><td><code>. ./Activate.sh</code></td></tr><tr><td>Windows:</td><td><code>Activate.cmd</code></td></tr></table> | <p>Activates the terminal for development. Each new terminal window must be activated.</p><p>`Activate.sh/.cmd` is actually a shortcut to the most recently bootstrapped version of python (e.g. `Activate3.11.sh/.cmd`). With this functionality, it is possible to support multiple python versions in the same repository and activate each in a terminal using the python-specific activation script.</p> |
| 4. [Optional] Deactivate the environment | <table><tr><td>Linux / MacOS:</td><td><code>. ./Deactivate.sh</code></td></tr><tr><td>Windows:</td><td><code>Deactivate.cmd</code></td></tr></table> | Deactivates the terminal environment. Deactivating is optional, as the terminal window itself may be closed when development activities are complete. |

## Development Activities

Each of these activities can be invoked from an activated terminal on your local machine.

| Activity | Command Line | Description | Invoked by [Continuous Integration](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/.github/workflows/standard.yaml) |
| --- | --- | --- | :---: |
| Code Formatting | `python Build.py black [--format]` | Format source code using [black](https://github.com/psf/black) based on settings in [pyproject.toml](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/pyproject.toml). | :white_check_mark: |
| Static Code Analysis | `python Build pylint` | Validate source code using [pylint](https://github.com/pylint-dev/pylint) based on settings in [pyproject.toml](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/pyproject.toml). | :white_check_mark: |
| Automated Testing | `python Build pytest [--code-coverage]` | Run automated tests using [pytest](https://docs.pytest.org/) and (optionally) extract code coverage information using [coverage](https://coverage.readthedocs.io/) based on settings in [pyproject.toml](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/pyproject.toml). | :white_check_mark: |
| Semantic Version Generation | `python Build.py update_version` | Generate a new [Semantic Version](https://semver.org) based on git commits using [AutoGitSemVer](https://github.com/davidbrownell/AutoGitSemVer). Version information is stored [here](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/src/PythonProjectBootstrapper/__init__.py). | :white_check_mark: |
| Python Package Creation | <p>`python Build.py package`</p><p>Requires that the repository was bootstrapped with the `--package` flag.</p> | Create a python package using [setuptools](https://github.com/pypa/setuptools) based on settings in [pyproject.toml](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/pyproject.toml). | <p>:white_check_mark:</p><p>Packages are built for all supported python versions.</p> |
| Python Package Publishing | <p>`python Build.py publish`</p><p>Requires that the repository was bootstrapped with the `--package` flag.</p> | Publish a python package to [PyPi](https://pypi.org). | :white_check_mark: |
| Build Binaries | `python Build.py build_binaries` | Create a python binary for your current operating system using [cx_Freeze](https://cx-freeze.readthedocs.io/) based on settings in [BuildBinary.py](https://github.com/gt-sse-center/PythonProjectBootstrapper/blob/main/src/BuildBinary.py). | <p>:white_check_mark:</p><p>Binaries are built for Linux, MacOS, and Windows.</p>

## Generated Content

A brief description of the most important content generated by `PythonProjectBootstrapper`.

### `.github/`

Information that defines the CI/CD workflows used by GitHub actions.

### `src/`

Python source code making up the contents of your package. `src/<project_name>/EntryPoint.py` represents an executable script that can be invoked on the command line once your package is installed and `src/<project_name>/Math.py` contains functionality that can be used by other python modules when your package is installed.

### `tests/`

Automated tests that exercise functionality defined within your package. There should be a file in `tests/` that corresponds to every file in `src/`.

### `Bootstrap.sh` / `Bootstrap.cmd`

Script that prepares your repository for development within the local environment. This script installs python (if necessary), creates a virtual python environment, and installs the python dependencies defined in `pyproject.toml`. In addition, it creates the files `Activate.sh` / `Activate.cmd` and `Deactivate.sh` / `Deactivate.cmd`.

Visit [PythonBootstrapper](https://github.com/davidbrownell/PythonBootstrapper) for more information about these files.

### `Build.py`

The entry point for local development activities for your repository. Run `python Build.py --help` for more information about this script.

### `pyproject.toml`

Configuration settings for your python project and tools used in its development. Visit the [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) for more information on this file.

## Frequently Asked Questions (FAQs)

### Python Dependencies

#### How do I modify the python dependencies for my project?

Open `/pyproject.toml` and edit one of the following values:

| Section | Value | Description |
| --- | --- | --- |
| `[project]` | `dependencies` | Python package dependencies required by your package; these will be installed when your package is installed. |
| `[project.optional-dependencies]` | `dev` | Python package dependencies required for local development (e.g. when `Bootstrap` is invoked). |
| `[project.optional-dependencies]` | `package` | Additional python package dependencies required for local development when creating or publishing wheels (e.g. when `Bootstrap --package` is invoked). |

Information about the format of these values can be found [here](https://peps.python.org/pep-0631/).

### Executable Scripts

Executable scripts are python files that can be executed from the command line when your python package is installed. You may specify any number of these scripts.

#### How do I modify the executable scripts generated when my package is installed?

Open `/pyproject.toml` and modify the `[project.scripts]` section. These values are line delimited and should be in the format:

`<script_name>` = `<module_name>:<script_name>.app`

Example:

- `src/MyPackage/ScriptA.py` is a python file using [typer](https://typer.tiangolo.com/) that defines a global variable named `app`.
- `src/MyPackage/ScriptB.py` is a python file using [typer](https://typer.tiangolo.com/) that defines a global variable named `app`.

```
[project.scripts]
MyScript1 = MyPackage:ScriptA.app
MyScript2 = MyPackage:ScriptB.app
```

After these changes, running `MyScript1` on the command line will invoke `src/MyPackage/ScriptA.py` and running `MyScript2` will invoke `src/MyPackage/ScriptB.py`.

Note that this example used different names for the script name and the python file that it invokes. This is to show that these values can vary independently when defined in `pyproject.toml`. Normally, the script name should be the same as the name of the python file that implements it.

### Continuous Integration

#### How do I modify the required pylint score?

Open `Build.py` and search for `default_min_score=`. Set this to a decimal value >= 0.0 and <= 10.0.

#### How do I modify the required code coverage percentage?

Open `Build.py` and search for `default_min_coverage=`. Set this to a decimal value >= 0.0 and <= 100.0.

#### How do I change the command line used to validate a package installation?

Open `.github/workflows/standard.yaml` and search for `validation_command: ` under the section `validate_package`. Update the value to the new command line.

#### How do I change the command line used to validate an executable?

Open `.github/workflows/standard.yaml` and search for `validation_command: ` under the section `validate_binary`. Update the value to the new command line.
