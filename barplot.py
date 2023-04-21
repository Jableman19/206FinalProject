import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_data_from_db(db_file, table_name, genre_col_name, genre):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT score FROM {} WHERE {}=?".format(table_name, genre_col_name), (genre,))
    scores = [score[0]/10 for score in c.fetchall()]
    conn.close()
    return scores

def create_games_plot():
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    # create a figure with 1 subplot
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    # set the title of the plot
    ax.set_title('Average Game Scores by Genre')
    # set the x-axis label
    ax.set_xlabel('Genre')
    # set the y-axis label
    ax.set_ylabel('Score (out of 10)')
    # set the y-axis limits
    ax.set_ylim(0, 10)
    # loop through the genres
    conn = sqlite3.connect("ratings.db")
    c = conn.cursor()
    #select score from games where genre = genre
    for genre in genres:
        c.execute("SELECT score FROM games WHERE genre = ?", (genre,))
        scores = [score[0]/10 for score in c.fetchall()]
        if scores:
            avg_score = round(sum(scores)/len(scores), 2)
            ax.bar(genre, avg_score)
            ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
    plt.show()
    c.close()

def create_books_plot():
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    # create a figure with 1 subplot
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    # set the title of the plot
    ax.set_title('Average Book Scores by Genre')
    # set the x-axis label
    ax.set_xlabel('Genre')
    # set the y-axis label
    ax.set_ylabel('Score (out of 10)')
    # set the y-axis limits
    ax.set_ylim(0, 10)
    # loop through the genres
    conn = sqlite3.connect("ratings.db")
    c = conn.cursor()
    #select score from games where genre = genre
    for genre in genres:
        c.execute("SELECT score FROM books WHERE genre = ?", (genre,))
        scores = [score[0]/10 for score in c.fetchall()]
        if scores:
            avg_score = round(sum(scores)/len(scores), 2)
            ax.bar(genre, avg_score)
            ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
    plt.show()
    c.close()

def create_movies_plot():
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    # create a figure with 1 subplot
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    # set the title of the plot
    ax.set_title('Average Movie Scores by Genre')
    # set the x-axis label
    ax.set_xlabel('Genre')
    # set the y-axis label
    ax.set_ylabel('Score (out of 10)')
    # set the y-axis limits
    ax.set_ylim(0, 10)
    # loop through the genres
    conn = sqlite3.connect("ratings.db")
    c = conn.cursor()
    #select score from games where genre = genre
    for genre in genres:
        c.execute("SELECT movie_ratings.score FROM movie_ratings JOIN movie_genres ON movie_ratings.id = movie_genres.id WHERE movie_genres.genre = ?", (genre,))
        scores = [score[0] for score in c.fetchall()]
        if scores:
            avg_score = round(sum(scores)/len(scores), 2)
            ax.bar(genre, avg_score)
            ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
    plt.show()
    c.close()

    conn.close()

def plot_all_together():
    return

def create_genre_ratings_plot():
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    ig, ax = plt.subplots(1, 1, figsize=(15, 5))
    # set the title of the plot
    ax.set_title('Average scores by Genre Across all media types')
    # set the x-axis label
    ax.set_xlabel('Genres')
    # set the y-axis label
    ax.set_ylabel('Rating (out of 10)')
    # set the y-axis limits
    ax.set_ylim(0, 10)
    # loop through the genres
    conn = sqlite3.connect('ratings.db')
    c = conn.cursor()
    for genre in genres:
        #select scores from tables games, books, genre_ids
        c.execute("SELECT score FROM games WHERE genre = ?", (genre,))
        scores = [score[0]/10 for score in c.fetchall()]
        c.execute("SELECT score FROM books WHERE genre = ?", (genre,))
        scores += [score[0]/10 for score in c.fetchall()]
        c.execute("SELECT movie_ratings.score FROM movie_ratings JOIN movie_genres ON movie_ratings.id = movie_genres.id WHERE movie_genres.genre = ?", (genre,))
        scores += [score[0] for score in c.fetchall()]
        if scores:
            avg_score = round(sum(scores)/len(scores), 2)
            ax.bar(genre, avg_score)
            ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
    plt.show()
    c.close()

def create_media_types_plot():
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    ig, ax = plt.subplots(1, 1, figsize=(15, 5))
    # set the title of the plot
    ax.set_title('Average scores by Genre and Media Type')
    # set the x-axis label
    ax.set_xlabel('Genres')
    # set the y-axis label
    ax.set_ylabel('Rating (out of 10)')
    # set the y-axis limits
    ax.set_ylim(0, 10)
    # loop through the genres
    conn = sqlite3.connect('ratings.db')
    c = conn.cursor()
    #loop through the genres and get the average score for each genre for each media type. 
    data = {'Games': {}, 'Books': {}, 'Movies': {}}
    for genre in genres:
        #select scores from tables games, books, genre_ids
        c.execute("SELECT score FROM games WHERE genre = ?", (genre,))
        gameScores = [score[0]/10 for score in c.fetchall()]
        c.execute("SELECT score FROM books WHERE genre = ?", (genre,))
        bookScores = [score[0]/10 for score in c.fetchall()]
        c.execute("SELECT movie_ratings.score FROM movie_ratings JOIN movie_genres ON movie_ratings.id = movie_genres.id WHERE movie_genres.genre = ?", (genre,))
        movieScores = [score[0] for score in c.fetchall()]
        #create a bar chart where there are 5 groupings of 3 bars each.
        #each grouping will be a genre and the 3 bars will be the average score for each media type
        if gameScores and bookScores and movieScores:
            avg_game_score = round(sum(gameScores)/len(gameScores), 2)
            avg_book_score = round(sum(bookScores)/len(bookScores), 2)
            avg_movie_score = round(sum(movieScores)/len(movieScores), 2)
            data['Games'][genre] = avg_game_score
            data['Books'][genre] = avg_book_score
            data['Movies'][genre] = avg_movie_score
    #create a bar chart where there are 5 groupings of 3 bars each.
    #each grouping will be a genre and the 3 bars will be the average score for each media type
    x = np.arange(len(genres))  # the label locations
    width = 0.25  # the width of the bars   
    rects1 = ax.bar(x - width, data['Games'].values(), width, label='Games')
    rects2 = ax.bar(x, data['Books'].values(), width, label='Books')
    rects3 = ax.bar(x + width, data['Movies'].values(), width, label='Movies')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by Genre and Media Type')
    ax.set_xticks(x)
    ax.set_xticklabels(genres)
    ax.legend()
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    plt.show()
if __name__ == '__main__':
    create_games_plot()
    create_movies_plot()
    create_books_plot()
    create_genre_ratings_plot()
    create_media_types_plot()