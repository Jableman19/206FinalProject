import requests
from bs4 import BeautifulSoup
import time
import json
import sqlite3
import re

#return a dictionary of genre names to their ids
#use that to loop through each genre page to get a count and total score for each movie scraped
#calculate the average of each genre in a separate function
#plot it


def get_genre_ids(api_key):
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    response = requests.get(url="https://api.themoviedb.org/3/genre/movie/list?api_key=" + api_key + "&language=en-US")
    #should get a json of genres: https://developers.themoviedb.org/3/genres/get-movie-list
    dict = json.loads(response.text)
    id_to_name = {}
    name_to_id = {}
    for genre in dict["genres"]:
        if genre in genres:
            id_to_name[genre["id"]] = genre["name"] 
            name_to_id[genre["name"]] = genre["id"] 
    return id_to_name, name_to_id

#base_url/endpoint with parameters
#movie list- here is the link https://api.themoviedb.org/3/genre/movie/list?api_key=<<api_key>>&language=en-US for list of movies
#somehow grab movie ids from a specific genre- there are genre ids 
#https://api.themoviedb.org/3/movie/{movie_id}?api_key=<<api_key>>&language=en-US <-- this is a page for a movie
#get genre ids in a list (/genre/movie/list --> genres["name"] grab the id)
#find a way to get the genre id to a page with movie ids??? or loop through a 
#function to grab movie_ids per genre (/movie/{movie_id}/reviews)
#looping through the movie_ids to get the reviews for that certain genre and then consolidate into an average

def scrape_movies(genre_dict, api_key): #get_genre_ids list 
    scores_nested = {}
    for genre in genre_dict:
        url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key  + "&with_genres=" + str(genre)
        response = requests.get(url)
        dict = json.loads(response)
        for movie in dict["results"]:
            if movie["genre_id"] in genre_dict.keys(): #too ambiguous and not efficient, a lot of working backwards
                #we have genre id
                #add the reviews {genre : {total:count}, }
                genre_name = genre_dict[movie["genre_id"]]
                if not scores_nested[genre_name]:
                    scores_nested[genre_name] = {movie["vote_average"] : 1}
                else:
                    scores_nested[genre_name] += movie["vote_average"] #update total vote rating
                    scores_nested[genre_name][movie["vote_average"]] += 1 #update the count
    return scores_nested


def avg_calc(scores_nested):
    avg_dict = {} #{genre: avg_rating}
    for name, values in scores_nested.items():
        for total, count in values:
            avg_dict[name] = total / count
    return avg_dict

def main():
    api_key = "ccaddcfc821617cf6afe4ed671bc203a"
    id_to_name, name_to_id = get_genre_ids(api_key)
    print(id_to_name)
    scores_nested = scrape_movies(id_to_name, api_key)
    avg_calc_dict = avg_calc(scores_nested)

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE movies (id integer, genre TEXT, score NUMERIC)''')
    genre_list = ["Horror", "Thriller", "Comedy", "Romance", "Action"]
    for genre in genre_list: #genre should be the genre name
            c.execute("INSERT OR IGNORE INTO movies VALUES (?, ?, ?)", (name_to_id[genre], genre, avg_calc_dict[genre]))
    conn.commit()
        
if __name__ == "__main__":
    main()
