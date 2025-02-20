import os
import subprocess
from pprint import pprint

from unrush import tracks_editor
from unrush.cli import build_cli, parse_cli_arguments
from unrush.tracks_info import extract_tracks_information


def check_exec() -> bool:
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


def get_mkv_files_in_path(path: str) -> list[os.DirEntry]:
    movie_dirs = [subdir for subdir in os.scandir(path) if subdir.is_dir()]
    mkv_files = []

    for movie_dir in movie_dirs:
        files = [file for file in os.scandir(movie_dir) if file.name.endswith(".mkv")]
        mkv_files.extend(files)

    return mkv_files


def main() -> None:
    cli = build_cli()
    args = parse_cli_arguments(cli)

    if not check_exec():
        print("mkvpropedit or mkvinfo not found in PATH")
        raise SystemExit

    if not os.path.exists(args.path):
        print(f"Path {args.path} does not exist")
        raise SystemExit

    if os.path.isfile(args.path):
        track_info = extract_tracks_information(args.path)
        pprint(track_info)

        editor = tracks_editor.MkvTracksEditor(args.path, tracks_info=track_info)

        editor.set_audio_preferences(["eng", "spa"]).set_subtitle_preferences(
            ["eng", "spa"]
        ).set_banned_languages(["rus", "ru"]).apply()
        raise SystemExit


if __name__ == "__main__":
    main()
