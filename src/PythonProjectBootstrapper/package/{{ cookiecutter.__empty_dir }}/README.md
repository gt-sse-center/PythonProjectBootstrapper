# {{ cookiecutter.github_project_name }}

[![CI]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions/workflows/standard.yaml/badge.svg?event=push)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions/workflows/standard.yaml)
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/{{ cookiecutter.github_username }}/{{ cookiecutter.gist_id }}/raw/{{ cookiecutter.github_project_name }}_coverage.json)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions)
[![License](https://img.shields.io/github/license/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}?color=dark-green)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/master/LICENSE.txt)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}?color=dark-green)]({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/commits/main/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{{ cookiecutter.pypi_project_name }}?color=dark-green)](https://pypi.org/project/{{ cookiecutter.pypi_project_name | pypi_string }}/)
[![PyPI - Version](https://img.shields.io/pypi/v/{{ cookiecutter.pypi_project_name }}?color=dark-green)](https://pypi.org/project/{{ cookiecutter.pypi_project_name | pypi_string }}/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/{{ cookiecutter.pypi_project_name }})](https://pypistats.org/packages/{{ cookiecutter.pypi_project_name | pypi_string }})

# {{ cookiecutter.github_project_name }}
{{ cookiecutter.project_description }}

### Overview

TODO: Complete this section

### How to use {{ cookiecutter.github_project_name }}

TODO: Complete this section

## Installation via pip

`pip install {{ cookiecutter.pypi_project_name }}`

## Local Development

1) Clone this repository
2) Bootstrap the local repository by running...
    <table>
        <tr>
            <th>Operating System</th>
            <th>Command</th>
        </tr>
        <tr>
            <td>Linux / MacOS</td>
            <td><code>Bootstrap.sh --package</code></td>
        </tr>
        <tr>
            <td>Windows</td>
            <td><code>Bootstrap.cmd --package</code></td>
        </tr>
    </table>
3) Activate the development environment by running...
    <table>
        <tr>
            <th>Operating System</th>
            <th>Command</th>
        </tr>
        <tr>
            <td>Linux / MacOS</td>
            <td><code>. ./Activate.sh</code></td>
        </tr>
        <tr>
            <td>Windows</td>
            <td><code>Activate.cmd</code></td>
        </tr>
    </table>
4) Invoke `Build.py`
    <table>
        <tr>
            <th>Command</th>
            <th>Description</th>
            <th>Example</th>
        </tr>
        <tr>
            <td><code>black</code></td>
            <td>Validates that the source code is formatted by <a href="https://github.com/psf/black" target="_blank">black</a>.</td>
            <td>
                <p>
                    Validation:<br/>
                    <code>python Build.py black</code>
                </p>
                <p>
                    Perform formatting:<br/>
                    <code>python Build.py black --format</code>
                </p>
            </td>
        </tr>
        <tr>
            <td><code>pylint</code></td>
            <td>Validates the source code using <a href="https://github.com/pylint-dev/pylint" target="_blank">pylint</a>.</td>
            <td><code>python Build.py pylint</code></td>
        </tr>
        <tr>
            <td><code>pytest</code></py>
            <td>Runs automated tests using <a href="https://docs.pytest.org/" target="_blank">pytest</a>.</td>
            <td>
                <p>
                    Without Code Coverage:<br/>
                    <code>python Build.py pytest</code>
                </p>
                <p>
                    With Code Coverage:<br/>
                    <code>python Build.py pytest --code-coverage</code>
                </p>
            </td>
        </tr>
        <tr>
            <td><code>update_version</code></td>
            <td>Updates the <a href="https://semver.org/" target="_blank">semantic version</a> of the package based on git commits using <a href="https://github.com/davidbrownell/AutoGitSemVer" target="_blank">AutoGitSemVer</a>.</td>
            <td><code>python Build.py update_version</code></td>
        </tr>
        <tr>
            <td><code>package</code></td>
            <td>Creates a Python wheel package for distribution; outputs to the <code>/dist</code> directory.</td>
            <td><code>python Build.py package</code></td>
        </tr>
        <tr>
            <td><code>publish</code></td>
            <td>Publishes a Python wheel package to <a href="https://pypi.org/" target="_blank">PyPi</a>.</td>
            <td>
                <p>
                    <a href="https://test.pypi.org/" target="_blank">https://test.pypi.org</a>:<br/>
                    <code>python Build.py publish &lt;your PyPi API token here&gt;</code>
                </p>
                <p>
                    <a href="https://pypi.org/" target="_blank">https://pypi.org</a>:<br/>
                    <code>python Build.py publish &lt;your PyPi API token here&gt; --production</code>
                </p>
            </td>
        </tr>
        <tr>
            <td><code>build_binary</code></td>
            <td>Builds an executable for your package that can be run on machines without a python installation; outputs to the <code>/build</code> directory.</td>
            <td><code>python Build.py build_binary</code></td>
        </tr>
{%- if cookiecutter.create_docker_image -%}
        <tr>
            <td><code>create_docker_image</code></td>
            <td>Creates a <a href="https://www.docker.com/" target="_blank">Docker</a> image based on the current development environment. This supports the "Reusable" aspect of <a href="https://www.go-fair.org/fair-principles/" target="_blank">FAIR principles</a> by creating a snapshot of the repository and all of its dependencies as they exist in a single moment in time.</td>
            <td><code>python Build.py create_docker_image</code></td>
        </tr>
{% endif %}
    </table>

5) [Optional] Deactivate the development environment by running:
    <table>
        <tr>
            <th>Operating System</th>
            <th>Command</th>
        </tr>
        <tr>
            <td>Linux / MacOS</td>
            <td><code>. ./Deactivate.sh</code></td>
        </tr>
        <tr>
            <td>Windows</td>
            <td><code>Deactivate.cmd</code></td>
        </tr>
    </table>

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
