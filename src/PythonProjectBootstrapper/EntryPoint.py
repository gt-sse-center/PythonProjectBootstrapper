# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""This file serves as an example of how to create scripts that can be invoked from the command line once the package is installed."""

import hashlib
import importlib
import itertools
import json
import os
import sys
import uuid
import yaml

from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

from rich import print  # pylint: disable=redefined-builtin
from rich.panel import Panel

import typer

from typer.core import TyperGroup  # type: ignore [import-untyped]

from cookiecutter.main import cookiecutter
from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx
from PythonProjectBootstrapper import __version__

# The following imports are used in cookiecutter hooks. Import them here to
# ensure that they are frozen when creating binaries,
import shutil  # pylint: disable=unused-import, wrong-import-order
import textwrap  # pylint: disable=unused-import, wrong-import-order


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):
    # pylint: disable=missing-class-docstring
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs):  # pylint: disable=unused-argument
        return self.commands.keys()


# ----------------------------------------------------------------------
app = typer.Typer(
    cls=NaturalOrderGrouper,
    help=__doc__,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


# ----------------------------------------------------------------------
class ProjectType(str, Enum):
    """Defines the different types of projects that can be specified on the command line."""

    package = "package"


# ----------------------------------------------------------------------
def _VersionCallback(value: bool) -> None:
    if value:
        sys.stdout.write(f"PythonProjectBootstrapper {__version__}")
        raise typer.Exit()


# ----------------------------------------------------------------------
_project_argument = typer.Argument(
    help="Project to build.",
)

_configuration_filename_option = typer.Option(
    "--configuration-filename",
    dir_okay=False,
    exists=True,
    resolve_path=True,
    help="Filename that contains template configuration values; see https://cookiecutter.readthedocs.io/en/stable/advanced/user_config.html for more info.",
)

_replay_option = typer.Option(
    "--replay", help="Do not prompt for input, instead read from saved json."
)
_yes_option = typer.Option("--yes", help="Answer yes to all prompts.")
_version_option = typer.Option(
    "--version",
    help="Display the current version and exit.",
    callback=_VersionCallback,
    is_eager=True,
)


# ----------------------------------------------------------------------
# The cookiecutter project dir must be accessed in different ways depending on whether the code is:
#   - running from source
#   - running from a pip installation
#   - running as a frozen binary.
#
if getattr(sys, "frozen", False):
    _project_root_dir = Path(sys.executable).parent / "lib" / "PythonProjectBootstrapper"

    # This is admittedly very strange. cookiecutter apparently uses sys.argv[0] to invoke
    # python hooks. Within a binary, sys.argv[0] will point back to this file. So, create
    # functionality that invokes cookiecutter when passed a directory and executes python code
    # from a file when invoked as a hook.

    # ----------------------------------------------------------------------
    @app.command()
    def FrozenExecute(
        project: Annotated[ProjectType, _project_argument],
        output_dir: Annotated[
            Path, typer.Argument(resolve_path=True, help="Directory to populate.")
        ],
        configuration_filename: Annotated[Optional[Path], _configuration_filename_option] = None,
        replay: Annotated[bool, _replay_option] = False,
        yes: Annotated[bool, _yes_option] = False,
        version: Annotated[bool, _version_option] = False,  # pylint: disable=unused-argument
    ) -> None:
        if output_dir.is_file():
            with output_dir.open() as f:
                content = f.read()

            exec(content)  # pylint: disable=exec-used
            return

        _ExecuteOutputDir(
            project,
            output_dir,
            configuration_filename,
            replay=replay,
            yes=yes,
        )

    # ----------------------------------------------------------------------

else:
    _project_root_dir = Path(__file__).parent

    # ----------------------------------------------------------------------
    @app.command()
    def StandardExecute(
        project: Annotated[ProjectType, _project_argument],
        output_dir: Annotated[
            Path, typer.Argument(file_okay=False, resolve_path=True, help="Directory to populate.")
        ],
        configuration_filename: Annotated[Optional[Path], _configuration_filename_option] = None,
        replay: Annotated[bool, _replay_option] = False,
        yes: Annotated[bool, _yes_option] = False,
        version: Annotated[bool, _version_option] = False,  # pylint: disable=unused-argument
    ) -> None:
        _ExecuteOutputDir(
            project,
            output_dir,
            configuration_filename,
            replay=replay,
            yes=yes,
        )


PathEx.EnsureDir(_project_root_dir)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _ExecuteOutputDir(
    project: ProjectType,
    output_dir: Path,
    configuration_filename: Optional[Path],
    *,
    replay: bool,
    yes: bool,
) -> None:
    project_dir = PathEx.EnsureDir(_project_root_dir / project.value)

    # create temporary directory for cookiecutter output
    tmp_dir = Path.cwd() / uuid.uuid4().hex
    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(tmp_dir / ".git", exist_ok=True)

    # Does the project have a startup script? If so, invoke it dynamically.
    potential_startup_script = project_dir / "hooks" / "startup.py"
    if potential_startup_script.is_file():
        sys.path.insert(0, str(potential_startup_script.parent))
        with ExitStack(lambda: sys.path.pop(0)):
            module = importlib.import_module(potential_startup_script.stem)

            execute_func = getattr(module, "Execute", None)
            if execute_func:
                if execute_func(project_dir, tmp_dir, yes=yes) is False:
                    return

    # generate project in temporary directory so we can avoid overwriting files without user approval
    cookiecutter(
        str(project_dir),
        output_dir=str(tmp_dir),
        config_file=str(configuration_filename) if configuration_filename is not None else None,
        replay=replay,
        overwrite_if_exists=True,
        accept_hooks=True,
    )

    _CopyToOutputDir(tmp_dir=tmp_dir, output_dir=output_dir)
    _DisplayPrompts(output_dir=output_dir)


# ----------------------------------------------------------------------
def _CreateManifest(
    generated_dir: Path, manifest_file_path: Optional[Path], write_to_file: bool
) -> dict[str, str]:

    manifest_dict: dict[str, str] = {}
    generated_files: list[Path] = []
    directories: list[Path] = [generated_dir]

    while directories != []:
        dir = directories.pop(0)
        PathEx.EnsureDir(dir)

        for root, dirs, files in os.walk(dir):
            create_path_obj_fn = lambda str_path: Path(os.path.join(root, str_path))
            generated_files += [create_path_obj_fn(file) for file in files]
            directories += [create_path_obj_fn(directory) for directory in dirs]

    # Populate manifest dictionary
    for genfile in generated_files:
        PathEx.EnsureFile(genfile)

        with open(genfile, "rb") as f:
            digest = hashlib.file_digest(f, hashlib.sha256)
            manifest_dict[genfile] = digest.hexdigest()

    # Store manifest dictionary in file if needed
    if write_to_file:
        manifest_file = open(manifest_file_path, "w")
        json.dump(manifest_dict, manifest_file)
        manifest_file.close()

    return manifest_dict


# ----------------------------------------------------------------------
def _CopyToOutputDir(tmp_dir: Path, output_dir: Path) -> None:
    generated_manifest = _CreateManifest(tmp_dir, manifest_file_path=None, write_to_file=False)

    for filepath, hash in generated_manifest.items():
        relative_filepath = PathEx.CreateRelativePath(tmp_dir, Path(filepath))
        output_dir_filepath = output_dir / relative_filepath

        # Check if we are overwriting any modified files
        if output_dir_filepath.is_file():
            with open(output_dir_filepath, "rb") as existing_file:
                existing_file_hash = hashlib.file_digest(existing_file, hashlib.sha256).hexdigest()

            # Changes detected
            if hash != existing_file_hash:
                changed_file_name = str(output_dir_filepath)

                while True:
                    sys.stdout.write(
                        f"\nWould you like to overwrite your changes in {changed_file_name}? [yes/no]: "
                    )
                    overwrite = input().strip().lower()

                    if overwrite in ["yes", "y"]:
                        break

                    if overwrite in ["no", "n"]:
                        shutil.copy2(output_dir_filepath, filepath)
                        break

    # copy temporary directory to final output directory and remove temporary directory
    shutil.copytree(tmp_dir, output_dir, dirs_exist_ok=True, copy_function=shutil.copy2)
    shutil.rmtree(tmp_dir)


# ----------------------------------------------------------------------
def _DisplayPrompts(output_dir: Path) -> None:
    # Ensure yaml file exists and load contents
    prompt_values_file = (
        Path.cwd() / "src" / "PythonProjectBootstrapper" / "PromptPopulateValues.yml"
    )
    PathEx.EnsureFile(prompt_values_file)

    with open(prompt_values_file, "r") as yaml_file:
        _prompt_values = yaml.load(yaml_file, Loader=yaml.Loader)

    # Instructions for post generation
    _prompts: dict[str, str] = {
        "GitHub Personal Access Token for gists": textwrap.dedent(
            f"""\
            In this step, we will create a GitHub Personal Access Token (PAT) that is used to update the gist that stores dynamic build data.

            1. Visit {_prompt_values['github_url']}/settings/tokens?type=beta
            2. Click the "Generate new token" button
            3. Name the token "GitHub Workflow Gist ({_prompt_values['github_project_name']})"
            4. In the Repository access section...
            5. Select "Only select repositories"...
            6. Select "{_prompt_values['github_project_name']}"
            7. In the "Permissions" section...
            8. Press the "Account permissions" dropdown...
            9. Select the "Gists" section...
            10. Click the "Access: No access" dropdown button...
            11. Select "Read and write"
            12. Click the "Generate token" button
            13. Copy the token for use in the next step
            """,
        ),
        "Save the GitHub Personal Access Token for gists": textwrap.dedent(
            f"""\
            In this step, we will save the GitHub PAT we just created as a GitHub Action Secret.

            1. Visit {_prompt_values['github_url']}/{_prompt_values['github_username']}/{_prompt_values['github_project_name']}/settings/secrets/actions
            2. In the "Repository secrets" section...
            3. Click the "New repository secret" button
            4. Enter the values:
                    Name:     GIST_TOKEN
                    Secret:   <paste the token generated in the previous step>
            5. Click the "Add secret" button
            """,
        ),
        "Temporary PyPi Token to Publish Packages": textwrap.dedent(
            f"""\
            In this step, we will create a PyPi token that is used to publish python packages. Note that this token will be scoped to all of your projects on PyPi. Once the package is published for the first time, we will delete this token and create one that is scoped to a single project.

            1. Visit https://pypi.org/manage/account/
            2. Click the "Add API token" button
            3. Enter the values:
                    Token name:    Temporary GitHub Publish Action ({_prompt_values['github_project_name']})
                    Scope:         Entire account (all projects)
            4. Click the "Create token" button
            5. Click the "Copy token" button for use in the next step
            """,
        ),
        "Save the Temporary PyPi Token to Publish Packages": textwrap.dedent(
            f"""\
            In this step, we will save the PyPi token that we just created as a GitHub Action Secret.

            1. Visit {_prompt_values['github_url']}/{_prompt_values['github_username']}/{_prompt_values['github_project_name']}/settings/secrets/actions
            2. In the "Repository secrets" section...
            3. Click the "New repository secret" button
            4. Enter the values:
                    Name:     PYPI_TOKEN
                    Secret:   <paste the token generated in the previous step>
            5. Click the "Add secret" button
            """,
        ),
        "Update GitHub Settings": textwrap.dedent(
            f"""\
            In this step, we will update GitHub settings to allow the creation of git tags during a release.

            1. Visit {_prompt_values['github_url']}/{_prompt_values['github_username']}/{_prompt_values['github_project_name']}/settings/actions
            2. In the "Workflow permissions" section...
            3. Select "Read and write permissions"
            4. Click the "Save" button
            """,
        ),
        "Commit and Push the Repository": textwrap.dedent(
            """\
            In this step, we commit the files generated in git and push the changes to GitHub. Note that these steps assume that the GitHub repository has already been created.

            From a terminal:

            1. Run 'git add --all'
            {windows_command}{commit_step_num}. Run 'git commit -m "🎉 Initial commit"'
            {push_step_num}. Run 'git push'
            """,
        ).format(
            windows_command=(
                "2. Run 'git update-index --chmod=+x Bootstrap.sh'\n" if os.name == "nt" else ""
            ),
            commit_step_num="3" if os.name == "nt" else "2",
            push_step_num="4" if os.name == "nt" else "3",
        ),
        "Verify GitHub Actions": textwrap.dedent(
            f"""\
            In this step, we will verify that the GitHub Action workflows ran successfully.

            1. Visit {_prompt_values['github_url']}/{_prompt_values['github_username']}/{_prompt_values['github_project_name']}/actions
            2. Click on the most recent workflow
            3. Wait for the workflow to complete
            """,
        ),
        "Remove Temporary PyPi Token": textwrap.dedent(
            f"""\
            In this step, we will delete the temporary PyPi token previously created. A new token to replace it will be created in the steps that follow.

            1. Visit https://pypi.org/manage/account/
            2. Find the token named "Temporary GitHub Publish Action ({_prompt_values['github_project_name']})"...
            3. Click the "Options" dropdown button...
            4. Select "Remove token"
            5. In the dialog box that appears...
            6. Enter your password
            7. Click the "Remove API token" button
            """,
        ),
        "Scoped PyPi Token to Publish Packages": textwrap.dedent(
            f"""\
            In this step, we create a new token that is scoped to "{_prompt_values['pypi_project_name']}".

            1. Visit https://pypi.org/manage/account/
            2. Click the "Add API token" button
            3. Enter the values:
                    Token name:    GitHub Publish Action ({_prompt_values['github_project_name']})
                    Scope:         Project: {_prompt_values['pypi_project_name']}
            4. Click the "Create token" button
            5. Click the "Copy token" button for use in the next step
            """,
        ),
        "Save the Scoped PyPi Token to Publish Packages": textwrap.dedent(
            f"""\
            In this step, we will replace the GitHub secret with the PyPi token just created.

            1. Visit {_prompt_values['github_url']}/{_prompt_values['github_username']}/{_prompt_values['github_project_name']}/settings/secrets/actions/PYPI_TOKEN
            2. In the "Value" text window, paste the token generated in the previous step
            3. Click "Update secret"
            """,
        ),
        "Update README.md": textwrap.dedent(
            f"""\
            In this step, we will update the README.md file with information about your project.

            1. Edit README.md
            2. Replace the "TODO" comment in the "Overview" section.
            3. Replace the "TODO" comment in the "How to use {_prompt_values['github_project_name']}" section.
            """,
        ),
    }

    # Display prompts
    border_colors = itertools.cycle(
        ["yellow", "blue", "magenta", "cyan", "green"],
    )

    sys.stdout.write("\n\n")

    for prompt_index, (title, prompt) in enumerate(_prompts.items()):
        print(
            Panel(
                prompt.rstrip(),
                border_style=next(border_colors),
                padding=1,
                title=f"[{prompt_index + 1}/{len(_prompts)}] {title}",
                title_align="left",
            ),
        )

        sys.stdout.write("\nPress <enter> to continue")
        input()
        sys.stdout.write("\n\n")

    # Final prompt
    sys.stdout.write(
        textwrap.dedent(
            """\
            The project has now been bootstrapped!

            To begin development, run these commands:

                1. cd "{output_dir}"
                2. Bootstrap{ext}
                3. {source}{prefix}Activate{ext}
                4. python Build.py pytest


            """,
        ).format(
            output_dir=output_dir,
            ext=".cmd" if os.name == "nt" else ".sh",
            source="source " if os.name != "nt" else "",
            prefix="./" if os.name != "nt" else "",
        ),
    )

    # remove yaml
    prompt_values_file.unlink()


"""
TODO:
- Ensure all paths exist and all calls are safe
- Ensure all directories exist and all calls are safe
- Ensure proper packages are used for proper functions
- Ensure all resources are cleaned up as needed (tmp_dir properly removed, files are closed)
"""


if __name__ == "__main__":
    app()  # pragma: no cover
