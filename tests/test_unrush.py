from unrush.languages import get_language_code
from unrush.tracks_info import load_movies_json


def test_tracks_from_json() -> None:
    data = load_movies_json("tracks.json")

    for movie in data:
        print(movie)

        for track in movie.tracks:
            code = get_language_code(track.language)
            print(track.language, "->", code)
