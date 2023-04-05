import requests
from bs4 import BeautifulSoup
import time
import json
import sqlite3
import re

def GetGameList(APIKEY):
    gamesDict = {}
    genres = [("Horror", 83 ), ("Thriller", 123), ("Comedy", 120), ("Romance",122), ("Action", 1)]
    for genre in genres:
        #clear cache
        #wait 1 second to avoid rate limiting
        time.sleep(1)
        url = "https://api.mobygames.com/v1/games?format=id&genre=" + str(genre[1]) + "&limit=100&api_key=" + APIKEY
        response = requests.get(url)
        #make response to dictionary format
        newDict = json.loads(response.text)
        gamesDict[genre[0]] = newDict['games']
    return gamesDict

def scrapeGenre(gameList):
    #create bs4 object
    scores = []
    for game in gameList:
        print("Scraping game: " + str(game))
        time.sleep(1)
        url = "https://www.mobygames.com/game/" + str(game)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        #find score
        score = soup.find("div", {"class": "mobyscore"})
        if score is not None:
            score = score.text
            regEx = r'(\d+.\d+)'
            score = re.search(regEx, score)
            #convert score to float
            if score:
                score = float(score.group(1))
                score = int(score * 10)
                scores.append(score)
            else:
                #remove game from list
                gameList.remove(game)
    return scores

def main():

    APIKEY = "YOUR API KEY HERE"
    
    gamesByGenre = GetGameList(APIKEY)
    print(gamesByGenre)
    # iterate through dictionary and scrape the score for each game
    scoresByGenre = {}
    for genre in gamesByGenre:
        scoresByGenre[genre] = scrapeGenre(gamesByGenre[genre])
    print(scoresByGenre)

    #make database for games listing game id, genre, and score
    conn = sqlite3.connect('games.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE games (id integer, genre text, score integer)''')
    for genre in scoresByGenre:
        i = 0
        for score in scoresByGenre[genre]:
            c.execute("INSERT OR IGNORE INTO games VALUES (?, ?, ?)", (gamesByGenre[genre][i], genre, score))
            i += 1
    conn.commit()

        

if __name__ == "__main__":
    main()