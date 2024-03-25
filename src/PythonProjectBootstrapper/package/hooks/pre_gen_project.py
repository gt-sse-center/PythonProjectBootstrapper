# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
errors: list[str] = []

# fmt: off
if "{{ cookiecutter.name | escape_double_quotes }}".startswith("<") and "{{ cookiecutter.name | escape_double_quotes }}".endswith(">"):
    errors.append('''name ("{{ cookiecutter.name }}")''')
if "{{ cookiecutter.email | escape_double_quotes }}".startswith("<") and "{{ cookiecutter.email | escape_double_quotes }}".endswith(">"):
    errors.append('''email ("{{ cookiecutter.email }}")''')
if "{{ cookiecutter.project_description | escape_double_quotes }}".startswith("<") and "{{ cookiecutter.project_description | escape_double_quotes }}".endswith(">"):
    errors.append('''project_description ("{{ cookiecutter.project_description }}")''')
if "{{ cookiecutter.github_username | escape_double_quotes }}".startswith("<") and "{{ cookiecutter.github_username | escape_double_quotes }}".endswith(">"):
    errors.append('''github_username ("{{ cookiecutter.github_username }}")''')
if "{{ cookiecutter.github_project_name | escape_double_quotes }}".startswith("<") and "{{ cookiecutter.github_project_name | escape_double_quotes }}".endswith(">"):
    errors.append('''github_project_name ("{{ cookiecutter.github_project_name }}")''')
if "{{ cookiecutter.gist_id | escape_double_quotes }}".startswith("<") and "{{ cookiecutter.gist_id | escape_double_quotes }}".endswith(">"):
    errors.append('''gist_id ("{{ cookiecutter.gist_id }}")''')
# fmt: on

if errors:
    raise Exception(
        "Required data has not been populated:\n{}".format(
            "\n".join("    - {}".format(e) for e in errors)
        )
    )
