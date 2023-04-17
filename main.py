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
    c.execute("DROP TABLE IF EXISTS books")
    c.execute("DROP TABLE IF EXISTS games")
    c.execute("DROP TABLE IF EXISTS movie_ratings")
    c.execute("DROP TABLE IF EXISTS movie_genres")
    conn.commit()

    for i in range(0, 5):
        genreNum = i
        booksByGenre = goodreads.scrapeBooks(int(genreNum))
        
        c.execute('''CREATE TABLE IF NOT EXISTS books (title text, genre text, score integer, genreID integer)''')
        c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS titleIndex ON books (title)''')
        for genre in booksByGenre:
            for book in booksByGenre[genre]:
                c.execute("INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?)", (book[0], genre, book[1], int(genreNum)))
        conn.commit()
    
    APIKEY = "moby_QgxIRNhIzjq9gW7CgE2PM8jv8y0"
    for i in range(0, 5):
        genreNum = i
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

    for i in range(0, 5):
        genreId = i
        api_key = "ccaddcfc821617cf6afe4ed671bc203a"
        genre_list = ["Horror", "Thriller", "Comedy", "Romance", "Action"]
        id_to_name, name_to_id = movies.get_genre_ids(api_key)
        scores_nested, movies_per_genre = movies.get_movies(api_key, int(genreId))
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

    barplot.create_games_plot()
    barplot.create_books_plot()
    barplot.create_movies_plot()
    barplot.create_genre_ratings_plot()
    barplot.create_media_types_plot()



if __name__ == "__main__":
    main()