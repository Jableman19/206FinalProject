import requests
from bs4 import BeautifulSoup
import time
import json
import sqlite3
import re
import random
import sys

#return a dictionary of genre names to their ids
#use that to loop through each genre page to get a count and total score for each movie scraped
#calculate the average of each genre in a separate function
#plot it

def get_genre_ids(api_key):
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    response = requests.get(url="https://api.themoviedb.org/3/genre/movie/list?api_key=" + api_key + "&language=en-US")
    dict = json.loads(response.text)
    id_to_name = {}
    name_to_id = {}
    for genre in dict['genres']:
        if genre['name'] in genres:
            id_to_name[genre['id']] = genre['name'] 
            name_to_id[genre['name']] = genre['id'] 
    return id_to_name, name_to_id

#DO UNIQUE MOVIES -> if the movie is already in the thing then don't count it-> switch pages and grab the first 100 unique movies :)
def get_movies( api_key, genreID): #genre_dict is 
    scores_nested = {}
    movies_per_genre = {} #{genre : [[name0, score0], [name1, score1]...]...}
    already_processed = [] #ids of the movies that have already been scraped
    genre_dict= {27: 'Horror', 53: 'Thriller', 35: 'Comedy', 10749: 'Romance',28: 'Action'}
    print(f'genreDict: {genre_dict}')
    random_genre = list(genre_dict.keys())[genreID] #genre_dict is a dict of genre ids to genre names
    random_page = random.randint(1, 500)
    url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key  + "&with_genres=" + str(random_genre) + "&page=" + str(random_page)
    response = requests.get(url)
    dict = json.loads(response.text)
    genre_name = genre_dict[random_genre] #uhh genre_dict is indeed a dict LMAO
    movies_per_genre[genre_name] = []
    for movie in dict["results"]:
        if movie["id"] not in already_processed:
            movies_per_genre[genre_name].append([movie["id"], movie["original_title"], movie["vote_average"]]) #add the reviews {genre : {total:count}, }
            already_processed.append(movie["id"])
            if genre_name not in scores_nested:
                scores_nested[genre_name] = [movie["vote_average"], 1]
            else:
                scores_nested[genre_name][0] += movie["vote_average"] #update total vote rating
                scores_nested[genre_name][1] += 1 #update the count
    print(scores_nested) #should ask if duplicate movies is ok... but we have like 200 movies in the database?? (there are duplicates in the table gjhfjkg)
    print(movies_per_genre)
    return scores_nested, movies_per_genre

def avg_calc(scores_nested): #scores nested is {genre_name : [total_score, number_movies]}
    avg_dict = {} 
    for name, values in scores_nested.items():
        total, count = values
        avg_dict[name] = total / count
    return avg_dict #{genre: avg_rating}

def main():
    genreId = sys.argv[1]
    api_key = "API_KEY_HERE"
    genre_list = ["Horror", "Thriller", "Comedy", "Romance", "Action"]
    id_to_name, name_to_id = get_genre_ids(api_key)
    scores_nested, movies_per_genre = get_movies(api_key, int(genreId))
    # avg_calc_dict = avg_calc(scores_nested)

    conn = sqlite3.connect('ratings.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS movie_ratings (id INTEGER, name TEXT, score NUMERIC)")
    for movie in movies_per_genre[genre_list[int(genreId)]]:
        c.execute("INSERT OR IGNORE INTO movie_ratings VALUES ( ?, ?, ?)", (movie[0], movie[1], movie[2]))

    c.execute("CREATE TABLE IF NOT EXISTS movie_genres (id INTEGER, name TEXT, genre_id INTEGER, genre TEXT)")
    for movie in movies_per_genre[genre_list[int(genreId)]]:
        c.execute("INSERT OR IGNORE INTO movie_genres VALUES (?, ?, ?, ?)", (movie[0], movie[1], int(genreId), genre_list[int(genreId)]))

    conn.commit()
    conn.close()
        
if __name__ == "__main__":
    main()
