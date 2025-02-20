import argparse
import os
import urllib.parse
from pprint import pprint

import requests
import tracks_info
from dotenv import load_dotenv

load_dotenv()


def remove_year(title: str) -> str:
    # find the last pair of parenthesis and remove it
    start = title.rfind("(")
    end = title.rfind(")")
    if start == -1 or end == -1:
        return title

    return title[:start].strip()


def tmdb_search(title: str, api_key: str) -> dict:
    title = remove_year(title)
    encoded_title = urllib.parse.quote_plus(title)

    url = "https://api.themoviedb.org/3/search/movie?query=" + encoded_title
    url += "&api_key=" + api_key

    print(url)

    response = requests.get(url, params={"api_key": os.environ["TMDB_API_KEY"]})
    if response.status_code != 200:
        raise RuntimeError(f"Error {response.status_code} {response.text} for {title}")

    return response.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to json file containing tracks information")
    args = parser.parse_args()

    api_key = os.environ["TMDB_API_KEY"]

    movies = tracks_info.load_movies_json(args.path)

    for movie in movies:
        print(movie.title, movie.audio_languages())

        try:
            response = tmdb_search(movie.title, api_key)
        except RuntimeError as e:
            print(e)
            continue
        else:
            if response["total_results"] == 0:
                print(f"No results found for {movie.title}")
            else:
                pprint(response)
