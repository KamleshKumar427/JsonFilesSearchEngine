import copy
import os
import json
import ijson
import time
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
from functools import reduce

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
        objects = ijson.items(f, 'item')   # loading only the contents of each article into memory
        for data in objects:   # going through the contents of each article
            data = data['title'] + data['content']
            words_list = re.split(':|;|,|\s|\n|&|\?|\t|-|/|\|@|"|!', data)  # splitting the contents into words using multiple delimiters
            for word in words_list:  # going through the list of words
                temp = "".join(c for c in word if c.isalpha() or c == '.') # keeping only the alphabet and . in each word
                if temp and len(temp) > 2 and temp.lower() not in stop_words:   # filtering
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
        objects = ijson.items(f, 'item')  # loading contents of each article into memory
        for data in objects:                                  # for every article in the file
            data = data['title'] + data['content']
            words_list = re.split(':|;|,|\s|\n|&|\?|\t|-|/|\|@|"|!', str(data))
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

# del doc_ref
del forwardIndexWords
# del Lex_dict

Inv_index = {}    # dictionary to store inverted index
for docID in forwardIndex:    # for every article
    for wordID in forwardIndex[docID]:  # for every word present in the article
        if str(wordID) not in Inv_index:  # if the word is not already in inverted index
            Inv_index[str(wordID)] = {}   # create an empty dict with word_id as key
        Inv_index[str(wordID)][str(docID)] = forwardIndex[docID][wordID]  # put doc_id and hitlist into the dict of correesponding word

json.dump(Inv_index, open("../Generated_files/Inv_index.json", "w"))     # put inverted index into file
# del Inv_index
del forwardIndex

end = time.time()
print(f" Now Runtime of the program is {end - start}")

query = input("Enter your search query: ")
terms = query.split()

docs = {}
docs_list = []
total_docs = set()
temp_docs = {}

for word in terms:
    temp = "".join(c for c in word if c.isalpha() or c == '.')
    tmp = stemmer.stem(temp.lower())
    if tmp in Lex_dict:
        word_id = int(Lex_dict[tmp])
        docs = Inv_index[str(word_id)]
        for doc_id in docs:
            freq = len(Inv_index[str(word_id)][str(doc_id)])
            for pos in Inv_index[str(word_id)][str(doc_id)]:
                if pos < 20:
                    freq += 10
            temp_docs[str(doc_id)] = int(freq)
    docs_list.append(copy.deepcopy(temp_docs))
    temp_docs.clear()

for doc_list in docs_list:
    total_docs = set(docs_list[0].keys()).intersection(set(doc_list.keys()))

end1 = time.time()
print(f" Now Runtime of the program is {end1 - end}")
doc_dict = {}
freq_sum = 0
for doc in total_docs:
    freq_sum = sum([x[str(doc)] for x in docs_list])
    doc_dict[str(doc)] = freq_sum

doc_dict = sorted(doc_dict.items(), key=lambda x: -x[1])
for index, doc1 in enumerate(doc_dict):
    print(doc1)
    print(str(index) + " " + doc_ref[doc1[0]])
