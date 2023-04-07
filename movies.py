import requests
from bs4 import BeautifulSoup
import time
import json
import sqlite3
import re

def movies_data(api_key):
    movies_dict = {}
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    #im not sure how to get the genre since when you click the filter on the site, there is no change to the url..
    i = 0
    for genre in genres:
        #i want to use the method that you used to find a random amount of movies with a certain genre... 
        #though I have no idea what the url looks like to access a given page
        url = "https://api.themoviedb.org/3/movie/550?api_key={api_key}&callback=test" 
        response = requests.get(url)
        dict = json.loads(response)
        movies_dict[] = dict[genre]
        i += 1
        if i >= 100: #get exactly 100 movies
            break
    return movies_dict

def scrape_movies():
