import os

import pathlib

def get_avg_files(output_directory: os.PathLike, glob: str = "*_avg.nc", sort: bool = True) -> list[pathlib.Path]
    """Find and sort all the average files in  a directory."""
    avg_files = list(pathlib.Path(output_directory).glob(glob))
    if sort:
        avg_files.sort()
    return avg_files
