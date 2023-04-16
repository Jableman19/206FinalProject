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
    dict = json.loads(response.text)
    id_to_name = {}
    name_to_id = {}
    for genre in dict['genres']:
        if genre['name'] in genres:
            id_to_name[genre['id']] = genre['name'] 
            name_to_id[genre['name']] = genre['id'] 
    return id_to_name, name_to_id

#DO UNIQUE MOVIES -> if the movie is already in the thing then don't count it-> switch pages and grab the first 100 unique movies :)
def get_movies(genre_dict, api_key): #genre_dict is 
    scores_nested = {}
    movies_per_genre = {} #{genre : [[name0, score0], [name1, score1]...]...}
    already_processed = [] #ids of the movies that have already been scraped
    for genre_id in genre_dict.keys(): #how to loop for the specific page
        for page in range(1, 5): #rip the hardcoding
            count = 0 #somehow grab some same number 
            url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key  + "&with_genres=" + str(genre_id) + "&page=" + str(page)
            response = requests.get(url)
            dict = json.loads(response.text)
            genre_name = genre_dict[genre_id]
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
                    count += 1
                if count == 25:
                    break
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
    api_key = "ccaddcfc821617cf6afe4ed671bc203a"
    genre_list = ["Horror", "Thriller", "Comedy", "Romance", "Action"]
    id_to_name, name_to_id = get_genre_ids(api_key)
    scores_nested, movies_per_genre = get_movies(id_to_name, api_key)
    avg_calc_dict = avg_calc(scores_nested)

    # if len(avg_calc_dict) != 5:
    #     print('length not 5')
    # for genre in genre_list: 
    #     if len(movies_per_genre[genre]) != 20:
    #         print('not length 20')

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    #claims that the table already exists...
    c.execute('''CREATE TABLE IF NOT EXISTS Genre_averages (id INTEGER, genre TEXT, score NUMERIC)''')
    for genre in genre_list: #genre should be the genre name
            # print(name_to_id[genre])
            # print(genre)
            # print(avg_calc_dict[genre])
            # print('====')
            c.execute("INSERT OR IGNORE INTO Genre_averages VALUES (?, ?, ?)", (name_to_id[genre], genre, avg_calc_dict[genre]))

    c.execute('''CREATE TABLE IF NOT EXISTS Movies (id INTEGER, name TEXT, genre_id INTEGER, score NUMERIC)''') #SHOULD BE GENRE_ID INTEGER
    for genre in genre_list:
        for movie in movies_per_genre[genre]:
            c.execute("INSERT OR IGNORE INTO Movies VALUES (?, ?, ?, ?)", (movie[0], movie[1], name_to_id[genre], movie[2],)) #how much does the id matter :)
    conn.commit()
    conn.close()
        
if __name__ == "__main__":
    main()
