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


if __name__ == '__main__':
    create_bar_plot('games.db', 'games', 'genre', 'Average Scores by Media Type')
    create_bar_plot('movies.db', 'movies', 'genre', 'Average Scores by Media Type')
    create_bar_plot('books.db', 'books', 'genre', 'Average Scores by Media Type')

# import sqlite3
# import matplotlib.pyplot as plt


# def get_data_from_db(db_file, genre):
#     conn = sqlite3.connect(db_file)
#     c = conn.cursor()
#     c.execute("SELECT score FROM games WHERE genre=?", (genre,))
#     scores = [score[0]/10 for score in c.fetchall()]
#     conn.close()
#     return scores


# def create_bar_plot(db_file):
#     genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
#     fig, ax = plt.subplots()
#     for genre in genres:
#         scores = get_data_from_db(db_file, genre)
#         if scores:
#             avg_score = round(sum(scores)/len(scores), 2)
#             ax.bar(genre, avg_score)
#             ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
#     ax.set_ylim(0, 10)
#     ax.set_title('Average Game Scores by Genre')
#     ax.set_xlabel('Genre')
#     ax.set_ylabel('Score (out of 10)')
#     plt.show()


# if __name__ == '__main__':
#     create_bar_plot('games.db')



