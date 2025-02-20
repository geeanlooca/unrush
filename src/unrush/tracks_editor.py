from __future__ import annotations

import subprocess
from typing import Optional

from loguru import logger

from unrush.languages import ORIGINAL_LANGUAGE_KEYWORD, get_language_code
from unrush.tracks_info import Trackinfo, TrackType, extract_tracks_information


class MkvTracksEditor:
    _exec_name = "mkvpropedit"

    def __init__(
        self, mkv_file: str, tracks_info: Optional[list[Trackinfo]] = None
    ) -> None:
        self.mkv_file = mkv_file
        self._audio_preference = []
        self._subs_preference = []
        self._banned_languages = []

        if tracks_info:
            self.tracks = tracks_info
        else:
            self.tracks = extract_tracks_information(mkv_file)

    def set_banned_languages(self, language: str | list[str]) -> MkvTracksEditor:
        """Set the language(s) to disable for audio/subtitles tracks."""
        if isinstance(language, list):
            self._banned_languages = language
        else:
            self._banned_languages.append(language)

        return self

    def set_audio_preferences(self, languages: str | list[str]) -> MkvTracksEditor:
        if isinstance(languages, list):
            self._audio_preference = languages
        else:
            self._audio_preference.append(languages)

        return self

    def set_subtitle_preferences(self, languages: str | list[str]) -> MkvTracksEditor:
        if isinstance(languages, list):
            self._subs_preference = languages
        else:
            self._subs_preference.append(languages)
        return self

    def _build_track_args(self, track: Trackinfo, default: bool) -> list[str]:
        args = []
        default_str = "1" if default else "0"
        args.append("--edit")
        args.append(f"track:{track.number}")
        args.append("--set")
        args.append(f"flag-default={default_str}")
        return args

    def _build_audio_args(self) -> list[str]:
        return self._build_args(self._audio_preference, TrackType.AUDIO)

    def _build_subs_args(self) -> list[str]:
        return self._build_args(self._subs_preference, TrackType.SUBTITLES)

    def _build_args(
        self, language_preferences: list[str], track_type: TrackType
    ) -> list[str]:
        """Goes through the available tracks and selects the default track according to preferences."""

        tracks = [track for track in self.tracks if track.track_type == track_type]
        available_languages = {
            get_language_code(track.language): track for track in tracks
        }

        selected_track = None

        # find original language track
        original_language_track = None
        logger.info(f"Finding original language {track_type} tracks...")
        for track in tracks:
            if track.track_type == track_type and track.original_language:
                original_language_track = track

                logger.info(f"Found {original_language_track} as original track")

                # if there is more than one, just keep the first
                # there could be edge cases to evaluate when they come up
                break

        for preference in language_preferences:
            logger.info(f"Analyzing {preference=}")

            lang_code = get_language_code(preference)

            # if we asked for the original language
            if lang_code == ORIGINAL_LANGUAGE_KEYWORD:
                logger.info("Original language found in preferences...")

                # first check if we have a track marked as default language
                if original_language_track:
                    logger.info(
                        "There is an original language track. Finished search..."
                    )
                    selected_track = original_language_track
                    break
                else:
                    # we have to find out somehow the original language of the movie
                    # I am afraid we need to call some APIs

                    # for the moment, skip it
                    logger.warning(
                        "Can't determine an original language track. Skipping preference..."
                    )
                    continue

            if preference in available_languages:
                selected_track = available_languages[preference]
                logger.info(
                    f"Preference {preference} found, selecting {selected_track=}"
                )
                break

        if selected_track:
            # set the selected track as default, and the others to not default
            logger.info(f"Setting default track to {selected_track}")
            args = []
            for track in tracks:
                args.extend(self._build_track_args(track, track == selected_track))
            return args

        logger.warning("No tracks found for preferred languages.")
        # we couldn't find a preferred language, go on to disabling default tracks
        # for banned languages
        logger.info("Searching for first non-banned language...")
        first_acceptable_track = None
        for track in tracks:
            if track.language not in self._banned_languages:
                logger.info(f"Found {track} to set as default")
                first_acceptable_track = track
                break

        # if we couldn't find a track to set as default, set the first one
        if first_acceptable_track is None:
            first_acceptable_track = tracks[0]
            logger.warning(
                f"Could not find a non-banned language. Setting first track as default: {first_acceptable_track}"
            )

        args = []
        for track in tracks:
            args.extend(self._build_track_args(track, track == first_acceptable_track))

        return args

    def apply(self) -> None:
        args = []
        args.append(self._exec_name)
        args.append(f"{self.mkv_file}")

        audio_args = self._build_audio_args()
        subs_args = self._build_subs_args()

        args.extend(audio_args)
        args.extend(subs_args)

        logger.debug(" ".join(args))

        subprocess.call(args)
