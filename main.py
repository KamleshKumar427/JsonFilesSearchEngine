import copy
import os
import orjson
import time
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re

start = time.time()

stemmer = SnowballStemmer("english")
stop_words = set(stopwords.words('english'))

Lex_dict = {}                      # dictionary for Lexicon index
os.chdir(r".\sample_data")              # changing path sample_data folder so all files to be read from one place
word_id = 0
doc_id = 0
for file_name in os.listdir():                          # for loop for every file in the sample_data directory
    with open(file_name, "rb") as f:
        data = orjson.loads(f.read())
    for i in range(len(data)):                                  # for every article in the file
        corpus = data[i]["title"] + data[i]["content"]  # data of i th article of the file
        # print(repr(corpus))
        words_list = re.split(':|;|,|\s|\n|&|\?|\t|-|/|\|@|"|!', corpus)
        for word in words_list:  # going through the list of words
            temp = "".join(c for c in word if c.isalpha() or c == '.')
            if temp and len(temp) > 2 and temp.lower() not in stop_words:
                tmp = stemmer.stem(temp.lower())  # stemming the filtered words.
                if tmp not in Lex_dict:  # if the word is not in lexicon
                    Lex_dict[tmp] = word_id  # insert it in lexicon
                    word_id += 1

with open("../Generated_files/lexicon.json", "wb") as f:
    f.write(orjson.dumps(Lex_dict))

doc_ref = {}
forwardIndex = {}                       # dictionary for forward index:
forwardIndexWords = {}  # this dict will contain the word_ids of every article which is opened at that time
for file_name in os.listdir():                          # for loop for every file in the sample_data directory
    with open(file_name, "rb") as f:
        data = orjson.loads(f.read())
    for j in range(len(data)):                                  # for every article in the file
        corpus = data[j]["title"] + data[j]["content"]          # data of i th article of the file
        words_list = re.split(':|;|,|\s|\n|&|\?|\t|-|/|\|@|"|!', corpus)
        forwardIndexWords.clear()
        for index, word in enumerate(words_list):  # going through the whole list of words
            temp = "".join(c for c in word if c.isalpha() or c == '.')
            if temp and len(temp) > 2 and temp.lower() not in stop_words:
                tmp = stemmer.stem(temp.lower())  # stemming the filtered words.
                if Lex_dict[tmp] not in forwardIndexWords:
                    forwardIndexWords[Lex_dict[tmp]] = [index]
                else:
                    forwardIndexWords[Lex_dict[tmp]].append(index)
        forwardIndex[doc_id] = copy.deepcopy(forwardIndexWords)
        doc_ref[str(doc_id)] = copy.deepcopy(data[j]["title"])
        doc_id += 1
        forwardIndexWords.clear()

del Lex_dict        # to free memory
with open("../Generated_files/Doc_ref.json", "wb") as f:
    f.write(orjson.dumps(doc_ref))

Inv_index = {}
for docID in forwardIndex:
    for wordID in forwardIndex[docID]:
        if str(wordID) not in Inv_index:
            Inv_index[str(wordID)] = {}
        Inv_index[str(wordID)][str(docID)] = copy.deepcopy(forwardIndex[docID][wordID])

with open("../Generated_files/Inv_index.json", "wb") as f:
    f.write(orjson.dumps(Inv_index))

end = time.time()
print(f" Now Runtime of the program is {end - start}")
