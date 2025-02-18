import argparse
import subprocess
from pprint import pprint
from tracks_info import extract_tracks_information
import tracks_editor
import dataclasses
import os
import tqdm
import json


MKV_FILE = (
    r"/media/red1/Movies/Fallen Angels (1995)/Fallen Angels (1995) Bluray-1080p.mkv"
)
WRONG_FILE = "/does/not/exist.mkv"
ARCHIVE_PATH = r"/media/red1/Movies"


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def check_exec() -> bool:
    ret1 = subprocess.call(
        ["mkvpropedit", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    ret2 = subprocess.call(
        ["mkvinfo", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return ret1 == 0 and ret2 == 0


def get_mkv_files_in_path(path: str) -> list[os.DirEntry]:
    movie_dirs = [subdir for subdir in os.scandir(path) if subdir.is_dir()]
    mkv_files = []

    for movie_dir in movie_dirs:
        files = [file for file in os.scandir(movie_dir) if file.name.endswith(".mkv")]
        mkv_files.extend(files)

    return mkv_files


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract information from mkv files")
    parser.add_argument("path", help="Path to the mkv file or media directory")
    args = parser.parse_args()

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
        ).apply()
        raise SystemExit

    mkv_files = get_mkv_files_in_path(args.path)
    bar = tqdm.tqdm(mkv_files)
    tracks = {}

    for dir in bar:
        bar.set_description(f"Processing {dir.name}")
        tracks[dir.name] = extract_tracks_information(dir.path)
        pprint(tracks[dir.name])

        [
            track for track in tracks[dir.name] if track.track_type == "subtitles"
        ]
        [
            track for track in tracks[dir.name] if track.track_type == "audio"
        ]


if __name__ == "__main__":
    main()
