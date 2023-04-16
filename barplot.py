import sqlite3
import matplotlib.pyplot as plt


def get_data_from_db(db_file, genre):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT score FROM games WHERE genre=?", (genre,))
    scores = [score[0]/10 for score in c.fetchall()]
    conn.close()
    return scores


def create_bar_plot(db_file):
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    fig, ax = plt.subplots()
    for genre in genres:
        scores = get_data_from_db(db_file, genre)
        if scores:
            avg_score = round(sum(scores)/len(scores), 2)
            ax.bar(genre, avg_score)
            ax.text(genre, avg_score, str(avg_score), ha='center', va='bottom')
    ax.set_ylim(0, 10)
    ax.set_title('Average Game Scores by Genre')
    ax.set_xlabel('Genre')
    ax.set_ylabel('Score (out of 10)')
    plt.show()


if __name__ == '__main__':
    create_bar_plot('games.db')

