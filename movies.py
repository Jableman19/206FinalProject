import requests
from bs4 import BeautifulSoup
import time
import json
import sqlite3
import re

def get_genre_ids(api_key):
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    response = requests.get(url="https://api.themoviedb.org/3/genre/movie/list?api_key=<<api_key>>&language=en-US")
    #should get a json of genres: https://developers.themoviedb.org/3/genres/get-movie-list
    dict = json.loads(response)
    genre_ids = []
    both = []
    for genre in dict["genres"]:
        if genre["name"] in genres:
            genre_ids.append(genre["id"])
            both.append((genre, genre["id"])) #list of genres with their respective ids
    return (genres, genre_ids, both)
#base_url/endpoint with parameters
#movie list- here is the link https://api.themoviedb.org/3/genre/movie/list?api_key=<<api_key>>&language=en-US for list of movies
#somehow grab movie ids from a specific genre- there are genre ids 
#https://api.themoviedb.org/3/movie/{movie_id}?api_key=<<api_key>>&language=en-US <-- this is a page for a movie
#get genre ids in a list (/genre/movie/list --> genres["name"] grab the id)
#find a way to get the genre id to a page with movie ids??? or loop through a 
#function to grab movie_ids per genre (/movie/{movie_id}/reviews)
#looping through the movie_ids to get the reviews for that certain genre and then consolidate into an average

def scrape_movies(genre_list, api_key): #get_genre_ids list 
    scores = []
    for genre in genre_list:
        url = "https://api.themoviedb.org/3/discover/movie?api_key=<<api_key>>&with_genres=" + str(genre)
        response = requests.get(url)
        dict = json.loads(response)
        for movie in dict["results"]:
            if (movie["genre_id"] in genre_list[1]):


def avg_dict():
