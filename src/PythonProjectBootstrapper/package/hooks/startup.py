# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
import sys
import textwrap
import uuid

from pathlib import Path

from rich import print  # pylint: disable=redefined-builtin
from rich.panel import Panel


# ----------------------------------------------------------------------
def Execute(
    template_dir: Path,  # pylint: disable=unused-argument
    output_dir: Path,
    *,
    yes: bool,
) -> bool:
    # Ensure that the panel content is easy to read and modify here, but also leverages Panel's word
    # wrapping capabilities.
    panel_content = textwrap.dedent(
        """\
        This project creates a Python package hosted on GitHub that uploads a Python wheel to PyPi.
        It also includes opt-in functionality to create docker images that ensure the exact
        reproducibility of all commits (which is especially useful for scientific software).

        If you continue, you will be asked a series of questions about your project and given
        step-by-step instructions on how to set up your project so that it works with 3rd party
        solutions (GitHub, PyPi, etc.).

        The entire process should take about 10 minutes to complete.
        """,
    )

    paragraph_sentinel = str(uuid.uuid4())

    panel_content = (
        panel_content.replace("\n\n", paragraph_sentinel)
        .replace("\n", " ")
        .replace(paragraph_sentinel, "\n\n")
    )

    sys.stdout.write("\n")

    print(
        Panel(
            panel_content.rstrip(),
            border_style="green",
            padding=1,
            title="Python Package",
        ),
    )

    if not yes:
        while True:
            sys.stdout.write("\nEnter 'yes' to continue or 'no' to exit: ")
            result = input().strip().lower()

            if result in ["yes", "y"]:
                break

            if result in ["no", "n"]:
                return False

    if not (output_dir / ".git").is_dir():
        raise Exception(f"{output_dir} is not a git repository.")

    return True
