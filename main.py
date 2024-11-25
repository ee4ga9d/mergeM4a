#!/usr/bin/env python3

import argparse
import glob
import os
import time

from pathlib import Path
from pydub import AudioSegment

### NOTE
### MAKE SURE ffmpeg IS INSTALLED (pip install pydub) AND CAN BE RUN CORRECTLY
### ffmpeg -version

description = """
Merges specified m4a files into a single file or if no m4a files are specified,
merges all m4a files in the current directory.
"""

parser = argparse.ArgumentParser(prog=os.path.basename(__file__), description=description)

parser.add_argument("--files", "-f", nargs="+", help="The files to be merged (Merged in the order of input).")
parser.add_argument("--dir", "-d", nargs=1, help="The directory that contains the files to be merged \
                                                 (Instead of specifying individual files).")
parser.add_argument("--sort", "-s", nargs="*", help="Sort input files before merge.")
parser.add_argument("--output", "-o", nargs=1, help="Output path for the merged m4a file.")

args = parser.parse_args()



if __name__ == "__main__":
    files = args.files
    directory = None if args.dir == None else str((args.dir)[0])
    sort = True if args.sort != None else False
    output = None if args.output == None else str((args.output)[0])

    if directory != None:
        if not os.path.exists(directory):
            raise Exception(f"Directory {directory} does not exist.")

        if not directory.endswith("/"):
            directory = directory + "/"

        files = glob.glob(directory + "*.m4a")

        if len(files) == 0:
            print(f"No m4a files in {directory} directory.")
            exit()

        ans = str(input(f"You sure you want to merge {len(files)} m4a files in the current directory? (y/n) "))
        if ans.upper() != "Y":
            exit()
    elif files == None: # No files selected
        files = glob.glob("*.m4a")

        if len(files) == 0:
            print("No m4a files in the current directory.")
            exit()

        ans = str(input(f"You sure you want to merge {len(files)} m4a files in the current directory? (y/n) "))
        if ans.upper() != "Y":
            exit()

    if sort:
        files = sorted(files)

    if output == None:
        output = "merged_m4a_files.m4a"
    else:
        if not output.endswith(".m4a"):
            raise Exception(f"'{output}' does not end with '.m4a'.")
        try:
            Path(os.path.dirname(output)).mkdir(parents=True, exist_ok=True)
        except Exception:
            raise Exception("Could not create output path.")

    print("Merging, please wait...")
    timer = time.perf_counter() # Elapsed time timer

    merged = AudioSegment.empty()
    fConcat = list()
    for f in files:
        name = AudioSegment.from_m4a(f)
        fConcat.extend([name])

    for f in fConcat:
        merged += f

    merged.export(output, format="m4a")

    print(f"Elapsed time to merge m4a files: {time.perf_counter() - timer}")