import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import re
import random

def scrapeBooks():
    genres = ['Horror', 'Thriller', 'Comedy', 'Romance', 'Action']
    booksByGenre = {}
    for genre in genres:
        booksByGenre[genre] = []
        pageLB = 1
        pageUB = 15
        for i in range(0, 2):
            print("Scraping genre: " + genre)
            time.sleep(1)
            randomPage = random.randint(pageLB, pageUB)
            url = "https://www.goodreads.com/shelf/show/" + genre + "?page=" + str(randomPage)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            #find score
            books = soup.find_all("div", {"class": "elementList"})
            for book in books:
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
            pageLB = 16
            pageUB = 30
    return booksByGenre

def main():

    booksByGenre = scrapeBooks()

    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS books''')
    c.execute('''CREATE TABLE IF NOT EXISTS books (title text, genre text, score integer)''')
    for genre in booksByGenre:
        for book in booksByGenre[genre]:
            c.execute("INSERT OR IGNORE INTO books VALUES (?, ?, ?)", (book[0], genre, book[1]))
    conn.commit()

        

if __name__ == "__main__":
    main()