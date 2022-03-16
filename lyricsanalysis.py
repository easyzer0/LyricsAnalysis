# Lyrics Analysis - This program analyzes the vocabulary in any given artist's discography
print("Welcome to Lyrics Analysis. This program analyzes the vocabulary in any given artist's discography. Enjoy!")
# import modules
import glob
import os.path
import lyricsgenius
from lyricsgenius import Genius
import json
from collections import Counter
from keys import *

wordList = []

# function to find the lyrics of an artist's top 50 songs
def findLyrics():

    global artistChoice
    global songAmount
    global latest_file

    artistChoice = input("Which artist's lyrics would you like to analyze?: ")
    songAmount = int(
        input("How many of this artist's songs would you like to analyze?: "))

    # Genius API token is inserted
    genius = lyricsgenius.Genius(geniusKey)

    # searches for the songs and saves the lyrics to a json file
    while True:
        try:
            artist = genius.search_artist(
                artistChoice, max_songs=songAmount, sort="popularity")
            break
        except:
            pass

    artist.save_lyrics(filename='artistlyrics.json',
                       overwrite=True, verbose=True)

    list_of_files = glob.glob('/Users/obi/Desktop/Python/LyricsAnalysis/*json')
    latest_file = max(list_of_files, key=os.path.getctime)

# fuction to parse through the JSON file to find the lyrics


def parseJSON():
    # create empty lyrics string to be filled later
    lyrics = ''

    o = open(latest_file)

    data = json.load(o)

    for song in data['songs']:
        lyrics += song['lyrics']
    # remove symbols from the lyrics that skew the word and letter counts
    lyrics = lyrics.lower()

    spec_chars = ["!", '"', "#", "%", "&", "'", "(", ")",
                  "*", "+", ",", ".", "/", ":", ";", "<",
                  "=", ">", "?", "@", "[", "\\", "]", "^", "_",
                  "`", "{", "|", "}", "~", "–"]
    for i in spec_chars:
        lyrics = lyrics.replace(i, '')

    lyrics = lyrics.replace("-", " ")

    lyricsList = lyrics.split('urlcopyembedcopy')

    for i in range(len(lyricsList)):
        lyricsList[i] = lyricsList[i].replace('\n', ' ')

    # create a list that will hold all of the lyrics after being split
    wordListUnedited = lyrics.split(' ')
    wordListUnedited = [x.strip().split('\n') for x in wordListUnedited]

    global wordList

    # create the edited wordList
    for i in wordListUnedited:
        wordList = wordList + i

    wordList = [i.split("/")[0] for i in wordList]
    wordList = [i for i in wordList if not 'embed' in i]

# function that will count the words/letters and show the results to the user
def countWords():

    word_counter = Counter(wordList)
    most_common = word_counter.most_common(5)
    longest_word = max(wordList, key=len)
    longest_word_length = len(longest_word)
    average_words = len(wordList) / songAmount

    wordListSet = set(wordList)
    uniqueWords = len(wordListSet)

    print(artistChoice + " uses an average of " + str(average_words) +
          " words per song, in his " + str(songAmount) + " most popular songs.")

    print(artistChoice + " uses a total of " + str(uniqueWords) +
          " unique words in his " + str(songAmount) + " most popular songs.")
    print(artistChoice + "'s longest word used in those " +
          str(songAmount) + " songs is \"" + str(longest_word) + "\"(" + str(longest_word_length) + " characters).")


# call each of the functions
findLyrics()
parseJSON()
countWords()
