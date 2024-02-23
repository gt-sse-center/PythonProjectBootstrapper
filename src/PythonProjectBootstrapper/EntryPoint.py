# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""This file serves as an example of how to create scripts that can be invoked from the command line once the package is installed."""

import sys

from pathlib import Path
from typing import Annotated, Optional

import typer

from typer.core import TyperGroup  # type: ignore [import-untyped]

from cookiecutter.main import cookiecutter
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
_version_option = typer.Option("--version", help="Display the current version and exit.")


# ----------------------------------------------------------------------
# The cookiecutter project dir must be accessed in different ways depending on whether the code is:
#   - running from source
#   - running from a pip installation
#   - running as a frozen binary.
#
if getattr(sys, "frozen", False):
    _project_dir = (
        Path(sys.executable).parent / "lib" / "PythonProjectBootstrapper" / "python_project"
    )

    # This is admittedly very strange. cookiecutter apparently uses sys.argv[0] to invoke
    # python hooks. Within a binary, sys.argv[0] will point back to this file. So, create
    # functionality that invokes cookiecutter when passed a directory and executes python code
    # from a file when invoked as a hook.

    # ----------------------------------------------------------------------
    @app.command()
    def FrozenExecute(
        output_dir: Annotated[
            Path, typer.Argument(resolve_path=True, help="Directory to populate.")
        ],
        configuration_filename: Annotated[Optional[Path], _configuration_filename_option] = None,
        replay: Annotated[bool, _replay_option] = False,
        version: Annotated[bool, _version_option] = False,
    ) -> None:
        if output_dir.is_file():
            with output_dir.open() as f:
                content = f.read()

            exec(content)  # pylint: disable=exec-used
            return

        _ExecuteOutputDir(
            output_dir,
            configuration_filename,
            replay=replay,
            version=version,
        )

    # ----------------------------------------------------------------------

else:
    _project_dir = Path(__file__).parent / "python_project"

    # ----------------------------------------------------------------------
    @app.command()
    def StandardExecute(
        output_dir: Annotated[
            Path, typer.Argument(file_okay=False, resolve_path=True, help="Directory to populate.")
        ],
        configuration_filename: Annotated[Optional[Path], _configuration_filename_option] = None,
        replay: Annotated[bool, _replay_option] = False,
        version: Annotated[bool, _version_option] = False,
    ) -> None:
        _ExecuteOutputDir(
            output_dir,
            configuration_filename,
            replay=replay,
            version=version,
        )


PathEx.EnsureDir(_project_dir)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _ExecuteOutputDir(
    output_dir: Path,
    configuration_filename: Optional[Path],
    *,
    replay: bool,
    version: bool,
) -> None:
    if version:
        sys.stdout.write(__version__)
        return

    cookiecutter(
        str(_project_dir),
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
