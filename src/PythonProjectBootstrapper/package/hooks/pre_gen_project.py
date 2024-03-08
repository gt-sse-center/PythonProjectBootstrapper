# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
errors: list[str] = []

# fmt: off
if "{{ cookiecutter.name }}".startswith("<") and "{{ cookiecutter.name }}".endswith(">"):
    errors.append('name ("{{ cookiecutter.name }}")')
if "{{ cookiecutter.email }}".startswith("<") and "{{ cookiecutter.email }}".endswith(">"):
    errors.append('email ("{{ cookiecutter.email }}")')
if "{{ cookiecutter.project_description }}".startswith("<") and "{{ cookiecutter.project_description }}".endswith(">"):
    errors.append('project_description ("{{ cookiecutter.project_description }}")')
if "{{ cookiecutter.gist_id }}".startswith("<") and "{{ cookiecutter.gist_id }}".endswith(">"):
    errors.append('gist_id ("{{ cookiecutter.gist_id }}")')
if "{{ cookiecutter.github_username }}".startswith("<") and "{{ cookiecutter.github_username }}".endswith(">"):
    errors.append('github_username ("{{ cookiecutter.github_username }}")')
# fmt: on

if errors:
    raise Exception(
        "Required data has not been populated:\n{}".format(
            "\n".join("    - {}".format(e) for e in errors)
        )
    )
