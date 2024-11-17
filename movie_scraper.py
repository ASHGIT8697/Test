import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

    
def scrape_movies(genre, min_rating, num_suggestions, save_path):     
    #Setup headless browser option
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    #Constructing IMDB URL
    url=f"https://www.imdb.com/search/title/?genres={genre}"
    print(f"Scraping Movies!!!")
    driver.get(url)
    time.sleep(5)
    
    movie_element = driver.find_elements(By.CLASS_NAME, '.ipc-page-grid ipc-page-grid--bias-left ipc-page-grid__item ipc-page-grid__item--span-2')
    print(f"movie_element")
    movies = []
    
    for element in movie_element:

        try:
            title = element.find_element(By.CLASS_NAME, '.ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-a69a4297-2 bqNXEn dli-title with-margin').text
            year = element.find_element(By.CLASS_NAME, '').text
            rating=element.find_element(By.CLASS_NAME, '').text
            
            movies.append({
                "Title" : title,
                "Year" : year,
                "Rating" : rating,
                "Genre": genre
            })
        except Exception as e:
            print("Error Extracting data from a movie element: {e}")
        finally:
            driver.quit()
        
    df=pd.DataFrame(movies)
    df.to_csv(save_path, index=False)
    print(f"Data Saved!!")
    
    suggest_random_movies(df, min_rating, num_suggestions)
        
def suggest_random_movies(df,min_rating, num_suggestions):
    #filter top rated movies with the minimum rating
    top_movies=df[df["Rating"]>=min_rating]
    #Random Select
    suggestions=top_movies.sample(n=min(num_suggestions,len(top_movies)))
    
    #Display suggestions
    print("\n Here are some Suggestions for you : ")
    for _, movie in suggestions.iterrows():
        print(f"{movie['Title']}({movie['Year']}) - Rating:{movie['Rating']} - Cast:{movie['Cast']}")
        
#Get Input
genre = input("Enter the genre you're interested in : ")
min_rating=float(input("Enter the minimum rating for movies from (0-10) :"))
num_suggestions = int(input("Enter the number of Movie Suggestions : "))
save_path=input("Enter the destination path to save CSV file(e.g /xx/movies.csv) : ")

scrape_movies(genre,min_rating,num_suggestions,save_path)
    