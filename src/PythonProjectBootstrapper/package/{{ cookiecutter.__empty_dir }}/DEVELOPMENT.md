# Local Development

## Enlistment
Enlistment in this repository involves these steps.

| Step | Command Line | Description |
| --- | --- | --- |
| 1. Clone the repository locally | `git clone {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}` | https://git-scm.com/docs/git-clone |
| 2. Bootstrap the repository | <table><tr><td>Linux / MacOS:</td><td><code>./Bootstrap.sh [--python-version &lt;python version&gt;] [--package]</code></td></tr><tr><td>Windows:</td><td><code>Bootstrap.cmd [--python-version &lt;python version&gt;] [--package]</code></td></tr></table> | <p>Prepares the repository for local development by enlisting in all dependencies.</p>The `--package` argument is required to run the [Python Package Creation](#python-package-creation) and [Python Package Publising](#python-package-publishing) steps below. |
| 3. Activate the environment | <table><tr><td>Linux / MacOS:</td><td><code>. ./Activate.sh</code></td></tr><tr><td>Windows:</td><td><code>Activate.cmd</code></td></tr></table> | <p>Activates the terminal for development. Each new terminal window must be activated.</p><p>`Activate.sh/.cmd` is actually a shortcut to the most recently bootstrapped version of python (e.g. `Activate3.11.sh/.cmd`). With this functionality, it is possible to support multiple python versions in the same repository and activate each in a terminal using the python-specific activation script.</p> |
| 4. [Optional] Deactivate the environment | <table><tr><td>Linux / MacOS:</td><td><code>. ./Deactivate.sh</code></td></tr><tr><td>Windows:</td><td><code>Deactivate.cmd</code></td></tr></table> | Deactivates the terminal environment. Deactivating is optional, as the terminal window itself may be closed when development activities are complete. |

## Development Activities

Each of these activities can be invoked from an activated terminal on your local machine.

| Activity | Command Line | Description | Invoked by [Continuous Integration]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/.github/workflows/standard.yaml) |
| --- | --- | --- | :---: |
| Code Formatting | `python Build.py black [--format]` | Format source code using [black](https://github.com/psf/black) based on settings in [pyproject.toml]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/pyproject.toml). | :white_check_mark: |
| Static Code Analysis | `python Build pylint` | Validate source code using [pylint](https://github.com/pylint-dev/pylint) based on settings in [pyproject.toml]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/pyproject.toml). | :white_check_mark: |
| Automated Testing | `python Build pytest [--code-coverage]` | Run automated tests using [pytest](https://docs.pytest.org/) and (optionally) extract code coverage information using [coverage](https://coverage.readthedocs.io/) based on settings in [pyproject.toml]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/pyproject.toml). | :white_check_mark: |
| Semantic Version Generation | `python Build.py update_version` | Generate a new [Semantic Version](https://semver.org) based on git commits using [AutoGitSemVer](https://github.com/davidbrownell/AutoGitSemVer). Version information is stored [here]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/src/{{ cookiecutter.pypi_project_name }}/__init__.py). | :white_check_mark: |
| Python Package Creation | <p>`python Build.py package`</p><p>Requires that the repository was bootstrapped with the `--package` flag.</p> | Create a python package using [setuptools](https://github.com/pypa/setuptools) based on settings in [pyproject.toml]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/pyproject.toml). | <p>:white_check_mark:</p><p>Packages are built for all supported python versions.</p> |
| Python Package Publishing | <p>`python Build.py publish`</p><p>Requires that the repository was bootstrapped with the `--package` flag.</p> | Publish a python package to [PyPi](https://pypi.org). | :white_check_mark: |
| Build Binaries | `python Build.py build_binaries` | Create a python binary for your current operating system using [cx_Freeze](https://cx-freeze.readthedocs.io/) based on settings in [BuildBinary.py]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/src/BuildBinary.py). | <p>:white_check_mark:</p><p>Binaries are built for Linux, MacOS, and Windows.</p>
{%- if cookiecutter.create_docker_image %}
| Development Docker Image | `python Build.py create_docker_image` | Create a [docker](https://docker.com) image for a bootstrapped development environment. This functionality is useful when adhering to the [FAIR principles for research software](https://doi.org/10.1038/s41597-022-01710-x) by supporting the creation of a development environment and its dependencies as they existed at the moment when the image was created. | :white_check_mark: |
{% endif %}
