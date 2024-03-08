# ----------------------------------------------------------------------
#
# Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# Distributed under the MIT License.
#
# ----------------------------------------------------------------------
import itertools
import os
import shutil
import sys
import textwrap

from pathlib import Path

from dbrownell_Common import PathEx
from rich import print  # pylint: disable=redefined-builtin
from rich.panel import Panel


# ----------------------------------------------------------------------
_prompts: dict[str, str] = {
    "GitHub Personal Access Token for gists": textwrap.dedent(
        """\
        In this step, we will create a GitHub Personal Access Token (PAT) that is used to
        update the gist that stores dynamic build data.

        1. Visit {{ cookiecutter.github_url }}/settings/tokens?type=beta
        2. Click the "Generate new token" button
        3. Name the token "GitHub Workflow Gist ({{ cookiecutter.github_project_name }})"
        4. In the Repository access section...
        5. Select "Only select repositories"...
        6. Select "{{ cookiecutter.github_project_name }}"
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
        """\
        In this step, we will save the GitHub PAT we just created as a GitHub Action Secret.

        1. Visit {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/settings/secrets/actions
        2. In the "Repository secrets" section...
        3. Click the "New repository secret" button
        4. Enter the values:
                Name:     GIST_TOKEN
                Secret:   <paste the token generated in the previous step>
        5. Click the "Add secret" button
        """,
    ),
    "Temporary PyPi Token to Publish Packages": textwrap.dedent(
        """\
        In this step, we will create a PyPi token that is used to publish python packages. Note
        that this token will be scoped to all of your projects on PyPi. Once the package is
        published for the first time, we will delete this token and create one that is scoped to
        a single project.

        1. Visit https://pypi.org/manage/account/
        2. Click the "Add API token" button
        3. Enter the values:
                Token name:    "Temporary GitHub Publish Action ({{ cookiecutter.github_project_name }})"
                Scope:         "Entire account (all projects)"
        4. Click the "Create token" button
        5. Click the "Copy token" button for use in the next step
        """,
    ),
    "Save the Temporary PyPi Token to Publish Packages": textwrap.dedent(
        """\
        In this step, we will save the PyPi token that we just created as a GitHub Action Secret.

        1. Visit {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/settings/secrets/actions
        2. In the "Repository secrets" section...
        3. Click the "New repository secret" button
        4. Enter the values:
                Name:     PYPI_TOKEN
                Secret:   <paste the token generated in the previous step>
        5. Click the "Add secret" button
        """,
    ),
    "Commit and Push the Repository": textwrap.dedent(
        """\
        In this step, we commit the files generated in git, push the changes in GitHub, and verify
        that the GitHub Actions workflow ran successfully.

        Commit and Push the Changes
        ---------------------------
        Note that these steps assume that the GitHub repository has already been created.

        From a terminal:

        1. Run 'git add -all'
        {windows_command}{commit_step_num}. Run 'git commit -m "🎉 Initial commit"'
        {push_step_num}. Run 'git push'

        Verify the GitHub Actions Workflow
        ----------------------------------
        1. Visit {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions
        2. Click on the most recent workflow
        3. Wait for the workflow to complete
        """,
    ).format(
        windows_command=(
            "2. git update-index --chmod=+x Bootstrap.sh\n" if os.name == "nt" else ""
        ),
        commit_step_num="3" if os.name == "nt" else "2",
        push_step_num="4" if os.name == "nt" else "3",
    ),
    "Remove Temporary PyPi Token": textwrap.dedent(
        """\
        In this step, we will delete the temporary PyPi token previously created. A new token to replace
        it will be created in the steps that follow.

        1. Visit https://pypi.org/manage/account/
        2. Find the token named "Temporary GitHub Publish Action ({{ cookiecutter.github_project_name }})"...
        3. Click the "Options" dropdown button...
        4. Select "Remove token"
        5. In the dialog box that appears...
        6. Enter your password
        7. Click the "Remove API token" button
        """,
    ),
    "Scoped PyPi Token to Publish Packages": textwrap.dedent(
        """\
        In this step, we create a new token that is scoped to "{{ cookiecutter.pypi_project_name }}".

        1. Visit https://pypi.org/manage/account/
        2. Click the "Add API token" button
        3. Enter the values:
                Token name:    "GitHub Publish Action ({{ cookiecutter.github_project_name }})"
                Scope:         "Project: {{ cookiecutter.pypi_project_name }}"
        4. Click the "Create token" button
        5. Click the "Copy token" button for use in the next step
        """,
    ),
    "Save the Scoped PyPi Token to Publish Packages": textwrap.dedent(
        """\
        In this step, we will replace the GitHub secret with the PyPi token just created.

        1. Visit {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/settings/secrets/actions/PYPI_TOKEN
        2. In the "Value" text window, paste the token generated in the previous step
        3. Click "Update secret"
        """,
    ),
    "Update README.md": textwrap.dedent(
        """\
        In this step, we will update the README.md file with information about your project.

        1. Edit README.md
        2. Replace the "TODO" comment in the "Overview" section.
        3. Replace the "TODO" comment in the "How to use {{ cookiecutter.github_project_name }}" section.
        """,
    ),
}


# ----------------------------------------------------------------------
def UpdateLicenseFile():
    this_dir = Path.cwd()
    licenses_dir = PathEx.EnsureDir(this_dir / "Licenses")

    license_name = "{{ cookiecutter.license }}"

    if license_name == "BSL-1.0":
        source_file = licenses_dir / "BST-1.0_LICENSE_1_0.txt"
    else:
        source_file = licenses_dir / "{}_LICENSE.txt".format(license_name)

    PathEx.EnsureFile(source_file)
    dest_file = this_dir / source_file.name[len(license_name) + 1 :]

    shutil.copy(source_file, dest_file)
    shutil.rmtree(licenses_dir)


# ----------------------------------------------------------------------
def DisplayPrompts():
    border_colors = itertools.cycle(
        ["red", "green", "yellow", "blue", "magenta", "cyan"],
    )

    for prompt_index, (title, prompt) in enumerate(_prompts.items()):
        print(
            Panel(
                prompt.strip(),
                border_style=next(border_colors),
                padding=1,
                title=f"[{prompt_index + 1}/{len(_prompts)}] {title}",
                title_align="left",
            ),
        )

        sys.stdout.write("\nPress <enter> to continue")
        input()
        sys.stdout.write("\n\n")


# ----------------------------------------------------------------------
def FinalPrompt():
    sys.stdout.write(
        textwrap.dedent(
            """\
            The project has now been bootstrapped!

            To begin development, run these commands:

                1. cd "{current_dir}"
                2. Bootstrap{ext}
                3. {source}{prefix}Activate{ext}
                4. python Build.py pytest


            """,
        ).format(
            current_dir=Path.cwd(),
            ext=".cmd" if os.name == "nt" else ".sh",
            source="source " if os.name != "nt" else "",
            prefix="./" if os.name != "nt" else "",
        ),
    )


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
UpdateLicenseFile()
DisplayPrompts()
FinalPrompt()
