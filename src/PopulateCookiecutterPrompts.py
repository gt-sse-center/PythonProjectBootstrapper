# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Populates multiline cookiecutter.json __prompts__ values."""

import re
import sys
import textwrap

from pathlib import Path
from typing import Match

import rtyaml

from dbrownell_Common import PathEx
from dbrownell_Common import TextwrapEx


# ----------------------------------------------------------------------
# |  Calculate Directories
directories: list[Path] = []

for child in PathEx.EnsureDir(Path(__file__).parent / "PythonProjectBootstrapper").iterdir():
    if child.is_dir():
        directories.append(child)


# ----------------------------------------------------------------------
# |  Process Content
for directory in directories:
    # Read the yaml content
    yaml_filename = directory / "cookiecutter_prompts.yaml"
    if not yaml_filename.is_file():
        continue

    with yaml_filename.open() as f:
        yaml_content = rtyaml.load(f)

    # Read the json content
    json_filename = directory / "cookiecutter.json"
    assert json_filename.is_file(), json_filename

    with json_filename.open() as f:
        json_content = f.read()

    # Replace the content
    # ----------------------------------------------------------------------
    def Replace(
        match: Match,
    ) -> str:
        return TextwrapEx.Indent(
            textwrap.dedent(
                """\
                "__prompts__": {{
                {content}
                }}{trailing_comma}
                """,
            ).format(
                content=TextwrapEx.Indent(
                    ",\n".join(
                        '"{}": "{}"'.format(
                            key,
                            "\n\n{}{}".format(value, "\n\n" if "\n" in value else "")
                            .replace("\n", "\\n")
                            .replace('"', '\\"'),
                        )
                        for key, value in yaml_content.items()
                    ),
                    4,
                ),
                trailing_comma=match.group("trailing_comma") or "",
            ),
            match.group("initial_whitespace"),
        )

    # ----------------------------------------------------------------------

    new_content = re.sub(
        r"""(?#
            initial whitespace              )^(?P<initial_whitespace>[ \t]+)(?#
            begin section                   )[\"']__prompts__[\"']: {\r?\n(?#
            <content>                       ).+?(?#
            end section                     )(?P=initial_whitespace)}(?#
            trailing comma                  )(?P<trailing_comma>,)?\r?\n(?#
        )""",
        Replace,
        json_content,
        flags=re.MULTILINE | re.DOTALL,
    )

    # Write the content (if necessary)
    if new_content != json_content:
        with json_filename.open("w") as f:
            f.write(new_content)

        sys.stdout.write(f"New content has been written to '{json_filename}'.\n")
    else:
        sys.stdout.write(f"'{json_filename}' was not modified.\n")
