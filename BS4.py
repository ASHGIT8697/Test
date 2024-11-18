import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

def scrape_movies(genre, min_rating, num_suggestions, save_path):
    # Constructing IMDb URL
    url = f"https://www.imdb.com/search/title/?genres={genre}"
    print("Scraping Movies!!!")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    # Send an HTTP request to the IMDb server
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve data from IMDb")
        return
    
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Locate movie elements
    movie_elements = soup.find('div', class_='ipc-page-grid__item ipc-page-grid__item--span-2').find_all('li')
    movies = []
    
    for element in movie_elements:
        try:
            # Extract title
            title_tag = element.find('h3', class_= 'ipc-title__text')
            title= title_tag.text.strip() if title_tag else None
            
            # Extract year
            year_tag = element.find('span', class_='sc-5bc66c50-6 OOdsw dli-title-metadata-item')
            year= year_tag.text.strip() if year_tag else None
            
            # Extract rating
            rating_tag = element.find('span', class_='ipc-rating-star--rating')
            rating= rating_tag.text.strip() if rating_tag else None
            
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
