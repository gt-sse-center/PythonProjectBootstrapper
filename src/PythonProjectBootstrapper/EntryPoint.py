# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""This file serves as an example of how to create scripts that can be invoked from the command line once the package is installed."""

import importlib
import sys

from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

import typer
import yaml

from typer.core import TyperGroup  # type: ignore [import-untyped]

from cookiecutter.main import cookiecutter
from dbrownell_Common.ContextlibEx import ExitStack
from dbrownell_Common import PathEx
from dbrownell_Common.Streams.DoneManager import DoneManager

from PythonProjectBootstrapper import __version__
from PythonProjectBootstrapper.ProjectGenerationUtils import (
    CopyToOutputDir,
    DisplayPrompt,
    DisplayModifications,
    prompt_filename,
)

# from PythonProjectBootstrapper.package.hooks.post_gen_project import prompt_filename
# prompt_filename = "prompt_text.yml"

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
# Dynamically create the ProjectType enumeration based on the directories found in this dir.


def _CreateProjectType():
    project_types: list[str] = []

    if getattr(sys, "frozen", False):
        template_dir = Path(sys.executable).parent / "lib" / "PythonProjectBootstrapper"
    else:
        template_dir = Path(__file__).parent

    PathEx.EnsureDir(template_dir)

    for file_item in template_dir.iterdir():
        if not file_item.is_dir():
            continue

        project_types.append(file_item.name)

    assert project_types
    return Enum("ProjectType", {project_type: project_type for project_type in project_types})


ProjectType = _CreateProjectType()
del _CreateProjectType


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

_skip_prompts_option = typer.Option(
    "--skip-prompts",
    help="Do not display prompts after generating content.",
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
        skip_prompts: Annotated[bool, _skip_prompts_option] = False,
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
            skip_prompts=skip_prompts,
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
        skip_prompts: Annotated[bool, _skip_prompts_option] = False,
        version: Annotated[bool, _version_option] = False,  # pylint: disable=unused-argument
    ) -> None:
        _ExecuteOutputDir(
            project,
            output_dir,
            configuration_filename,
            replay=replay,
            yes=yes,
            skip_prompts=skip_prompts,
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
    skip_prompts: bool,
) -> None:
    if not (output_dir / ".git").is_dir():
        raise Exception(f"{output_dir} is not a git repository.")

    project_dir = PathEx.EnsureDir(_project_root_dir / project.value)

    # create temporary directory for cookiecutter output
    tmp_dir = PathEx.CreateTempDirectory()

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

    with DoneManager.Create(sys.stdout, "\nGenerating content..."):
        # generate project in temporary directory so we can avoid overwriting files without user approval
        cookiecutter(
            str(project_dir),
            output_dir=str(tmp_dir),
            config_file=str(configuration_filename) if configuration_filename is not None else None,
            replay=replay,
            overwrite_if_exists=True,
            accept_hooks=True,
        )

    modifications = CopyToOutputDir(src_dir=tmp_dir, dest_dir=output_dir)

    prompt_text_path = PathEx.EnsureFile(output_dir / prompt_filename)

    # The approach below with reading in the prompt file regardless of whether or not we will display the prompts is not ideal but has to be
    # done since we need to remove the prompt_text file before running DisplayPrompt(). This is because prompt_text.yml is currently stored in the output directory
    # and the instructions being printed out during the execution of DisplayPrompt() would result in that file being check into the git repo.
    # Alternate solutions would be to only read in the file in the 'if' block below, but, this would result in us needing the call 'unlink()' in both the 'if' block and a separate 'else' block.
    # This issue also prevents us from using a cleaner solution such as ExitStack()
    with open(prompt_text_path, "r") as prompt_file:
        prompts = yaml.load(prompt_file, Loader=yaml.Loader)

    prompt_text_path.unlink()

    DisplayModifications(modifications=modifications)

    if not skip_prompts:
        DisplayPrompt(output_dir=output_dir, prompts=prompts)


if __name__ == "__main__":
    app()  # pragma: no cover
