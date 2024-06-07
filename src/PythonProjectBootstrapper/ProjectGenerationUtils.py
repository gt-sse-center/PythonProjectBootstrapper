# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Util functions used during project generation"""

from dataclasses import dataclass, field
import hashlib
import itertools
import os
from stat import S_IWUSR
import sys
from pathlib import Path

from rich import print  # pylint: disable=redefined-builtin
from rich.panel import Panel
from rich.text import Text
import yaml

from dbrownell_Common import PathEx
from PythonProjectBootstrapper import __version__

# The following imports are used in cookiecutter hooks. Import them here to
# ensure that they are frozen when creating binaries,
import shutil  # pylint: disable=unused-import, wrong-import-order
import textwrap  # pylint: disable=unused-import, wrong-import-order

# This filename should be the same as the filename defined in package/hooks/post_gen_project.py
# Ideally we would be able to assert that these two variables have the same filename, but we encounter errors when importing
# the variable due to how cookiecutter changes the working directory for the post-gen hook
prompt_filename: str = "prompt_text.yml"


@dataclass(frozen=True)
class CopyToOutputDirResult:
    """
    Object containing information about file modifications triggered by CopyToOutputDir() function call
    """

    deleted_files: list[str] = field(default_factory=list)
    added_files: list[str] = field(default_factory=list)
    overwritten_files: list[str] = field(default_factory=list)
    modified_template_files: list[str] = field(default_factory=list)


# ----------------------------------------------------------------------
def GenerateFileHash(filepath: Path, hash_fn="sha256") -> str:
    """
    Returns a hash value for a given file

    Args:
        filepath (Path): file to hash
        hash_fn (str, optional): Hash algorithm to use. Choose from
                    ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
                      'blake2b', 'blake2s', 'sha3_224', 'sha3_256', 'sha3_384',
                      'sha3_512', 'shake_128', 'shake_256']

            Defaults to "sha256".

    Returns:
        str: hash value for file
    """
    PathEx.EnsureFile(filepath)

    hasher = hashlib.new(hash_fn)
    with open(filepath, "rb") as file:
        while True:
            chunk = file.read(8192)
            if not chunk:
                break

            hasher.update(chunk)

    hash_value = hasher.hexdigest()
    return hash_value


# ----------------------------------------------------------------------
def CreateManifest(generated_dir: Path) -> dict[str, str]:
    """
    Create manifest dictionary for a given path. Note the values in the returned dictionary represent the hash value of the file when it was originally generated or last overwritten by a project generation.
    These values will not necessarily reflect the hash of the current state of the file (for example if a user modifies a file but does not want to overwrite their changes)

    Args:
        generated_dir (Path): Path to create manifest of

    Returns:
        dict[str, str]: Dictionary mapping filepaths as strings to hash values representing the file contents
    """
    manifest_dict: dict[str, str] = {}

    for root, _, files in os.walk(generated_dir):
        root_path = Path(root)

        for file in files:
            full_path = root_path / Path(file)
            rel_path = PathEx.CreateRelativePath(generated_dir, full_path)
            manifest_dict[rel_path.as_posix()] = GenerateFileHash(filepath=full_path)

    return manifest_dict


# ----------------------------------------------------------------------
def _ChangeManifestWritePermissions(manifest_filepath: Path, read_only: bool) -> None:
    """
    Change write permissions for manifest file

    Args:
        manifest_filepath (Path): Filepath to manifest file
        read_only (bool): If true, set to read-only. If false, allow writing to file
    """
    PathEx.EnsureFile(manifest_filepath)
    status = manifest_filepath.stat()

    if read_only:
        manifest_filepath.chmod(status.st_mode & ~S_IWUSR)
    else:
        manifest_filepath.chmod(status.st_mode | S_IWUSR)

    status = manifest_filepath.stat()


# ----------------------------------------------------------------------
def ConditionallyRemoveUnchangedTemplateFiles(
    new_manifest_dict: dict[str, str],
    existing_manifest_dict: dict[str, str],
    output_dir: Path,
) -> list[str]:
    """
    Remove any template files no longer being generated as long as the file was never modified by the user.

    Args:
        new_manifest_dict (dict[str, str]): Manifest dictionary created that reflects contents on the newly generated cookiecutter project
        existing_manifest_dict (dict[str, str]): Manifest dictionary that reflects contents of the final output directory
        output_dir (Path): output directory path

    Returns:
        list[str]: Sorted list of file paths that were removed
    """

    # files no longer in template
    removed_template_files: set[str] = set(existing_manifest_dict.keys()) - set(
        new_manifest_dict.keys()
    )

    deleted_files: list[str] = []

    PathEx.EnsureDir(output_dir)

    # remove files no longer in template if they are unchanged
    for removed_file_rel_path in removed_template_files:
        removed_full_path = output_dir / removed_file_rel_path

        if removed_full_path.is_file():
            current_hash = GenerateFileHash(filepath=removed_full_path)
            original_hash = existing_manifest_dict[removed_file_rel_path]

            if current_hash == original_hash:
                deleted_files.append(removed_full_path.as_posix())
                removed_full_path.unlink()

    return sorted(deleted_files)


# ----------------------------------------------------------------------
def CopyToOutputDir(
    src_dir: Path,
    dest_dir: Path,
) -> CopyToOutputDirResult:
    """
    Copy contents to output directory following the following rules:

    1. If a file in the src_dir does not exist in the dest_dir, copy it over
    2. If a file in the src_dir exists in the dest_dir, copy it over only if the file in the dest_dir has never been modified by the user OR after prompted, they approve overwriting their changes

    Additionally, write the final manifest to "<dest_dir>/.manifest.yml". This manifest should reflect the state of the output directory after the project generation has completed

    Args:
        src_dir (Path): path to source dir
        dest_dir (Path): path to final output directory

    Returns:
        CopyToOutputDir: data object containing a lists of files deleted, added, overwritten, and modified due to template changes
    """

    PathEx.EnsureDir(src_dir)
    PathEx.EnsureDir(dest_dir)

    prompt_file = src_dir / prompt_filename
    if prompt_file.is_file():
        shutil.move(prompt_file, dest_dir)
        PathEx.EnsureFile(dest_dir / prompt_filename)

    # existing_manifest will be populated/updated as necessary and saved
    generated_manifest: dict[str, str] = CreateManifest(src_dir)
    existing_manifest: dict[str, str] = {}

    overwritten_files: list[str] = []
    added_files: list[str] = []
    modified_template_files: list[str] = []
    unchanged_files_deleted: list[str] = []

    potential_manifest: Path = dest_dir / ".manifest.yml"

    # if this is not our first time generating, remove unwanted template files
    if potential_manifest.is_file():
        with open(potential_manifest, "r") as existing_manifest_file:
            existing_manifest = yaml.load(existing_manifest_file, Loader=yaml.Loader)

        # Removing <prompt_filename> from the manifest for backward compatability.
        # Previous iterations of PythonProjectBootstrapper saved "<prompt_filename>"" in the manifest file when it should not have been there
        # (the manifest was created using the contents of the temporary directory and "<prompt_filename>"" was there but was removed from the output directory)
        # This results in "<prompt_filename>" being listed as a removed file since it exists in the manifest but not in the output directory
        if prompt_filename in existing_manifest.keys():
            del existing_manifest[prompt_filename]

        unchanged_files_deleted = ConditionallyRemoveUnchangedTemplateFiles(
            new_manifest_dict=generated_manifest,
            existing_manifest_dict=existing_manifest,
            output_dir=dest_dir,
        )

    merged_manifest = dict(existing_manifest)
    merged_manifest.update(generated_manifest)

    # Ask user if they would like to overwrite their changes if any conflicts detected
    for rel_filepath, generated_hash in generated_manifest.items():
        output_dir_filepath: Path = dest_dir / rel_filepath

        if output_dir_filepath.is_file():
            current_file_hash: str = GenerateFileHash(filepath=output_dir_filepath)

            # Changes detected in file and file modified by user (changes do not stem only from changes in the contents of the template file)
            if rel_filepath in existing_manifest.keys() and current_file_hash not in (
                generated_hash,
                existing_manifest[rel_filepath],
            ):
                while True:
                    sys.stdout.write(
                        f"\nWould you like to overwrite your changes in {str(output_dir_filepath)}? [yes/no]: "
                    )
                    overwrite = input().strip().lower()

                    if overwrite in ["yes", "y"]:
                        overwritten_files.append(output_dir_filepath.as_posix())
                        break

                    # Here, we are copying the file from the output directory to the temporary directory in the case that the user answers "no"
                    # to whether or not they would like to overwrite their changes. This implementation builds the final directory in the temporary directory then copies everything over.
                    # This makes it much easier to copy over generated files since we do not need to case on whether we are copying over a directory or a file

                    if overwrite in ["no", "n"]:
                        merged_manifest[rel_filepath] = existing_manifest[rel_filepath]
                        shutil.copy2(output_dir_filepath, src_dir / rel_filepath)
                        break

            # Looking at a template file, contents this generation are different, and contents were untouched by user
            elif rel_filepath in existing_manifest.keys() and (
                current_file_hash != generated_hash
                and current_file_hash == existing_manifest[rel_filepath]
            ):
                modified_template_files.append(output_dir_filepath.as_posix())
        else:
            added_files.append(output_dir_filepath.as_posix())
            merged_manifest[rel_filepath] = generated_hash

    # create and save manifest
    yaml_comments = textwrap.dedent(
        """\
        #############################################################################################################
        # This file is used by PythonProjectBootstrapper (https://github.com/gt-sse-center/PythonProjectBootstrapper)
        # to determine whether changes have been made to any files in the project. These values are saved in case the
        # project is regenerated so we can avoid overwriting any user changes. Please do not change the contents :)
        #############################################################################################################

        """,
    )

    if potential_manifest.is_file():
        _ChangeManifestWritePermissions(manifest_filepath=potential_manifest, read_only=False)

    with open(potential_manifest, "w") as manifest_file:
        manifest_file.write(yaml_comments)
        yaml.dump(merged_manifest, manifest_file)

    _ChangeManifestWritePermissions(manifest_filepath=potential_manifest, read_only=True)

    # copy temporary directory to final output directory and remove temporary directory
    shutil.copytree(
        src_dir,
        dest_dir,
        dirs_exist_ok=True,
        ignore_dangling_symlinks=True,
        copy_function=shutil.copy,
    )
    shutil.rmtree(src_dir)

    deleted_files: list[str] = list(set(unchanged_files_deleted) - set(added_files))

    return CopyToOutputDirResult(
        deleted_files=sorted(deleted_files),
        added_files=sorted(added_files),
        overwritten_files=sorted(overwritten_files),
        modified_template_files=sorted(modified_template_files),
    )


# ----------------------------------------------------------------------
def DisplayModifications(modifications: CopyToOutputDirResult) -> None:
    """
    Print out the changes in the output directory that were triggered by this project generation

    Args:
        modifications (CopyToOutputDirResult): Object containing information about files deleted, added, overwritten, and modified
    """

    sys.stdout.write("\n\n")

    labels = ["Deleted Files", "Added Files", "Overwritten Files", "Modified Template Files"]
    changes = [
        modifications.deleted_files,
        modifications.added_files,
        modifications.overwritten_files,
        modifications.modified_template_files,
    ]

    display_mods = Text("")

    for label, mods in zip(labels, changes):
        display_mods.append(("\n" + label + "\n"), style="bold")

        for file_changed in mods:
            display_mods.append(" - " + file_changed + "\n")

    print(
        Panel(
            display_mods,
            border_style="green",
            padding=1,
            title="Output Directory Modifications",
            title_align="left",
        )
    )


# ----------------------------------------------------------------------
def DisplayPrompt(output_dir: Path, prompts: list[tuple[str, str]]) -> None:
    """
    Display prompts/instructions after project generation

    Args:
        output_dir (Path): Path of final output directory
        prompts (dict[tuple[int, str], str]): Dictionary mapping (Prompt Number, Label) -> Prompt Text
    """
    PathEx.EnsureDir(output_dir)

    sys.stdout.write("\n\n")

    # Display prompts
    border_colors = itertools.cycle(
        ["yellow", "blue", "magenta", "cyan", "green"],
    )

    # Print out saved prompts
    for prompt_index, (title, prompt) in enumerate(prompts):
        print(
            Panel(
                prompt.rstrip(),
                border_style=next(border_colors),
                padding=1,
                title=f"[{prompt_index + 1}/{len(prompts)}] {title}",
                title_align="left",
            ),
        )

        sys.stdout.write("\nPress <enter> to continue")
        input()
        sys.stdout.write("\n\n")

    # Final prompt
    sys.stdout.write(
        textwrap.dedent(
            """\
            The project has now been bootstrapped!

            To begin development, run these commands:

                1. cd "{output_dir}"
                2. Bootstrap{ext}
                3. {source}{prefix}Activate{ext}
                4. python Build.py pytest


            """,
        ).format(
            output_dir=output_dir,
            ext=".cmd" if os.name == "nt" else ".sh",
            source="source " if os.name != "nt" else "",
            prefix="./" if os.name != "nt" else "",
        ),
    )
