import os
import pathlib
import subprocess


def get_mkv_files_in_path(path: str) -> list[os.DirEntry]:
    movie_dirs = [subdir for subdir in os.scandir(path) if subdir.is_dir()]
    mkv_files = []

    for movie_dir in movie_dirs:
        files = [file for file in os.scandir(movie_dir) if file.name.endswith(".mkv")]
        mkv_files.extend(files)

    return mkv_files


def check_required_executables() -> bool:
    """Returns true if the executables for 'mkvpropedit' and 'mkvinfo' are found in PATH."""
    try:
        ret1 = subprocess.call(
            ["mkvpropedit", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        return False

    try:
        ret2 = subprocess.call(
            ["mkvinfo", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        return False

    return ret1 == 0 and ret2 == 0


def find_all_mkv_files(paths: str | list[str], recursive: bool = False) -> list[str]:
    """Return the list of mkv files contained in paths list, optionally recursively."""

    _paths = [paths] if isinstance(paths, str) else paths

    filepaths: list[str] = []
    for path in _paths:
        if os.path.isfile(path) and path.casefold().endswith(".mkv"):
            filepaths.append(pathlib.Path(path))
        elif os.path.isdir(path):
            path = pathlib.Path(path)
            if recursive:
                files = path.rglob("*.mkv")
            else:
                files = path.glob("*.mkv")
            filepaths.extend(list(files))

    return filepaths
