import requests
from rich import print
import emoji

TMDB_API_KEY = "417fef161d9c1993b83b449c9ca2827c"
OMDB_API_KEY = "51a64312"

TMDB_TRENDING_URL = "https://api.themoviedb.org/3/trending/movie/day"
OMDB_URL = "http://www.omdbapi.com/"

def show_trending_movies():
    """Fetch and display top 5 trending movies from TMDb."""
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(TMDB_TRENDING_URL, params=params)

    if response.status_code != 200:
        print("Could not fetch trending movies.", response.status_code)
        return []

    movies = response.json().get("results", [])[:5]
    print(emoji.emojize("[bold bright_red]TOP 5 TRENDING MOVIES TODAY :film_frames:[/bold bright_red]"))

    for i, movie in enumerate(movies, start=1):
        title = movie.get("title", "N/A")
        year = movie.get("release_date", "N/A").split("-")[0] if movie.get("release_date") else "N/A"
        print(f"{i}. {title} ({year})")
    print()  # only one blank line after the list
    return movies

def get_movie_info(title):
    """Search movie by title using OMDb API and return info including IMDb rating."""
    params = {
        "t": title,
        "apikey": OMDB_API_KEY
    }
    response = requests.get(OMDB_URL, params=params)
    data = response.json()

    if data.get("Response") == "True":
        return {
            "id": data.get("imdbID"),
            "title": data.get("Title"),
            "year": data.get("Year"),
            "plot": data.get("Plot"),
            "imdb_rating": data.get("imdbRating"),
            "cast": data.get("Actors"),
            "runtime": data.get("Runtime"),
            "director": data.get("Director")
        }
    return None

def rating_to_stars(rating_str):
    """Convert IMDb rating (0–10) into star/half-star emojis."""
    try:
        rating = float(rating_str)
        full_stars = int(rating)
        half_star = 1 if (rating - full_stars) >= 0.5 else 0
        empty_stars = 10 - full_stars - half_star
        return "★" * full_stars + "⯪" * half_star + "✩" * empty_stars
    except:
        return "No rating"

def main():
    trending = show_trending_movies()

    while True:
        print(emoji.emojize("[bold blue]Movie Info Viewer :magnifying_glass_tilted_left:[/bold blue]"))
        movie_name = input("Enter movie title (or pick trending): ").strip()
        print()

        movie_info = get_movie_info(movie_name)
        if not movie_info:
            print("[underline red]Movie not found on OMDb![/underline red]")
        else:
            print(f"[bold]Results for {movie_info['title']} ({movie_info['year']})[/bold]")
            print(emoji.emojize(f"[underline bright_blue]Plot:[/underline bright_blue] {movie_info['plot']} :writing_hand:"))
            if movie_info.get("cast"):
                print(emoji.emojize(f"[underline bright_blue]Cast:[/underline bright_blue] {movie_info['cast']} :people_with_bunny_ears:"))
            if movie_info.get("director"):
                print(emoji.emojize(f"[underline bright_blue]Director:[/underline bright_blue] {movie_info['director']} :clapper:"))
            if movie_info.get("runtime"):
                print(emoji.emojize(f"[underline bright_blue]Runtime:[/underline bright_blue] {movie_info['runtime']} :hourglass:"))
            if movie_info.get("imdb_rating") and movie_info["imdb_rating"] != "N/A":
                stars = rating_to_stars(movie_info["imdb_rating"])
                print(f"[underline yellow]IMDb Rating:[/underline yellow] {movie_info['imdb_rating']}/10 {stars}")
            else:
                print("IMDb Rating not available.")

        again = input("\nDo you want to search for another movie? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break
        print()  # single blank line before the next search

if __name__ == "__main__":
    main()
