import requests
from bs4 import BeautifulSoup
import time
import json
import sqlite3
import re
import random
import movies
import goodreads
import mobyGames
import barplot

def main():
    conn = sqlite3.connect('ratings.db')
    c = conn.cursor()
    # Drop all tables
    # c.execute("DROP TABLE IF EXISTS books")
    # c.execute("DROP TABLE IF EXISTS games")
    # c.execute("DROP TABLE IF EXISTS movie_ratings") 
    # c.execute("DROP TABLE IF EXISTS movie_genres")
    # conn.commit()

    
    i = 0
    c.execute('''CREATE TABLE IF NOT EXISTS books (title text, genre text, score integer, genreID integer)''')
    #select all books with the genre of action
    c.execute('''SELECT * FROM books WHERE genre = "Action"''')
    if len(c.fetchall()) == 0:
        i = 4
    #select all books with the genre of romance
    c.execute('''SELECT * FROM books WHERE genre = "Romance"''')
    if len(c.fetchall()) == 0:
        i = 3
    #select all books with the genre of comedy
    c.execute('''SELECT * FROM books WHERE genre = "Comedy"''')
    if len(c.fetchall()) == 0:
        i = 2
    #select all books with the genre of thriller
    c.execute('''SELECT * FROM books WHERE genre = "Thriller"''')
    if len(c.fetchall()) == 0:
        i = 1
    #select all books with the genre of horror
    c.execute('''SELECT * FROM books WHERE genre = "Horror"''')
    if len(c.fetchall()) == 0:
        i = 0
    c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS titleIndex ON books (title)''')
    genreNum = i
    booksByGenre = goodreads.scrapeBooks(int(genreNum))
    for genre in booksByGenre:
        for book in booksByGenre[genre]:
            c.execute("INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?)", (book[0], genre, book[1], int(genreNum)))
    conn.commit()
    
    APIKEY = "moby_QgxIRNhIzjq9gW7CgE2PM8jv8y0"
    gamesByGenre = mobyGames.GetGameList(APIKEY, int(genreNum))
    scoresByGenre = {}
    for genre in gamesByGenre:
        scoresByGenre[genre] = mobyGames.scrapeGenre(gamesByGenre[genre])
    c.execute('''CREATE TABLE IF NOT EXISTS games (id integer, genre text, score integer, genreID integer)''')
    c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS id ON games (id)''')
    for genre in scoresByGenre:
        i = 0
        for score in scoresByGenre[genre]:

            c.execute("INSERT OR IGNORE INTO games VALUES (?, ?, ?, ?)", (gamesByGenre[genre][i], genre, score, int(genreNum)))
            i += 1
    conn.commit()

    
    api_key = "ccaddcfc821617cf6afe4ed671bc203a"
    genre_list = ["Horror", "Thriller", "Comedy", "Romance", "Action"]
    id_to_name, name_to_id = movies.get_genre_ids(api_key)
    scores_nested, movies_per_genre = movies.get_movies(api_key, int(genreNum))
    # avg_calc_dict = avg_calc(scores_nested)

    conn = sqlite3.connect('ratings.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS movie_ratings (id INTEGER, name TEXT, score NUMERIC)")
    for movie in movies_per_genre[genre_list[int(genreNum)]]:
        c.execute("INSERT OR IGNORE INTO movie_ratings VALUES ( ?, ?, ?)", (movie[0], movie[1], movie[2]))

    c.execute("CREATE TABLE IF NOT EXISTS movie_genres (id INTEGER, name TEXT, genre_id INTEGER, genre TEXT)")
    for movie in movies_per_genre[genre_list[int(genreNum)]]:
        c.execute("INSERT OR IGNORE INTO movie_genres VALUES (?, ?, ?, ?)", (movie[0], movie[1], int(genreNum), genre_list[int(genreNum)]))
    conn.commit()

    conn.close()

    if(int(genreNum) == 4):
        barplot.create_games_plot()
        barplot.create_books_plot()
        barplot.create_movies_plot()
        barplot.create_genre_ratings_plot()
        barplot.create_media_types_plot()



if __name__ == "__main__":
    main()