import requests
from config import TMDB_API_KEY

def fetch_genres():
    """
    "Fetches and returns genres list from TMDB"
    #Returns: dict mapping genre_id -> genre_name
    """
    logger.info("Fetching genre list from TMDB")

    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url,params=params) 
    if response.status_code != 200:
        logger.error(f"Failed to fetch generes. Status Code: {response.status_code}")
        return {}
    result = response.json()
    genres_list = result["genres"]
    genre_dict = {}
    for genre in genres_list:
        genre_dict[genre['id']] = genre['name']
    return genre_dict

def fetch_popular_movies(count = 10):
    "Fetch N popular movie id's"
    #Returns: List of movie ID's
    pass
def fetch_movie_details(movie_id):
    "Fetch details of a movie"
    #Returns: dict with title, release_date, budget, etc.
    pass
def fetch_movie_credits (movie_id):
    "Fetch cast and crew of a movie"
    #Returns: dict with cast list, crew list
    pass
