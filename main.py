import copy
import os
import json
import ijson
import math
import time
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re

if not os.path.exists('Generated_files'):
    os.makedirs('Generated_files')

start = time.time()
stemmer = SnowballStemmer("english")       # creating stemmer object
stop_words = set(stopwords.words('english'))   # importing stopwords and putting them in a set
Lex_dict = {}                      # dictionary to store lexicon
os.chdir(r".\sample_data")         # changing path sample_data folder so all files to be read from one place
word_id = 0
doc_id = 0
url_id = 0

for file_name in os.listdir():      # for every file in the sample_data directory
    with open(file_name, "rb") as f:  # opening each file
        objects = ijson.items(f, 'item.content')   # loading only the contents of each article into memory
        for data in objects:   # going through the contents of each article
            words_list = re.split(':|;|,|\s|\n|&|\?|\t|-|/|\|@|"|!', data)  # splitting the contents into words using multiple delimiters
            for word in words_list:  # going through the list of words
                temp = "".join(c for c in word if c.isalpha() or c == '.') # keeping only the alphabet and . in each word
                if temp and len(temp) > 2 and temp.lower() not in stop_words:   # filtering
                    tmp = stemmer.stem(temp.lower())  # stemming the filtered words.
                    if tmp not in Lex_dict:  # if the word is not in lexicon
                        Lex_dict[tmp] = word_id  # insert it in lexicon
                        word_id += 1
    with open(file_name, "rb") as f:
        titles = ijson.items(f, 'item.title') # loading title of each file into memory
        for title in titles:      # for the title of every article
            words_list = title.split()
            for word in words_list:  # going through the list of words
                temp = "".join(c for c in word if c.isalnum() or c == '.')
                if temp and len(temp) > 2 and temp.lower() not in stop_words:
                    tmp = stemmer.stem(temp.lower())  # stemming the filtered words.
                    if tmp not in Lex_dict:  # if the word is not in lexicon
                        Lex_dict[tmp] = word_id  # insert it in lexicon
                        word_id += 1

json.dump(Lex_dict, open("../Generated_files/lexicon.json", "w"))

doc_ref = {}
forwardIndex = {}                       # dictionary for complete forward index:
forwardIndexWords = {}     # dictionary to store word_ids and hit lists for each article
for file_name in os.listdir():                          # for every file in the sample_data directory
    with open(file_name, "rb") as f:
        objects = ijson.items(f, 'item.content')  # loading contents of each article into memory
        for data in objects:                                  # for every article in the file
            words_list = re.split(':|;|,|\s|\n|&|\?|\t|-|/|\|@|"|!', data)
            forwardIndexWords.clear()
            for index, word in enumerate(words_list):  # going through the whole list of words
                temp = "".join(c for c in word if c.isalpha() or c == '.')
                if temp and len(temp) > 2 and temp.lower() not in stop_words:
                    tmp = stemmer.stem(temp.lower())  # stemming the filtered words.
                    if Lex_dict[tmp] not in forwardIndexWords:
                        forwardIndexWords[Lex_dict[tmp]] = [index]
                    else:
                        forwardIndexWords[Lex_dict[tmp]].append(index)
            forwardIndex[doc_id] = copy.deepcopy(forwardIndexWords) # putting wordids and hitlists for each article into forward index
            doc_id += 1

    with open(file_name, "rb") as f:
        urls = ijson.items(f, 'item.url') # loading urls of articles into memory
        for url in urls:
            doc_ref[str(url_id)] = copy.copy(str(url)) # putting urls into doc ref dictionary
            url_id += 1

json.dump(doc_ref, open("../Generated_files/Doc_ref.json",  "w"))  # store doc_ref in file

Last_lex_key= list(Lex_dict.keys())[-1]
Last_lex_word = Lex_dict[Last_lex_key]

del doc_ref
del forwardIndexWords
del Lex_dict

mid = time.time()
print(f" Before lexicon :  {mid - start}")

Inv_index = {}    # dictionary to store inverted index
barre_size = 30000
lower_limit = 0
upper_limit = barre_size

while(lower_limit < Last_lex_word):
    for docID in forwardIndex:    # for every article
        for wordID in forwardIndex[docID]:  # for every word present in the article
            if(wordID >= lower_limit and wordID<=upper_limit):
                if str(wordID) not in Inv_index:  # if the word is not already in inverted index
                    Inv_index[str(wordID)] = {}   # create an empty dict with word_id as key
                Inv_index[str(wordID)][str(docID)] = forwardIndex[docID][wordID]  # put doc_id and hitlist into the dict of correesponding word
    inv_name = "../Generated_files/" + str(upper_limit) + ".json"
    json.dump(Inv_index, open(inv_name, "w"))  # put inverted index into file
    Inv_index.clear()
    lower_limit += barre_size
    upper_limit += barre_size

del Inv_index

end = time.time()
print(f" Now Runtime of the program is {end - start}")

Inv_index = {}
for docID in forwardIndex:
    for wordID in forwardIndex[docID]:
        if str(wordID) not in Inv_index:
            Inv_index[str(wordID)] = {}
        Inv_index[str(wordID)][str(docID)] = forwardIndex[docID][wordID]