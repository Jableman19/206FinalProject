import sqlite3
import matplotlib.pyplot as plt


def get_data_from_db(db_file, table_name, genre_col_name, genre):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT score FROM {} WHERE {}=?".format(table_name, genre_col_name), (genre,))
    scores = [score[0]/10 for score in c.fetchall()]
    conn.close()
    return scores


def create_bar_plot(db_file, table_name, genre_col_name, title):
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    for ax, media_type in zip(axs, ['Games', 'Movies', 'Books']):
        ax.set_title(f'Average {media_type} Scores by Genre')
        ax.set_xlabel('Genre')
        ax.set_ylabel('Score (out of 10)')
        ax.set_ylim(0, 10)
        for genre in genres:
            scores = get_data_from_db(db_file, table_name, genre_col_name, genre)
            if scores:
                avg_score = round(sum(scores)/len(scores), 2)
                ax.bar(genre, avg_score)
                ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
    plt.suptitle(title, fontsize=16)
    plt.show()

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
        if genre == 'Horror':
            c.execute("SELECT score FROM Horror")
            scores = [score[0] for score in c.fetchall()]
            if scores:
                avg_score = round(sum(scores)/len(scores), 2)
                ax.bar(genre, avg_score)
                ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
        elif genre == 'Thriller':
            c.execute("SELECT score FROM Thriller")
            scores = [score[0] for score in c.fetchall()]
            if scores:
                avg_score = round(sum(scores)/len(scores), 2)
                ax.bar(genre, avg_score)
                ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
        elif genre == 'Comedy':
            c.execute("SELECT score FROM Comedy")
            scores = [score[0] for score in c.fetchall()]
            if scores:
                avg_score = round(sum(scores)/len(scores), 2)
                ax.bar(genre, avg_score)
                ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
        elif genre == 'Romance':
            c.execute("SELECT score FROM Romance")
            scores = [score[0] for score in c.fetchall()]
            if scores:
                avg_score = round(sum(scores)/len(scores), 2)
                ax.bar(genre, avg_score)
                ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
        elif genre == 'Action':
            c.execute("SELECT score FROM Action")
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
    i = 0
    for genre in genres:
        #select scores from tables games, books, genre_ids
        c.execute("SELECT score FROM games WHERE genre = ?", (genre,))
        scores = [score[0]/10 for score in c.fetchall()]
        c.execute("SELECT score FROM books WHERE genre = ?", (genre,))
        scores += [score[0]/10 for score in c.fetchall()]
        c.execute("SELECT score FROM genre_ids WHERE genre_id = ?", (i,))
        scores += [score[0] for score in c.fetchall()]
        if scores:
            avg_score = round(sum(scores)/len(scores), 2)
            ax.bar(genre, avg_score)
            ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
        i += 1
    plt.show()
    c.close()

def create_media_types_plot():
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
    i = 0
    # for genre in genres:
        
    return

if __name__ == '__main__':
    create_games_plot()
    create_movies_plot()
    create_books_plot()
    create_genre_ratings_plot()