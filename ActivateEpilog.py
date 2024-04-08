# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
# pylint: disable=missing-module-docstring

import json
import os
import sys

from pathlib import Path

with (Path(os.environ["PYTHON_BOOTSTRAPPER_GENERATED_DIR"]) / "bootstrap_flags.json").open() as f:
    flags = json.load(f)

if flags:
    sys.stdout.write("\nBootstrapped with {}.\n".format(", ".join(f"'{flag}'" for flag in flags)))
