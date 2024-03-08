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
    package = "package"


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
_version_option = typer.Option("--version", help="Display the current version and exit.")


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
        version: Annotated[bool, _version_option] = False,
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
            version=version,
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
        version: Annotated[bool, _version_option] = False,
    ) -> None:
        _ExecuteOutputDir(
            project,
            output_dir,
            configuration_filename,
            replay=replay,
            yes=yes,
            version=version,
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
    version: bool,
) -> None:
    if version:
        sys.stdout.write(__version__)
        return

    project_dir = PathEx.EnsureDir(_project_root_dir / project.value)

    # Does the project have a startup script? If so, invoke it dynamically.
    potential_startup_script = project_dir / "hooks" / "startup.py"
    if potential_startup_script.is_file():
        sys.path.insert(0, str(potential_startup_script.parent))
        with ExitStack(lambda: sys.path.pop(0)):
            module = importlib.import_module(potential_startup_script.stem)

            execute_func = getattr(module, "Execute", None)
            if execute_func:
                if execute_func(project_dir, output_dir, yes=yes) is False:
                    return

    cookiecutter(
        str(project_dir),
        output_dir=str(output_dir),
        config_file=str(configuration_filename) if configuration_filename is not None else None,
        replay=replay,
        overwrite_if_exists=True,
        accept_hooks=True,
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()  # pragma: no cover
