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
    # print("====")
    # print(dict)
    # print("====")
    id_to_name = {}
    name_to_id = {}
    for genre in dict['genres']:
        if genre['name'] in genres:
            id_to_name[genre['id']] = genre['name'] 
            name_to_id[genre['name']] = genre['id'] 
    return id_to_name, name_to_id

#base_url/endpoint with parameters
#movie list- here is the link https://api.themoviedb.org/3/genre/movie/list?api_key=<<api_key>>&language=en-US for list of movies
#somehow grab movie ids from a specific genre- there are genre ids 
#https://api.themoviedb.org/3/movie/{movie_id}?api_key=<<api_key>>&language=en-US <-- this is a page for a movie
#get genre ids in a list (/genre/movie/list --> genres["name"] grab the id)
#find a way to get the genre id to a page with movie ids??? or loop through a 
#function to grab movie_ids per genre (/movie/{movie_id}/reviews)
#looping through the movie_ids to get the reviews for that certain genre and then consolidate into an average

def scrape_movies(genre_dict, api_key): #genre_dict is 
    scores_nested = {}
    movies_per_genre = {} #{genre : [[name0, score0], [name1, score1]...]...}
    for genre_id in genre_dict.keys(): #loop through the id_to_name dict 
        url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key  + "&with_genres=" + str(genre_id)
        response = requests.get(url)
        dict = json.loads(response.text)
        genre_name = genre_dict[genre_id]
        movies_per_genre[genre_name] = []
        for movie in dict["results"]:
            #we have genre id
            #add the reviews {genre : {total:count}, }
            movies_per_genre[genre_name].append([movie["original_title"], movie["vote_average"]])
            if genre_name not in scores_nested:
                scores_nested[genre_name] = [movie["vote_average"], 1]
            else:
                scores_nested[genre_name][0] += movie["vote_average"] #update total vote rating
                scores_nested[genre_name][1] += 1 #update the count
    print(scores_nested) #should ask if duplicate movies is ok... (if it counts towards 100 things) it should but pain
    print(movies_per_genre)
    return scores_nested, movies_per_genre


def avg_calc(scores_nested): #scores nested is {genre_name : [total_score, number_movies]}
    avg_dict = {} 
    for name, values in scores_nested.items():
        total, count = values
        avg_dict[name] = total / count
    return avg_dict #{genre: avg_rating}

def main():
    api_key = "key here"
    id_to_name, name_to_id = get_genre_ids(api_key)
    # print(id_to_name)
    # print("=====")
    # print(name_to_id)
    scores_nested, movies_per_genre = scrape_movies(id_to_name, api_key)
    #scores_nested, movies_per_genre = scrape_movies(id_to_name, api_key)
    #print(len(movies_per_genre))
    avg_calc_dict = avg_calc(scores_nested)

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    #claims that the table already exists...
    c.execute('''CREATE TABLE IF NOT EXISTS genre_averages (id integer, genre TEXT, score NUMERIC)''')
    c.execute('''CREATE TABLE IF NOT EXISTS movies (id integer, name TEXT, genre TEXT, score NUMERIC)''')
    genre_list = ["Horror", "Thriller", "Comedy", "Romance", "Action"]
    i = 0
    for genre in genre_list: #genre should be the genre name
            c.execute("INSERT OR IGNORE INTO genre_averages VALUES (?, ?, ?)", (name_to_id[genre], genre, avg_calc_dict[genre]))
            c.execute("INSERT OR IGNORE INTO movies VALUES (?,?,?,?)", (i, movies_per_genre[genre][i][0], genre, movies_per_genre[genre][i][1])) #how much does the id matter :)
            i += 1
    conn.commit()
        
if __name__ == "__main__":
    main()
