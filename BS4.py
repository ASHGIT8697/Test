import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

def scrape_movies(genre, min_rating, num_suggestions, save_path):
    # Constructing IMDb URL
    url = f"https://www.imdb.com/search/title/?genres={genre}"
    print("Scraping Movies!!!")
    
    # Send an HTTP request to the IMDb server
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve data from IMDb")
        return
    
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Locate movie elements
    movie_elements = soup.find_all('div', class_='lister-item mode-advanced')
    movies = []
    
    for element in movie_elements:
        try:
            # Extract title
            title = element.h3.a.text.strip()
            
            # Extract year
            year = element.h3.find('span', class_='lister-item-year').text.strip()
            
            # Extract rating
            rating_tag = element.find('div', class_='inline-block ratings-imdb-rating')
            rating = float(rating_tag['data-value']) if rating_tag else None
            
            # Collect movie details
            movies.append({
                "Title": title,
                "Year": year,
                "Rating": rating,
                "Genre": genre
            })
        except Exception as e:
            print(f"Error extracting data for a movie element: {e}")
    
    # Save data to a CSV file
    df = pd.DataFrame(movies)
    df.to_csv(save_path, index=False)
    print("Data Saved!!")
    
    # Suggest movies
    suggest_random_movies(df, min_rating, num_suggestions)

def suggest_random_movies(df, min_rating, num_suggestions):
    # Filter top-rated movies with the minimum rating
    top_movies = df[df["Rating"].notnull() & (df["Rating"] >= min_rating)]
    
    # Random selection
    suggestions = top_movies.sample(n=min(num_suggestions, len(top_movies)))
    
    # Display suggestions
    print("\nHere are some suggestions for you:")
    for _, movie in suggestions.iterrows():
        print(f"{movie['Title']} ({movie['Year']}) - Rating: {movie['Rating']}")

# Get Input
genre = input("Enter the genre you're interested in: ").lower()
min_rating = float(input("Enter the minimum rating for movies from (0-10): "))
num_suggestions = int(input("Enter the number of movie suggestions: "))
save_path = input("Enter the destination path to save CSV file (e.g., /path/to/movies.csv): ")

scrape_movies(genre, min_rating, num_suggestions, save_path)
