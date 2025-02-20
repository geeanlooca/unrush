from argparse import ArgumentParser

import tqdm

from unrush import tracks_editor
from unrush.cli import build_cli, parse_cli_arguments
from unrush.languages import get_language_code, normalize_language_list
from unrush.tracks_info import extract_tracks_information
from unrush.utils import (
    check_required_executables,
    find_all_mkv_files,
)


def export_language_tags() -> None:
    parser = ArgumentParser()
    parser.add_argument("path", nargs="+", action="extend")
    parser.add_argument("--recursive", action="store_true", default=False)

    args = parser.parse_args()

    if not check_required_executables():
        print("mkvpropedit or mkvinfo not found in PATH")
        raise SystemExit

    mkv_files = find_all_mkv_files(args.path, recursive=args.recursive)

    languages = []
    for file in mkv_files:
        tracks = extract_tracks_information(str(file))

        for track in tracks:
            languages.append(track.language)

    for lang in languages:
        try:
            lang_code = get_language_code(lang)
            print(f"{lang} -> {lang_code}")
        except Exception as e:
            print(f"Error for {lang}: {e}")


def unrush() -> None:
    cli = build_cli()
    args = parse_cli_arguments(cli)

    print(args)

    if not check_required_executables():
        print("mkvpropedit or mkvinfo not found in PATH")
        raise SystemExit

    mkv_files = find_all_mkv_files(args.path, recursive=args.recursive)

    audio_prefs = normalize_language_list(args.audio_preferences)
    sub_prefs = normalize_language_list(args.sub_preferences)
    ban = normalize_language_list(args.ban)

    print(f"Preferred audio languages: {audio_prefs}")
    print(f"Preferred subtitle languages: {sub_prefs}")
    print(f"Banned languages: {ban}")

    for file in tqdm.tqdm(mkv_files):
        track_info = extract_tracks_information(str(file))
        editor = tracks_editor.MkvTracksEditor(str(file), tracks_info=track_info)

        editor.set_audio_preferences(audio_prefs).set_subtitle_preferences(
            sub_prefs
        ).set_banned_languages(ban).apply()


if __name__ == "__main__":
    unrush()
