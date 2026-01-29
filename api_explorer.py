import requests
from config import TMDB_API_KEY
from tmdb_client import fetch_genres
   
genres = fetch_genres()
print(f"Fetched {len(genres)} genres")
print(genres)

#url = "https://api.themoviedb.org/3/genre/movie/list"
#params = {"api_key": TMDB_API_KEY}
#response = requests.get(url, params=params)
#print(response.json())