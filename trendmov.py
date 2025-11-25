import requests


TMDB_API_KEY = "417fef161d9c1993b83b449c9ca2827c"      
OMDB_API_KEY = "51a64312"                               

TMDB_TRENDING_URL = "https://api.themoviedb.org/3/trending/movie/day"
OMDB_URL = "http://www.omdbapi.com/"

def show_trending_movies():
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(TMDB_TRENDING_URL, params=params)

    if response.status_code != 200:
        print("Could not fetch trending movies.", response.status_code)
        return []

    movies = response.json().get("results", [])[:5]
    print("=== TOP 5 TRENDING MOVIES TODAY ===")
    for i, movie in enumerate(movies, start=1):
        title = movie.get("title", "N/A")
        year = movie.get("release_date", "N/A").split("-")[0] if movie.get("release_date") else "N/A"
        print(f"{i}. {title} ({year})")
    print()
    return movies


def main():
    trending = show_trending_movies()

   

if __name__ == "__main__":
    main()