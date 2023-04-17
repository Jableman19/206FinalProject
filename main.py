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

def main():
    conn = sqlite3.connect('ratings.db')
    c = conn.cursor()
    c.execute("SELECT")