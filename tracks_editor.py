from __future__ import annotations

from tracks_info import Trackinfo, extract_tracks_information
from typing import Optional
import subprocess


class MkvTracksEditor:

    _exec_name = "mkvpropedit"

    def __init__(self, mkv_file: str, tracks_info: Optional[list[Trackinfo]] = None) -> None:
        self.mkv_file = mkv_file
        self._audio_preference = []
        self._subs_preference = []

        if tracks_info:
            self.tracks = tracks_info
        else:
            self.tracks = extract_tracks_information(mkv_file)

    def set_audio_preferences(self, languages: list[str]) -> MkvTracksEditor:
        return self


    def set_subtitle_preferences(self, languages: list[str]) -> MkvTracksEditor:
        return self



    def _build_track_args(self, track: Trackinfo, default: bool) -> list[str]:
        args = []
        default_str = "1" if default else "0"
        args.append(f"--edit track:{track.number}")
        args.append(f"--set flag-default={default_str}")
        return args

    def _build_audio_args(self) -> list[str]:
        return self._build_args(self._audio_preference, "audio")

    def _build_subs_args(self) -> list[str]:
        return self._build_args(self._subs_preference, "subtitles")

    def _build_args(self, language_preferences: list[str], track_type: str) -> list[str]:
        tracks = [track for track in self.tracks if track.track_type == track_type]
        available_languages = {track.language:track for track in tracks}
        selected_track = tracks[0]

        args = []
        for preference in language_preferences:
            if preference in available_languages:
                selected_track = available_languages[preference]
                print(f"Preference {preference} found, selecting {selected_track=}")
                break

        for track in tracks:
            args.extend(self._build_track_args(track, track == selected_track))

        return args
        
    
    def apply(self) -> None:

        args = []
        args.append(self._exec_name)
        args.append(self.mkv_file)

        audio_args = self._build_audio_args()
        subs_args = self._build_subs_args()

        args.extend(audio_args)
        args.extend(subs_args)

        print(args)

        # subprocess.call(args)


    




