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

    
    i = -1
    c.execute('''CREATE TABLE IF NOT EXISTS books (title text, score integer, genreID integer)''')
    #select all books with the genre of action
    c.execute('''SELECT * FROM books WHERE genreID = 4''')
    if len(c.fetchall()) == 0:
        i = 4
    #select all books with the genre of romance
    c.execute('''SELECT * FROM books WHERE genreID = 3''')
    if len(c.fetchall()) == 0:
        i = 3
    #select all books with the genre of comedy
    c.execute('''SELECT * FROM books WHERE genreID = 2''')
    if len(c.fetchall()) == 0:
        i = 2
    #select all books with the genre of thriller
    c.execute('''SELECT * FROM books WHERE genreID = 1''')
    if len(c.fetchall()) == 0:
        i = 1
    #select all books with the genre of horror
    c.execute('''SELECT * FROM books WHERE genreID = 0''')
    if len(c.fetchall()) == 0:
        i = 0
    c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS titleIndex ON books (title)''')
    genreNum = i
    if(genreNum == -1):
        barplot.create_games_plot()
        barplot.create_books_plot()
        barplot.create_movies_plot()
        barplot.create_genre_ratings_plot()
        barplot.create_media_types_plot()
        return
    booksByGenre = goodreads.scrapeBooks(int(genreNum))
    for genre in booksByGenre:
        for book in booksByGenre[genre]:
            c.execute("INSERT OR IGNORE INTO books VALUES (?, ?, ?)", (book[0], book[1], int(genreNum)))
    conn.commit()
    
    APIKEY = "moby_QgxIRNhIzjq9gW7CgE2PM8jv8y0"
    gamesByGenre = mobyGames.GetGameList(APIKEY, int(genreNum))
    scoresByGenre = {}
    for genre in gamesByGenre:
        scoresByGenre[genre] = mobyGames.scrapeGenre(gamesByGenre[genre])
    c.execute('''CREATE TABLE IF NOT EXISTS games (id integer, score integer, genreID integer)''')
    c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS id ON games (id)''')
    for genre in scoresByGenre:
        i = 0
        for score in scoresByGenre[genre]:

            c.execute("INSERT OR IGNORE INTO games VALUES (?, ?, ?)", (gamesByGenre[genre][i], score, int(genreNum)))
            i += 1
    conn.commit()

    
    api_key = "ccaddcfc821617cf6afe4ed671bc203a"
    genre_list = ["Horror", "Thriller", "Comedy", "Romance", "Action"]
    movies_per_genre = movies.get_movies(api_key, int(genreNum))
    # avg_calc_dict = avg_calc(scores_nested)

    conn = sqlite3.connect('ratings.db')
    c = conn.cursor()
    id_list = [27, 53, 35, 10749, 28]
    c.execute("CREATE TABLE IF NOT EXISTS genre_table (id INT, new_id INT, genre TEXT)")
    c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS id ON genre_table (id)''')
    for i in range(0,5):
        c.execute("INSERT OR IGNORE INTO genre_table VALUES (?, ?, ?)", (id_list[i], i, genre_list[i]))
    
    c.execute("CREATE TABLE IF NOT EXISTS movie_ratings (id INTEGER, name TEXT, score NUMERIC)")
    for movie in movies_per_genre[genre_list[int(genreNum)]]:
        c.execute("INSERT OR IGNORE INTO movie_ratings VALUES ( ?, ?, ?)", (movie[0], movie[1], movie[2]))

    c.execute("CREATE TABLE IF NOT EXISTS movie_genres (id INTEGER, name TEXT, genre_id INTEGER)")
    for movie in movies_per_genre[genre_list[int(genreNum)]]:
        c.execute("INSERT OR IGNORE INTO movie_genres VALUES (?, ?, ?)", (movie[0], movie[1], int(genreNum)))
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