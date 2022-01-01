import json
import os
from copy import copy
from copy import deepcopy
from math import ceil
from os import listdir
from os import chdir
from json import dump
from ijson import items
from time import time
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from re import split
from os import path
from itertools import product
from itertools import pairwise

def main():

    # TODO: IF FILE EXISTS
    # TODO: insertion
    start = time()

    paths = "C:\Seecs\fall_2021\DSA\DSA Project Work\Project\nela-gt-2020\newsdata\airwars.json"
    state = 0
    stemmer = SnowballStemmer("english")  # creating stemmer object
    stop_words = set(stopwords.words('english'))  # importing stopwords and putting them in a set

    if not os.path.exists('Generated_files'):
        os.makedirs('Generated_files')
    chdir(r".\Generated_files")  # changing path sample_data folder so all files to be read from one place

    files_already_read = {}
    if not os.path.exists("comp_files.json"):
        files_already_read[1] = []
        files_already_read[2] = 0
        files_already_read[3] = 0
        files_already_read[4] = 0

        dump(files_already_read, open(r"comp_files.json", "w+"))

    with open("comp_files.json", 'r') as j:
        files_already_read = json.load(j)

    doc_id = files_already_read['2']
    url_id = files_already_read['3']
    word_id = files_already_read['4']


    # files_already_read['1'].append("hello.json")

    Lex_dict = {}  # dictionary to store lexicon
    if not os.path.exists("lexicon.json"):
        Lex_dict[""] = -1                 # temprary initalization of dictoinary this will wip while writing again the lexicon.
        dump(Lex_dict, open(r"lexicon.json", "w"))

    with open("lexicon.json", 'r') as LEX:
        Lex_dict = json.load(LEX)

    chdir(r"..\sample_data")  # changing path sample_data folder so all files to be read from one place

    print(os.getcwd())

    for file_name in listdir() :  # for every file in the sample_data directory
        if(file_name not in files_already_read['1']):
            print(file_name)
            with open(file_name, "rb") as f:  # opening each file
                objects = items(f, 'item')  # loading only the contents of each article into memory
                for data in objects:  # going through the contents of each article
                    data = data['title'] + data['content']
                    words_list = split(':|;|,|\s|\n|&|\?|\t|-|/|\|@|"|!', data)  # splitting the contents into words using multiple delimiters
                    for word in words_list:  # going through the list of words
                        temp = "".join(c for c in word if c.isalpha() or c == '.')  # keeping only the alphabet and . in each word
                        temp = copy(temp.lower())
                        if len(temp) > 2 and temp not in stop_words:  # filtering
                            tmp = stemmer.stem(temp)  # stemming the filtered words.
                            if tmp not in Lex_dict:  # if the word is not in lexicon
                                Lex_dict[tmp] = word_id  # insert it in lexicon
                                word_id += 1

    Last_lex_key = list(Lex_dict.keys())[-1]
    Last_lex_word = Lex_dict[Last_lex_key]
    print(Last_lex_word)
    files_already_read['4'] = Last_lex_word

    print(os.getcwd())
    dump(Lex_dict, open("../Generated_files/lexicon.json", "w"))

    end12 = time()
    print(f" Now Runtime of the program is {end12 - start}")
    doc_ref = {}
    if not os.path.exists("../Generated_files/Doc_ref.json"):
        doc_ref[1] = ""                 # temprary initalization of dictoinary this will wip while writing again the lexicon.
        dump(doc_ref, open(r"../Generated_files/Doc_ref.json", "w"))
    with open("../Generated_files/Doc_ref.json", 'r') as doc:
        doc_ref = json.load(doc)

    forwardIndex = {}  # dictionary for complete forward index:
    forwardIndexWords = {}  # dictionary to store word_ids and hit lists for each article
    for file_name in listdir():  # for every file in the sample_data directory
        if(file_name not in files_already_read['1']):
            print(file_name)
            files_already_read['1'].append(file_name)
            with open(file_name, "rb") as f:
                objects = items(f, 'item')  # loading contents of each article into memory
                for data in objects:  # for every article in the file
                    data = data['title'] + data['content']
                    words_list = split(':|;|,|\s|\n|&|\?|\t|-|/|\|@|"|!', str(data))
                    forwardIndexWords.clear()
                    for index, word in enumerate(words_list):  # going through the whole list of words
                        temp = "".join(c for c in word if c.isalpha() or c == '.')
                        temp = copy(temp.lower())
                        if len(temp) > 2 and temp not in stop_words:
                            tmp = stemmer.stem(temp)  # stemming the filtered words.
                            if Lex_dict[tmp] not in forwardIndexWords:
                                forwardIndexWords[Lex_dict[tmp]] = [index]
                            else:
                                forwardIndexWords[Lex_dict[tmp]].append(index)
                    forwardIndex[doc_id] = deepcopy(forwardIndexWords)  # putting wordids and hitlists for each article into forward index
                    doc_id += 1
                with open(file_name, "rb") as f:
                    urls = items(f, 'item.url')  # loading urls of articles into memory
                    for url in urls:
                        doc_ref[str(url_id)] = copy(str(url))  # putting urls into doc ref dictionary
                        url_id += 1

    files_already_read['2'] = doc_id
    files_already_read['3'] = url_id

    dump(files_already_read, open("../Generated_files/comp_files.json", "w"))
    dump(doc_ref, open("../Generated_files/Doc_ref.json", "w"))  # store doc_ref in file


    end13 = time()
    print(f" Now Runtime of the program is {end13 - start}")
    # del doc_ref
    del forwardIndexWords

    barre_size = 2000
    lower_limit = 0
    upper_limit = barre_size        # upper limit changes in following code :

    Inv_index = {}  # dictionary to store inverted index
    if(state == 0):
        while (lower_limit < Last_lex_word):
            for docID in forwardIndex:  # for every article
                for wordID in forwardIndex[docID]:  # for every word present in the article
                    if (wordID >= lower_limit and wordID <= upper_limit):
                        if str(wordID) not in Inv_index:  # if the word is not already in inverted index
                            Inv_index[str(wordID)] = {}  # create an empty dict with word_id as key
                        Inv_index[str(wordID)][str(docID)] = forwardIndex[docID][wordID]  # put doc_id and hitlist into the dict of correesponding word
            inv_name = "../Generated_files/" + str(upper_limit) + ".json"
            json.dump(Inv_index, open(inv_name, "w"))  # put inverted index into file
            Inv_index.clear()
            lower_limit += barre_size
            upper_limit += barre_size
    else:           # here we make another barral for the external file insertion.
        if not os.path.exists("../Generated_files/new_file_barrel.json"):
            Inv_index[-1] = {}  # temprary initalization of dictoinary this will wip while writing again the lexicon.
            Inv_index[-1][-1] = []
            dump(Inv_index, open(r"../Generated_files/new_file_barrel.json", "w"))

        with open("../Generated_files/new_file_barrel.json", 'r') as Inv:
            Inv_index = json.load(Inv)
        for Doc_id in forwardIndex:  # for every article
            print(Doc_id)
            for wordID in forwardIndex[Doc_id]:  # for every word present in the article
                if str(wordID) not in Inv_index:  # if the word is not already in inverted index
                    Inv_index[str(wordID)] = {}  # create an empty dict with word_id as key
                Inv_index[str(wordID)][str(Doc_id)] = forwardIndex[Doc_id][
                    wordID]  # put doc_id and hitlist into the dict of correesponding word

        dump(Inv_index, open("../Generated_files/new_file_barrel.json", "w"))  # put inverted index into file


    # Inv-index now contains the Inv - index for new file inserted
    #
    end = time()
    print(f" Now Runtime of the program is {end - start}")

    query = input("Enter your search query: ")

    terms = query.split()
    start1 = time()

    docs = {}
    docs_list = []
    total_docs = set()
    temp_docs = {}
    hitlists = {}

    req_barral = {}
    for word in terms:
        temp = "".join(c for c in word if c.isalpha() or c == '.')
        tmp = stemmer.stem(temp.lower())
        if tmp in Lex_dict:
            word_id = int(Lex_dict[tmp])
            barral_name = r"../Generated_files/" + str(ceil(word_id/barre_size) * 1000) + ".json"
            with open(barral_name, "r") as barral_file:  # opening word according to word id
                req_barral  = json.load(barral_file)  # loading only the contents of each article into memory
            docs = req_barral[str(word_id)]
            print(type(req_barral[str(word_id)]))
            for doc_id in docs:
                freq = len(req_barral[str(word_id)][str(doc_id)])
                print(freq)
                hitlists[doc_id] = []
                hitlists[doc_id].append(req_barral[str(word_id)][str(doc_id)])
                for pos in req_barral[str(word_id)][str(doc_id)]:
                    if pos < 15:
                        freq += 10
                temp_docs[str(doc_id)] = int(freq)
        req_barral.clear()
        docs_list.append(deepcopy(temp_docs))
        temp_docs.clear()

    docs_list1 = [x.keys() for x in docs_list]

    total_docs = copy(set(docs_list1[0]).intersection(*docs_list1))
    doc_dict = {}

    for doc in total_docs:
        freq_sum = sum([x[str(doc)] for x in docs_list])
        doc_dict[str(doc)] = freq_sum

    for doc_id1 in total_docs:
        for element in product(x for x in hitlists[doc_id1]):
            for num in [y-x for (x, y) in pairwise(element[0])]:
                if num < 5:
                    doc_dict[str(doc_id1)] += 15

    doc_dict = sorted(doc_dict.items(), key=lambda x: -x[1])
    for index, doc1 in enumerate(doc_dict):
        print(doc1)
        print(str(index) + " " + doc_ref[doc1[0]])

    print("hello")

    print(doc_dict)

    if len(doc_dict) < 20:
        extra_docs = copy(set(docs_list1[0]).union(*docs_list1))

        extra_docs = extra_docs - set([x for x in doc_dict])

        for index, doc1 in enumerate(extra_docs):
            print(doc1)
            print(str(index) + " " + doc_ref[doc1])

# TODO: rank the appended articles
    end1 = time()
    print(f" Now Runtime of the program is {end1 - start1}")


if _name_ == "_main_":
    main()