import json
import requests
from config import TMDB_API_KEY
from tmdb_client import fetch_genres, fetch_popular_movies, fetch_movie_details, fetch_movie_credits

credits = fetch_movie_credits(550, max_cast=5)
print(json.dumps(credits, indent=2))

"""
movie_id = 550  # Fight Club

url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
params = {"api_key": TMDB_API_KEY}

response = requests.get(url, params=params)
data = response.json()

print("=== CAST (first 3) ===")
for actor in data['cast'][:3]:
    print(actor)

print("\n=== CREW (directors only) ===")
for person in data['crew']:
    if person['job'] == 'Director':
        print(person)
"""
"""
movie = fetch_movie_details(550)  # Fight Club
print(movie)
"""
"""
# Use one of the movie IDs you fetched (e.g., 1084242)
movie_id = 1084242

url = f"https://api.themoviedb.org/3/movie/{movie_id}"
params = {"api_key": TMDB_API_KEY}

response = requests.get(url, params=params)
print(response.json())
"""
"""
movie_ids = fetch_popular_movies(count=5)
print(f"Fetched {len(movie_ids)} movie IDs:")
print(movie_ids)
"""
""" For pulling the first movie listed on the most popular pages
url = "https://api.themoviedb.org/3/movie/popular"
params = {
    "api_key": TMDB_API_KEY,
    "page": 1  # TMDB returns 20 movies per page
}
response = requests.get(url, params=params)
data = response.json()

# Print the structure
print("Keys in response:", data.keys())
print("\nFirst movie:")
print(data['results'][0])
"""


"""
genres = fetch_genres()
print(f"Fetched {len(genres)} genres")
print(genres)
"""
#url = "https://api.themoviedb.org/3/genre/movie/list"
#params = {"api_key": TMDB_API_KEY}
#response = requests.get(url, params=params)
#print(response.json())