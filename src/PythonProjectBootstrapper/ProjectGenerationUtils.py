# ----------------------------------------------------------------------
# |
# |  Copyright (c) 2024 Scientific Software Engineering Center at Georgia Tech
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
import hashlib
import itertools
import os
import sys
from pathlib import Path

from rich import print  # pylint: disable=redefined-builtin
from rich.panel import Panel
import yaml

from dbrownell_Common import PathEx
from PythonProjectBootstrapper import __version__

# The following imports are used in cookiecutter hooks. Import them here to
# ensure that they are frozen when creating binaries,
import shutil  # pylint: disable=unused-import, wrong-import-order
import textwrap  # pylint: disable=unused-import, wrong-import-order


# ----------------------------------------------------------------------
def GenerateFileHash(filepath: Path, hash_fn="sha256") -> str:
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
    manifest_dict: dict[str, str] = {}

    for root, _, files in os.walk(generated_dir):
        root_path = Path(root)

        for file in files:
            full_path = root_path / Path(file)
            rel_path = PathEx.CreateRelativePath(generated_dir, full_path)
            manifest_dict[rel_path.as_posix()] = GenerateFileHash(filepath=full_path)

    return manifest_dict


# ----------------------------------------------------------------------
def ConditionallyRemoveUnchangedTemplateFiles(
    new_manifest_dict: dict[str, str],
    existing_manifest_dict: dict[str, str],
    output_dir: Path,
) -> None:
    # Removes any template files no longer being generated as long as the file was never modified by the user

    # files no longer in template
    removed_template_files: set[str] = set(existing_manifest_dict.keys()) - set(
        new_manifest_dict.keys()
    )

    PathEx.EnsureDir(output_dir)

    # remove files no longer in template if they are unchanged
    for removed_file_rel_path in removed_template_files:
        removed_full_path = output_dir / removed_file_rel_path

        if removed_full_path.is_file():
            current_hash = GenerateFileHash(filepath=removed_full_path)
            original_hash = existing_manifest_dict[removed_file_rel_path]

            if current_hash == original_hash:
                removed_full_path.unlink()


# ----------------------------------------------------------------------
def CopyToOutputDir(
    src_dir: Path,
    dest_dir: Path,
) -> None:
    # Copies all generated files into the output directory and handles the creation/updating of the manifest file

    PathEx.EnsureDir(src_dir)
    PathEx.EnsureDir(dest_dir)

    # existing_manifest will be populated/updated as necessary and saved
    generated_manifest: dict[str, str] = CreateManifest(src_dir)
    existing_manifest: dict[str, str] = {}

    potential_manifest: Path = dest_dir / ".manifest.yml"

    # if this is not our first time generating, remove unwanted template files
    if potential_manifest.is_file():
        with open(potential_manifest, "r") as existing_manifest_file:
            existing_manifest = yaml.load(existing_manifest_file, Loader=yaml.Loader)

        ConditionallyRemoveUnchangedTemplateFiles(
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

            # Changes detected in file and file modified by xser (changes do not stem only from changes in the contents of the template file)

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
                        break

                    # Here, we are copying the file from the output directory to the temporary directory in the case that the user answers "no"
                    # to whether or not they would like to overwrite their changes. This implementation builds the final directory in the temporary directory then copies everything over.
                    # This makes it much easier to copy over generated files since we do not need to case on whether we are copying over a directory or a file (for example if we generated an empty directory)

                    if overwrite in ["no", "n"]:
                        merged_manifest[rel_filepath] = existing_manifest[rel_filepath]
                        shutil.copy2(output_dir_filepath, src_dir / rel_filepath)
                        break
        else:
            merged_manifest[rel_filepath] = generated_hash

    # create and save manifest
    with open(potential_manifest, "w") as manifest_file:
        yaml.dump(merged_manifest, manifest_file)

    # copy temporary directory to final output directory and remove temporary directory
    shutil.copytree(
        src_dir,
        dest_dir,
        dirs_exist_ok=True,
        ignore_dangling_symlinks=True,
        copy_function=shutil.copy,
    )
    shutil.rmtree(src_dir)


# ----------------------------------------------------------------------
def DisplayPrompt(output_dir: Path) -> None:
    PathEx.EnsureDir(output_dir)

    prompt_text_path = PathEx.EnsureFile(output_dir / "prompt_text.yml")

    with open(prompt_text_path, "r") as prompt_file:
        _prompts = yaml.load(prompt_file, Loader=yaml.Loader)

    prompt_text_path.unlink()

    # Display prompts
    border_colors = itertools.cycle(
        ["yellow", "blue", "magenta", "cyan", "green"],
    )

    sys.stdout.write("\n\n")

    for prompt_index, ((_, title), prompt) in enumerate(sorted(_prompts.items())):
        print(
            Panel(
                prompt.rstrip(),
                border_style=next(border_colors),
                padding=1,
                title=f"[{prompt_index + 1}/{len(_prompts)}] {title}",
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
