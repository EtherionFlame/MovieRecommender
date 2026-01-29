import requests
from config import TMDB_API_KEY

url = "https://api.themoviedb.org/3/genre/movie/list"
params = {"api_key": TMDB_API_KEY}
response = requests.get(url, params=params)
print(response.json())