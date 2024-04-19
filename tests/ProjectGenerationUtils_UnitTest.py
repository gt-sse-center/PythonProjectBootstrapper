# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
import pytest
import pyfakefs.fake_filesystem as fake_fs
import os
import itertools
from unittest.mock import patch

from pathlib import Path, PurePath, PurePosixPath

from dbrownell_Common import PathEx
from PythonProjectBootstrapper.ProjectGenerationUtils import (
    _CreateManifest,
    _ConditionallyRemoveUnchangedTemplateFiles,
    _CopyToOutputDir,
    _GenerateFileHash,
    HASH_ALG,
)


# ----------------------------------------------------------------------
def dirs_equal(dir1: Path, dir2: Path) -> bool:
    # Check that 2 given directories have the same structure and files have the same contents EXCEPT for any manifest.yml files

    generated_files1: list[Path] = []
    generated_files2: list[Path] = []

    for root, _, files in os.walk(dir1):
        if ".manifest.yml" in files:
            files.remove(".manifest.yml")

        generated_files1 += [Path(root) / Path(file) for file in files]

    for root, _, files in os.walk(dir2):
        if ".manifest.yml" in files:
            files.remove(".manifest.yml")

        generated_files2 += [Path(root) / Path(file) for file in files]

    contents1 = [_GenerateFileHash(file, hash_fn=HASH_ALG) for file in generated_files1]
    contents2 = [_GenerateFileHash(file, hash_fn=HASH_ALG) for file in generated_files2]
    rel_gen_1 = [PathEx.CreateRelativePath(dir1, file) for file in generated_files1]
    rel_gen_2 = [PathEx.CreateRelativePath(dir2, file) for file in generated_files2]

    assert len(rel_gen_1) == len(contents1)
    assert len(contents2) == len(rel_gen_2)

    return list(zip(rel_gen_1, contents1)) == list(zip(rel_gen_2, contents2))


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "os_type", [fake_fs.OSType.WINDOWS, fake_fs.OSType.MACOS, fake_fs.OSType.LINUX]
)
def test_CreateManifest(fs, os_type):
    # Test for the following:
    #   - All created files and only files exist in the manifest
    #   - Files with same content have the same hash
    #   - Files with different contents have different hash

    fs.os = os_type

    files = [("test/file1", "abc"), ("test/file1repeat", "abc"), ("test/file2", "def")]

    for filepath, content in files:
        fs.create_file(filepath, contents=content)

    fs.create_dir("/emptydir")

    test_manifest = _CreateManifest(generated_dir=Path("/"))

    file_names = set(file[0] for file in files)

    assert set(test_manifest.keys()) == file_names
    assert test_manifest["test/file1"] == test_manifest["test/file1repeat"]
    assert test_manifest["test/file1"] != test_manifest["test/file2"]


# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "os_type", [fake_fs.OSType.WINDOWS, fake_fs.OSType.MACOS, fake_fs.OSType.LINUX]
)
def test_ConditionalRemoveTemplateFiles_no_changed_files(fs, os_type):
    fs.os = os_type

    output_dir_path = Path("output_dir")
    new_output_path = Path("new_output_dir")

    # test that template files are removed if the user has made no changes to the file contents

    files = [("testFile", "abc"), ("testFile2", "def")]

    for file, content in files:
        fs.create_file(output_dir_path / file, contents=content)
        fs.create_file(new_output_path / file, contents=content)

    fs.create_file(output_dir_path / "testFile3", contents="hello")

    existing_manifest = _CreateManifest(generated_dir=output_dir_path)
    new_manifest = _CreateManifest(generated_dir=new_output_path)

    _ConditionallyRemoveUnchangedTemplateFiles(
        new_manifest_dict=new_manifest,
        existing_manifest_dict=existing_manifest,
        output_dir=Path("output_dir"),
    )

    assert dirs_equal(output_dir_path, new_output_path)


# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "os_type", [fake_fs.OSType.WINDOWS, fake_fs.OSType.MACOS, fake_fs.OSType.LINUX]
)
def testConditionalRemoveTemplateFiles_files_changed(fs, os_type):
    fs.os = os_type

    output_dir_path = Path("output_dir")
    new_output_path = Path("new_output_dir")
    expected_output_dir = Path("expected_dir")

    files = [("testFile", "abc"), ("testFile2", "def")]

    for file, content in files:
        fs.create_file(output_dir_path / file, contents=content)
        fs.create_file(new_output_path / file, contents=content)
        fs.create_file(expected_output_dir / file, contents=content)

    file_to_change = fs.create_file(output_dir_path / "testFile3", contents="hello")
    fs.create_file(expected_output_dir / "testFile3", contents="hi")

    existing_manifest = _CreateManifest(generated_dir=output_dir_path)
    file_to_change.set_contents("hi")

    new_manifest = _CreateManifest(generated_dir=new_output_path)

    _ConditionallyRemoveUnchangedTemplateFiles(
        new_manifest_dict=new_manifest,
        existing_manifest_dict=existing_manifest,
        output_dir=output_dir_path,
    )

    assert dirs_equal(output_dir_path, expected_output_dir)


# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "os_type, overwrite",
    list(
        itertools.product(
            [fake_fs.OSType.WINDOWS, fake_fs.OSType.MACOS, fake_fs.OSType.LINUX], ["y", "n"]
        )
    ),
)
def test_CopyToOutputDir_overwritePrompt(fs, os_type, overwrite):
    fs.os = os_type

    src = Path("src")
    src2 = Path("src2")
    dest = Path("dest")

    files1 = [("testFile", "abc"), ("testFile2", "def"), ("testFile3", "hello")]
    files2 = [("testFile", "abc"), ("testFile2", "def"), ("testFile3", "hi")]

    for filepath, content in files1:
        fs.create_file(src / filepath, contents=content)
        fs.create_file(src2 / filepath, contents=content)

    fs.create_dir(dest)

    _CopyToOutputDir(src_dir=src, dest_dir=dest)

    fs.get_object(str(dest / "testFile3")).set_contents(contents="hi")

    with patch("builtins.input", lambda *args: overwrite):
        _CopyToOutputDir(src_dir=src2, dest_dir=dest)

    correct_output = files1 if overwrite == "y" else files2

    for path, content in correct_output:
        PathEx.EnsureExists(dest / path)

        with open(dest / path, "r") as destfile:
            assert content == destfile.read()

    PathEx.EnsureExists(dest / ".manifest.yml")


# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "os_type", [fake_fs.OSType.WINDOWS, fake_fs.OSType.MACOS, fake_fs.OSType.LINUX]
)
def test_CopyToOutputDir_no_prompt(fs, os_type):
    # Test for the following:
    #   - All created files and directories are copied into the dest
    #   - All contents of files are the same in src and dest
    fs.os = os_type

    files = [(Path("test/file1"), "abc"), (Path("test/file2"), "def")]
    emptydir_path = Path("emptydir")

    src = Path("src")
    dest = Path("dest")
    expected = Path("expected")

    for filepath, content in files:
        fs.create_file(src / filepath, contents=content)
        fs.create_file(expected / filepath, contents=content)

    fs.create_dir(src / emptydir_path)
    fs.create_dir(expected / emptydir_path)

    fs.create_dir(dest)

    _CopyToOutputDir(src_dir=src, dest_dir=dest)

    assert dirs_equal(expected, dest)
    PathEx.EnsureExists(dest / ".manifest.yml")
