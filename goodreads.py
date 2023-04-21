import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import re
import random
import sys

def scrapeBooks(genNum):
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    booksByGenre = {}
    genre = genres[genNum]
    booksByGenre[genre] = []
    pageLB = 1
    pageUB = 15
    print("Scraping genre: " + genre)
    time.sleep(1)
    randomPage = random.randint(pageLB, pageUB)
    url = "https://www.goodreads.com/shelf/show/" + genre + "?page=" + str(randomPage)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    #find score
    books = soup.find_all("div", {"class": "elementList"})
    for book in books:
        if(len(booksByGenre[genre]) >= 25):
            return booksByGenre
        if(book.find("a", {"class": "bookTitle"}) is None):
            continue
        else:
            title = book.find("a", {"class": "bookTitle"}).text
        if(book.find("span", {"class": "greyText smallText"}) is None):
            continue
        else:
            rating = book.find("span", {"class": "greyText smallText"}).text
            regEx = r'(\d+.\d+)'
            rating = re.search(regEx, rating)
        #convert score to float
        if rating and title:
            rating = float(rating.group(1))
            rating = int(rating * 20)
            booksByGenre[genre].append((title, rating))
    return booksByGenre

def main():

    genreNum = sys.argv[1]
    booksByGenre = scrapeBooks(int(genreNum))
    conn = sqlite3.connect('ratings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (title text, score integer, genreID integer)''')
    c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS titleIndex ON books (title)''')
    for genre in booksByGenre:
        for book in booksByGenre[genre]:
            c.execute("INSERT OR IGNORE INTO books VALUES (?, ?, ?)", (book[0], book[1], int(genreNum)))
    conn.commit()

        

if __name__ == "__main__":
    main()