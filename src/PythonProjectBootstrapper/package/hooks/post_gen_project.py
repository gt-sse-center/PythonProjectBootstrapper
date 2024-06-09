# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
import os
import shutil
import textwrap
import yaml

from pathlib import Path

from dbrownell_Common import PathEx

# This filename should be the same as the filename defined in ../../ProjectGenerationUtils.py
# Ideally we would be able to assert that these two variables have the same filename, but we encounter errors when importing
# the variable due to how cookiecutter changes the working directory for the post-gen hook
prompt_filename = "prompt_text.yml"


# ----------------------------------------------------------------------
def SavePrompts() -> None:
    # Instructions for post generation
    #
    # By not displaying the prompts right away, we allow the integration of a DoneManager
    # so we can let the user know when the cookiecutter generation is done and before them seeing all the prompts
    #
    prompts: dict[str, str] = {}

    prompts["GitHub Personal Access Token for gists"] = textwrap.dedent(
        """\
        In this step, we will create a GitHub Personal Access Token (PAT) that is used to update the gist that stores dynamic build data.

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
    )

    prompts["Save the GitHub Personal Access Token for gists"] = textwrap.dedent(
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
    )

    prompts["Temporary PyPi Token to Publish Packages"] = textwrap.dedent(
        """\
        In this step, we will create a PyPi token that is used to publish python packages. Note that this token will be scoped to all of your projects on PyPi. Once the package is published for the first time, we will delete this token and create one that is scoped to a single project.

        1. Visit https://pypi.org/manage/account/
        2. Click the "Add API token" button
        3. Enter the values:
                Token name:    Temporary GitHub Publish Action ({{ cookiecutter.github_project_name }})
                Scope:         Entire account (all projects)
        4. Click the "Create token" button
        5. Click the "Copy token" button for use in the next step
        """,
    )

    prompts["Save the Temporary PyPi Token to Publish Packages"] = textwrap.dedent(
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
    )

    prompts["Update GitHub Settings"] = textwrap.dedent(
        """\
        In this step, we will update GitHub settings to allow the creation of git tags during a release.

        1. Visit {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/settings/actions
        2. In the "Workflow permissions" section...
        3. Select "Read and write permissions"
        4. Click the "Save" button
        """,
    )

{% if cookiecutter.minisign_public_key != 'none' %}
    prompts["Save the Minisign Private Key"] = textwrap.dedent(
        f"""\
        In this step, we will save the Minisign private key as a GitHub Action Secret.

        1. Open 'key.pri' in a text editor.
        2. Copy the contents of the file.
        3. Visit {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/settings/secrets/actions
        4. In the "Repository secrets" section...
        5. Click the "New repository secret" button
        6. Enter the values:
                Name:     MINISIGN_PRIVATE_KEY
                Secret:   <paste the contents of key.pri copied in step #2>
        7. Click the "Save" button
        8. Save 'key.pri' in a safe place.
        """,
    )
{% endif %}

    prompts["Commit and Push the Repository"] = textwrap.dedent(
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
    )

    prompts["Verify GitHub Actions"] = textwrap.dedent(
        """\
        In this step, we will verify that the GitHub Action workflows ran successfully.

        1. Visit {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/actions
        2. Click on the most recent workflow
        3. Wait for the workflow to complete
        """,
    )

    prompts["Remove Temporary PyPi Token"] = textwrap.dedent(
        """\
        In this step, we will delete the temporary PyPi token previously created. A new token to replace it will be created in the steps that follow.

        1. Visit https://pypi.org/manage/account/
        2. Find the token named "Temporary GitHub Publish Action ({{ cookiecutter.github_project_name }})"...
        3. Click the "Options" dropdown button...
        4. Select "Remove token"
        5. In the dialog box that appears...
        6. Enter your password
        7. Click the "Remove API token" button
        """,
    )

    prompts["Scoped PyPi Token to Publish Packages"] = textwrap.dedent(
        """\
        In this step, we create a new token that is scoped to "{{ cookiecutter.pypi_project_name }}".

        1. Visit https://pypi.org/manage/account/
        2. Click the "Add API token" button
        3. Enter the values:
                Token name:    GitHub Publish Action ({{ cookiecutter.github_project_name }})
                Scope:         Project: {{ cookiecutter.pypi_project_name }}
        4. Click the "Create token" button
        5. Click the "Copy token" button for use in the next step
        """,
    )

    prompts["Save the Scoped PyPi Token to Publish Packages"] = textwrap.dedent(
        """\
        In this step, we will replace the GitHub secret with the PyPi token just created.

        1. Visit {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/settings/secrets/actions/PYPI_TOKEN
        2. In the "Value" text window, paste the token generated in the previous step
        3. Click "Update secret"
        """,
    )

    prompts["Update README.md"] = textwrap.dedent(
        """\
        In this step, we will update the README.md file with information about your project.

        1. Edit README.md
        2. Replace the "TODO" comment in the "Overview" section.
        3. Replace the "TODO" comment in the "How to use {{ cookiecutter.github_project_name }}" section.
        """,
    )

{% if cookiecutter.openssf_best_practices_badge_id != "none" %}
    prompts["Create the OpenSSF Best Practices Badge"] = textwrap.dedent(
        """\
        In this step, we will populate information on www.bestpractices.dev that is used to display
        the badge on our README.md file.

        1. Visit https://www.bestpractices.dev/
        2. Click the "Get Your Badge Now!" button.
        3. In the lower form, provide these values:
                What is the URL for the project home page?
                    {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}
                What is the URL for the version control repository?
                    {{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}
        4. Click the "Submit URL" button.
        5. Search for these options and set them to the following values:

                Basics
                    \[interact]: Met
                    \[contribution_requirements]: Met ({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/CONTRIBUTING.md)
                    \[english]: Met

                Change Control
                    \[repo_interim]: Met
                    \[version_unique]: Met
                    \[version_semver]: Met
                    \[version_tags]: Met
                    \[release_notes]: Met ({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/releases/latest)

                Reporting
                    \[report_process]: Met ({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/CONTRIBUTING.md)
                    \[report_tracker]: Met
                    \[report_responses]: Met
                    \[report_archive]: Met ({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/issues)
                    \[vulnerability_report_process]: Met ({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/SECURITY.md)
                    \[vulnerability_report_private]: Met ({{ cookiecutter.github_url }}/{{ cookiecutter.github_username }}/{{ cookiecutter.github_project_name }}/blob/main/SECURITY.md)

                Quality
                    \[build]: Met
                    \[build_common_tools]: Met
                    \[build_floss_tools]: Met
                    \[test]: Met
                    \[test_invocation]: Met
                    \[test_most]: Met
                    \[test_continuous_integration]: Met
                    \[test_policy]: Met
                    \[tests_are_added]: Met
                    \[tests_documented_added]: Met
                    \[warnings]: Met
                    \[warnings_fixed]: Met
                    \[warnings_strict]: Met

                Analysis
                    \[static_analysis]: Met (pylint, CodeQL)
                    \[static_analysis_common_vulnerabilities]: Met
                    \[static_analysis_often]: Met
                    \[dynamic_analysis]: Met
                    \[dynamic_analysis_unsafe]: N/A

           These changes will result in a score of 63% (at the time this documentation was written). The remaining fields rely on documentation specific to your project
           or developer behavior based on your interaction with the package (fix critical vulnerabilities within 60 days, etc.).

        6. Click on the "Submit (and exit)" button.
        7. Copy the unique id of your project from the bestpractices.dev URL for use in the next step.

            https://www.bestpractices.dev/en/projects/12345
                                                      ^^^^^
                                                      This is the unique id of your project
        """,
    )

    prompts["Save the OpenSSF Best Practices Badge ID"] = textwrap.dedent(
        """\
        In this step, we will update README.md with the OpenSSF Best Practices Badge ID.

        1. Edit 'README.md'.
        2. Search for '__openssf_badge_id__' and replace all instances with the badge id copied in the previous step.
        3. Save 'README.md'.
        """,
    )

    prompts["Commit and Push the OpenSSF Best Practices Badge ID Changes"] = textwrap.dedent(
        """\
        1. Run 'git add --all'
        2. Run 'git commit -m "🎉 Updated README.md with OpenSSF Best Practices Badge ID"'
        3. Run 'git push'
        """,
    )

{% endif %}

    with open(prompt_filename, "w") as prompt_file:
        # Modify the keys to include an index to ensure that the prompts are displayed in the
        # correct order after being read from the yaml file created here.
        yaml.dump(list(prompts.items()), prompt_file)


# ----------------------------------------------------------------------
def UpdateBootstrapExecutionPermissions():
    bootstrap_path = Path("./Bootstrap.sh")

    PathEx.EnsureFile(bootstrap_path)
    status = bootstrap_path.stat()
    bootstrap_path.chmod(status.st_mode | 0o700)


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
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
UpdateLicenseFile()
SavePrompts()
UpdateBootstrapExecutionPermissions()
