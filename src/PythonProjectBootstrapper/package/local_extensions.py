# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
from cookiecutter.utils import simple_filter


# ----------------------------------------------------------------------
@simple_filter
def pypi_string(value):
    return value.lower().replace("_", "-")


# ----------------------------------------------------------------------
@simple_filter
def escape_double_quotes(value):
    return value.replace('"', '\\"')
