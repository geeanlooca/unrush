import json
import subprocess
from dataclasses import dataclass
from enum import StrEnum


class TrackType(StrEnum):
    AUDIO = "audio"
    SUBTITLES = "subtitles"
    VIDEO = "video"


@dataclass
class Trackinfo:
    number: int
    uid: str
    track_type: TrackType
    language: str
    default_track: bool = False
    forced_display: bool = False
    original_language: bool = False


@dataclass
class MKVInfo:
    title: str
    tracks: list[Trackinfo]

    def audio_languages(self) -> list[str]:
        return [track.language for track in self.tracks if track.track_type == "audio"]

    def subtitle_languages(self) -> list[str]:
        return [
            track.language for track in self.tracks if track.track_type == "subtitles"
        ]


def load_movies_json(file: str) -> list[MKVInfo]:
    with open(file) as f:
        data = json.load(f)

    movies = []

    for title, movie_tracks in data.items():
        tracks = []
        for track in movie_tracks:
            tracks.append(Trackinfo(**track))
        movie = MKVInfo(title, tracks)
        movies.append(movie)

    return movies


def get_prefix_width(line: str, delim: str = "+") -> int:
    return len(line.split(delim)[0])


def get_track_info(track_info_lines: list[str]) -> Trackinfo:
    def clean_line(line: str) -> str:
        return line.strip().split("+")[1].strip()

    def key_value(line: str) -> tuple[str, str]:
        clean = clean_line(line)
        parts = clean.split(":")

        if len(parts) < 2:
            return parts[0].strip(), ""

        return parts[0].strip(), parts[1].strip()

    number = 1
    uid = ""
    track_type = ""
    language = ""
    default_track = False
    forced_display = False
    original_language = False

    for line in track_info_lines:
        k, v = key_value(line)
        if k.startswith("Track number"):
            number = int(v.split(" ")[0])
        elif k.startswith("Track UID"):
            uid = v
        elif k.startswith("Track type"):
            track_type = TrackType(v)
        elif k.startswith("Language"):
            language = v
        elif k.startswith('"Default track" flag'):
            default_track = v == "1"
        elif k.startswith('"Forced display" flag'):
            forced_display = v == "1"
        elif k.startswith('"Original language" flag'):
            print(k, v)
            original_language = v == "1"

    return Trackinfo(
        number,
        uid,
        track_type,
        language,
        default_track,
        forced_display,
        original_language,
    )


def extract_track_info_lines(lines: str, start: int) -> list[str]:
    line = lines[start]
    prefix_count = get_prefix_width(line)
    info_prefix = get_prefix_width(lines[start + 1])

    if info_prefix == prefix_count:
        raise ValueError("Unexpected format in track info")

    stop = False
    i = 1
    track_info = []
    while not stop and start + i < len(lines):
        line = lines[start + i]
        prefix = get_prefix_width(line)
        if prefix == info_prefix:
            track_info.append(line)
            i += 1
        else:
            stop = True

    return track_info


def parse_tracks(mkv_info: str) -> list[Trackinfo]:
    lines = list(map(lambda s: s.rstrip(), mkv_info.split("|")))

    track_starts = []
    for i, line in enumerate(lines):
        if line.endswith("+ Track"):
            track_starts.append(i)

    track_info = []
    for start in track_starts:
        info_lines = extract_track_info_lines(lines, start)
        info = get_track_info(info_lines)
        track_info.append(info)

    return track_info


def extract_tracks_information(
    mkv_file: str, print_full_output: bool = False
) -> list[Trackinfo]:
    out = subprocess.check_output(["mkvinfo", mkv_file]).decode("utf-8")
    if print_full_output:
        print(out)

    return parse_tracks(out)
