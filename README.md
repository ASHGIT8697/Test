Movie Suggestion Bot 

Overview : 
This Script scrapes movie data from IMDb based on the user's input genre and saves it to a CSV file.
It also provides a random selection of movie suggestions from the scraped data. The script is written in Python and utillizes the following libraries requests, BeautifulSoup(from bs4) and pandas.

Featurs :
1. Scrapes movies from IMDb based on a specified genre.
2. Extarct movie details such as title, year of release, rating and genre.
3. Saves the scraped data to a CSV file at a user-specified location.
4. Provides random movie suggestion from the scraped data.

Prerequisites :
Ensure you have the following installed:
1. Python 3.x
2. Required Python libraries:
    1. requests
    2. bs4 (BeautifulSoup)
    3. pandas
Install these libraries using pip if not already installed:

pip install requests beautifulsoup4 pandas

How to Use :
1. Run the Script.
2. Input Parameters:
   1. Enter the genre of movies you want to scrape (e.g., Comedy, Action).
   2. Enter the number of movie suggestions you want (e.g. 3).
   3. Provide the file path where the scraped data should be saved (e.g., C:/Users/Name/movies.csv).
3. View Output :
   1. The script will scrape data from IMDb and save it as a CSV file.
   2. A list of random movie suggestions will be displayed in the console.
