# ----------------------------------------------------------------------
# SPDX-FileCopyrightText: 2024 Scientific Software Engineering Center <ssec-dev@gatech.edu>
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------
"""Unit tests for Math.py"""

from PythonProjectBootstrapper.Math import *


# ----------------------------------------------------------------------
def test_Add():
    assert Add(1, 20) == 21


# ----------------------------------------------------------------------
def test_Sub():
    assert Sub(1, 20) == -19


# ----------------------------------------------------------------------
def test_Mult():
    assert Mult(2, 15) == 30


# ----------------------------------------------------------------------
def test_Div():
    assert Div(6, 3) == 2
