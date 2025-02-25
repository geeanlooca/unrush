import json
from pprint import pprint
from unrush.tracks_info import Trackinfo, load_movies_json
from unrush.languages import get_language_code

def test_tracks_from_json() -> None:

    data = load_movies_json("tracks.json")
    
    for movie in data:
        print(movie)

        for track in movie.tracks:
            code = get_language_code(track.language)
            print(track.language, '->', code)

    
