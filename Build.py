# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Build tasks for this python module."""

import sys

from pathlib import Path

import typer

from dbrownell_Common import PathEx
from typer.core import TyperGroup

from dbrownell_DevTools.RepoBuildTools import Python as RepoBuildTools


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
this_dir = PathEx.EnsureDir(Path(__file__).parent)
src_dir = PathEx.EnsureDir(this_dir / "src")
package_dir = PathEx.EnsureDir(src_dir / "PythonProjectBootstrapper")
tests_dir = PathEx.EnsureDir(this_dir / "tests")


# ----------------------------------------------------------------------
Black = RepoBuildTools.BlackFuncFactory(
    this_dir,
    app,
    '--force-exclude "{{ cookiecutter.__empty_dir }}|src/PythonProjectBootstrapper/package/hooks"',
)

Pylint = RepoBuildTools.PylintFuncFactory(
    package_dir,
    app,
    default_min_score=9.5,
)

Pytest = RepoBuildTools.PytestFuncFactory(
    tests_dir,
    package_dir.name,
    app,
    default_min_coverage=70.0,
)

UpdateVersion = RepoBuildTools.UpdateVersionFuncFactory(
    src_dir,
    PathEx.EnsureFile(package_dir / "__init__.py"),
    app,
)

Package = RepoBuildTools.PackageFuncFactory(this_dir, app)
Publish = RepoBuildTools.PublishFuncFactory(this_dir, app)

BuildBinary = RepoBuildTools.BuildBinaryFuncFactory(
    this_dir,
    src_dir / "BuildBinary.py",
    app,
)

CreateDockerImage = RepoBuildTools.CreateDockerImageFuncFactory(this_dir, app)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(app())
