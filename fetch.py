import os
import shutil
import requests

from dotenv import load_dotenv

from generate_html import generate_html

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'
LANGUAGE = 'fr-FR'

MOVIES_FOLDER = r'C:\Users\Steve\Downloads\[Vidz]'


def get_genre_dict():
    genre_url = f"{BASE_URL}/genre/movie/list"
    params = {
        'api_key': API_KEY,
        'language': LANGUAGE
    }
    response = requests.get(genre_url, params=params)
    if response.status_code == 200:
        genres = response.json().get('genres')
        return {genre['id']: genre['name'] for genre in genres}
    return {}


def search_movie(movie_name):
    search_url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': movie_name,
        'language': LANGUAGE
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0]
    return None


def download_poster(movie, save_path):
    poster_path = movie.get('poster_path')
    if poster_path:
        poster_url = f"{IMAGE_BASE_URL}{poster_path}"
        response = requests.get(poster_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)


def save_synopsis(movie, save_path):
    overview = movie.get('overview')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(overview)


def move_movie_file(movie_file, movie_folder):
    original_path = os.path.join(MOVIES_FOLDER, movie_file)
    new_path = os.path.join(movie_folder, movie_file)
    shutil.move(original_path, new_path)
    print(f"Movie {movie_file} OK.")


def main():

    films_folder = os.path.join(MOVIES_FOLDER, '[Films]')

    genre_dict = get_genre_dict()

    for movie_file in os.listdir(MOVIES_FOLDER):
        if movie_file.endswith(('.mp4', '.avi', '.mkv')):
            movie_name = os.path.splitext(movie_file)[0]
            movie = search_movie(movie_name)
            if movie:
                genre_ids = movie.get('genre_ids')
                genre_name = 'Unknown'
                if genre_ids:
                    genre_id = genre_ids[0]
                    genre_name = genre_dict.get(genre_id, 'Unknown')

                genre_folder = os.path.join(films_folder, genre_name)
                os.makedirs(genre_folder, exist_ok=True)

                movie_folder = os.path.join(genre_folder, movie_name)
                os.makedirs(movie_folder, exist_ok=True)

                poster_save_path = os.path.join(movie_folder,
                                                f"{movie_name}.jpg")
                synopsis_save_path = os.path.join(movie_folder,
                                                  f"{movie_name}.txt")

                download_poster(movie, poster_save_path)
                save_synopsis(movie, synopsis_save_path)
                move_movie_file(movie_file, movie_folder)
            else:
                print(f"Nothing found for {movie_name}.")

    generate_html()


if __name__ == "__main__":
    main()
