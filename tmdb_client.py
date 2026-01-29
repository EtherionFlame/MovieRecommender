import requests
import math
from config import TMDB_API_KEY
from logger import setup_logger


logger = setup_logger(__name__)

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
    logger.info(f"Successfully fetched {len(genre_dict)} genres")

    return genre_dict

def fetch_popular_movies(count = 20):
    """
    Fetch N popular movie IDs from TMDB
    
    Args:
        count: Number of movie IDs to return (default 10)
    
    Returns:
        list: List of movie IDs (integers)
    """
    logger.info(f"Fetching {count} popular movie IDs")
    pages_needed = math.ceil(count / 20)
    movie_ids=[]
    for pages in range(1, pages_needed+1):
        url = "https://api.themoviedb.org/3/movie/popular"
        params = {"api_key": TMDB_API_KEY, "page": pages}
        response = requests.get(url,params=params) 
        if response.status_code != 200:
            logger.error(f"Failed to fetch popular movies page {pages}. Status code: {response.status_code}")
            continue  # Skip this page, try next one
        data=response.json()
        movie_list = data['results']
        for movie in movie_list:
            movie_ids.append(movie['id'])
    movie_ids = movie_ids[:count]
    logger.info(f"Successfully fetched {len(movie_ids)} movie IDs")

    return movie_ids


def fetch_movie_details(movie_id):
    """
    Fetch details for a single movie
    
    Args:
        movie_id: TMDB movie ID
    
    Returns:
        dict: Movie data formatted for Neo4j insertion, or None if failed
        
        Example return:
        {
            'tmdb_id': 1084242,
            'title': 'Zootopia 2',
            'release_year': 2025,
            'rating': 7.604,
            'budget': 150000000,  # or None if 0
            'revenue': 1744338246,  # or None if 0
            'overview': '...',
            'poster_url': 'https://...',
            'genres': [16, 35, 12, 10751, 9648],  # Just IDs
            'studios': [{'id': 6125, 'name': 'Walt Disney Animation Studios'}]
        }
    """
    logger.info(f"Fetching details for movie ID {movie_id}")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}
    movie = {}
    response = requests.get(url, params=params)
    if response.status_code != 200:
            logger.error(f"Failed to fetch popular movies page {movie_id}. Status code: {response.status_code}")
            return None
    data=response.json()
    if data.get('release_date'):
        release_year = int(data['release_date'].split('-')[0])
    else:
        release_year=None
    movie['tmdb_id'] = data.get('id')
    budget = data.get('budget')
    if budget == 0:
        budget = None
    movie['budget']=budget
    revenue = data.get('revenue')
    if revenue == 0:
        revenue = None
    movie['revenue']= revenue
    movie['title'] = data.get('title')
    movie['rating'] = data.get('vote_average')
    poster_path = data.get('poster_path')
    if poster_path:
        poster_path="https://image.tmdb.org/t/p/w500"+poster_path
        movie['poster_url'] = poster_path 
    else:
        movie['poster_url'] = None
    movie['overview']=data.get('overview')
    movie['release_year'] = release_year
    studios=[]
    for company in data.get('production_companies', []):
        studio = {
        'id': company['id'],
        'name': company['name']
    }
        studios.append(studio)
    movie['studios']=studios
    genre_ids = []
    for genre in data.get('genres', []):
        genre_ids.append(genre['id'])

    movie['genres'] = genre_ids
    logger.info(f"Successfully fetched details for '{movie['title']}'")
    return movie

def fetch_movie_credits(movie_id, max_cast=10):
    """
    Fetch cast and crew (directors) for a movie
    
    Args:
        movie_id: TMDB movie ID
        max_cast: Maximum number of cast members to return (default 10)
    
    Returns:
        dict with 'cast' and 'directors' lists, or None if failed
        
        Example return:
        {
            'cast': [
                {
                    'tmdb_id': 819,
                    'name': 'Edward Norton',
                    'profile_url': 'https://...',
                    'character': 'Narrator',
                    'order': 0
                },
                ...
            ],
            'directors': [
                {
                    'tmdb_id': 7467,
                    'name': 'David Fincher',
                    'profile_url': 'https://...'
                }
            ]
        }
    """
    logger.info(f"Fetching credits for movie ID {movie_id}")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
            logger.error(f"Failed to fetch movies{movie_id}. Status code: {response.status_code}")
            return None
    data=response.json()
    movie_credits={}
    cast = []
    for actor in data['cast'][:max_cast]:
        profile_path = actor.get('profile_path')
        if profile_path:
            profile_url = f"https://image.tmdb.org/t/p/w500{profile_path}"
        else:
            profile_url = None
    
        cast.append({
        'tmdb_id': actor['id'],
        'name': actor['name'],
        'profile_url': profile_url,
        'character': actor.get('character', 'Unknown'),  # Some have no character
        'order': actor.get('order', 999)  # Some missing order
        })
    directors = []
    for person in data.get('crew', []):
        if person.get('job') == 'Director':
            profile_path = person.get('profile_path')
            if profile_path:  # ← Add this
                profile_url = f"https://image.tmdb.org/t/p/w500{profile_path}"
            else:
                profile_url = None
            
            directors.append({
                'tmdb_id': person['id'],
                'name': person['name'],
                'profile_url': profile_url
            })
            if not directors:
                logger.warning(f"No director found for movie {movie_id}")
    movie_credits['cast']=cast
    movie_credits['directors']=directors
    return movie_credits
    # TODO 2: Make request
    
    # TODO 3: Check status code, return None on error
    
    # TODO 4: Parse JSON
    
    # TODO 5: Process cast (limit to max_cast)
    #         For each actor, extract:
    #         - tmdb_id (from 'id')
    #         - name
    #         - profile_url (build from profile_path, handle None)
    #         - character
    #         - order
    
    # TODO 6: Process crew to find directors
    #         Filter crew where job == 'Director'
    #         For each director, extract:
    #         - tmdb_id (from 'id')
    #         - name
    #         - profile_url (build from profile_path, handle None)
    
    # TODO 7: Log if no director found (this can happen!)
    
    # TODO 8: Return dict with 'cast' and 'directors' lists