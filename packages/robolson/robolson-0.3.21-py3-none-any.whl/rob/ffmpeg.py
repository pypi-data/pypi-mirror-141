import glob
import pathlib
import os
import time
import asyncio
import argparse
import logging
import sys
import subprocess
import multiprocessing
import time

import pydub
import rich
from pydub.utils import mediainfo

# Create the parser
my_parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    allow_abbrev=True,
    add_help=True,
    description="Concatenates audio files using ffmpeg.",
    epilog="(C) Rob",
)

# Add the arguments
my_parser.add_argument(
    "-f",
    "--filetype",
    metavar="filetype",
    nargs=1,
    default=".mp3",
    choices=[".mp3", ".wav", ".ogg"],
    action="store",
    type=str,
    help="the filetype to concatenate, e.g., '.mp3'",
)

my_parser.add_argument(
    "-p",
    "--path",
    metavar="path",
    nargs=1,
    default=".",
    action="store",
    type=str,
    help="the path to files to be concatted",
)

my_parser.add_argument(
    "-c",
    "--cpus",
    metavar="cpus",
    nargs=1,
    default=[1],
    action="store",
    type=int,
    help="the number of processor cores to utilize",
)

my_parser.add_argument('-o',
                       '--overwrite',
                       action='store_true',
                       help='force ffmpeg to overwrite existing files')

my_parser.add_argument('-i',
                       '--interactive',
                       action='store_true',
                       help='supply arguments manually via prompt')

# Execute the parse_args() method
_ARGS = my_parser.parse_args()

_PROMPT = "rob.ffmpeg> "

_PATH = _ARGS.path
_FILETYPE = _ARGS.filetype
_OVERWRITE = _ARGS.overwrite
_CPUS = _ARGS.cpus


def spin_up(folder):
    """Spin up an ffmpeg process in target folder.

    Args:
        folder: path to folder that contains audio files
    """

    os.chdir(folder)


    mp3s = glob.glob(f"*{_FILETYPE}")
    mp3s = [elem for elem in mp3s if elem[0] != '~']


    if not mp3s:
        return

    bit_rate = mediainfo(mp3s[0])['bit_rate']

    if _OVERWRITE:
        try:
            os.remove(f"{pathlib.Path(mp3s[0]).stem}.m4b")
        except FileNotFoundError as e:
            pass

    # Merge audio files
    combined = pydub.AudioSegment.empty()

    match _FILETYPE:
        case ".mp3":
            for file in mp3s:
                combined += pydub.AudioSegment.from_mp3(file)

        case ".wav":
            for file in mp3s:
                combined += pydub.AudioSegment.from_wav(file)

        case ".ogg":
            for file in mp3s:
                combined += pydub.AudioSegment.from_ogg(file)

    _temp_file = f"~{pathlib.Path(mp3s[0]).stem}-full{_FILETYPE}"

    combined.export(_temp_file, tags={"test":"TEST"}, bitrate=bit_rate)
    # End of Merge audio files

    count = 0
    while not pathlib.Path(_temp_file).exists():
        count += 1
        print(f"Merged file not found.  Retry {count}/5 in 10s.", end="\r", flush=True)
        if count > 6:
            print("Merged file not found.  Exiting...")
            exit(1)
        time.sleep(10)

    rich.print(f"\n[green]Merged file ({_temp_file}) created.[/green]\n")

    # Convert audio files
    command = [
        "ffmpeg",
        "-i",
        # f"concat:{concated}",
        f"~{pathlib.Path(mp3s[0]).stem}-full{_FILETYPE}",
        "-movflags", # Carry metadata over
        "use_metadata_tags",
        "-c:a", # audio cocec
        "aac",
        "-b:a", # bitrate
        "64k",
        "-c:v",
        "copy",
        f"{pathlib.Path(mp3s[0]).stem}.m4b",
    ]

    rich.print("\nRunning the following command:\n[yellow]" + " ".join(command) + "[/yellow]\n")
    subprocess.run(command, shell=True)
    # End of Convert audio files

def interact():
    global _PATH
    global _FILETYPE
    global _OVERWRITE
    global _CPUS

    choice = input(f"Enter path to work on [default: {_PATH}].\n{_PROMPT}")
    if choice:
        _PATH = choice

    choice = input(f"Automatically overwrite existing files [default: {_OVERWRITE}]? y/n\n{_PROMPT}")
    if choice in ['y', "Y", 'yes', "YES"]:
        _OVERWRITE = True
    elif not choice:
        pass
    else:
        _OVERWRITE = False

    choice = input(f"Which file type to work on [default: {_FILETYPE}]?\n 1.) *.mp3\n 2.) *.wav\n 3.) *.ogg\n{_PROMPT}")
    match choice:
        case "1" | "*.mp3" | ".mp3" | "mp3":
            _FILETYPE = ".mp3"

        case "2" | "*.wav" | ".wav" | "wav":
            _FILETYPE = ".wav"

        case "3" | "*.ogg" | ".ogg" | "ogg":
            _FILETYPE = ".ogg"

        case _:
            pass

    choice = input(f"How many CPU cores to use [default: {_CPUS[0]}]?\n{_PROMPT}")
    while True:
        try:
            if not choice:
                break
            else:
                _CPUS = [int(choice)]
                break
        except (TypeError, ValueError):
            rich.print(f"[red]Must supply an integer.[/red]\nHow many CPU cores to use [default: {_CPUS[0]}]?\n")
            choice = input(f"{_PROMPT}")

def main():
    folders = set()

    if _ARGS.interactive:
        interact()

    os.chdir(_PATH)
    for file in glob.glob(f"**/*{_FILETYPE}", recursive=True):
        target = pathlib.Path(file).absolute()
        folders.add(target.parent)

    folders = sorted(list(folders))

    input(
        f"Executing on \n * "
        + "\n * ".join([str(folder) for folder in folders])
        + ". \nOk?"
    )


    with multiprocessing.Pool(_CPUS[0]) as pool:
        pool.map_async(spin_up, folders).get()

if __name__ == "__main__":
    main()
