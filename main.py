from copy import copy
from copy import deepcopy
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
    start = time()

    stemmer = SnowballStemmer("english")  # creating stemmer object
    stop_words = set(stopwords.words('english'))  # importing stopwords and putting them in a set
    Lex_dict = {}  # dictionary to store lexicon
    chdir(r".\sample_data")  # changing path sample_data folder so all files to be read from one place
    word_id = 0
    doc_id = 0
    url_id = 0

    for file_name in listdir():  # for every file in the sample_data directory
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

    dump(Lex_dict, open("../Generated_files/lexicon.json", "w"))

    end12 = time()
    print(f" Now Runtime of the program is {end12 - start}")
    doc_ref = {}
    forwardIndex = {}  # dictionary for complete forward index:
    forwardIndexWords = {}  # dictionary to store word_ids and hit lists for each article
    for file_name in listdir():  # for every file in the sample_data directory
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

    dump(doc_ref, open("../Generated_files/Doc_ref.json", "w"))  # store doc_ref in file
    end13 = time()
    print(f" Now Runtime of the program is {end13 - start}")
    # del doc_ref
    del forwardIndexWords
    # del Lex_dict

    Inv_index = {}  # dictionary to store inverted index
    for docID in forwardIndex:  # for every article
        for wordID in forwardIndex[docID]:  # for every word present in the article
            if str(wordID) not in Inv_index:  # if the word is not already in inverted index
                Inv_index[str(wordID)] = {}  # create an empty dict with word_id as key
            Inv_index[str(wordID)][str(docID)] = forwardIndex[docID][
                wordID]  # put doc_id and hitlist into the dict of correesponding word

    dump(Inv_index, open("../Generated_files/Inv_index.json", "w"))  # put inverted index into file
    # del Inv_index
    del forwardIndex

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

    for word in terms:
        print(word)
        temp = "".join(c for c in word if c.isalpha() or c == '.')
        tmp = stemmer.stem(temp.lower())
        if tmp in Lex_dict:
            word_id = int(Lex_dict[tmp])
            docs = Inv_index[str(word_id)]
            for doc_id in docs:
                freq = len(Inv_index[str(word_id)][str(doc_id)])
                hitlists[doc_id] = []
                hitlists[doc_id].append(Inv_index[str(word_id)][str(doc_id)])
                for pos in Inv_index[str(word_id)][str(doc_id)]:
                    if pos < 15:
                        freq += 10
                temp_docs[str(doc_id)] = int(freq)
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
            for num in [y-x for (x, y) in pairwise(element)]:
                print(num)
                if num < 5:
                    doc_dict[str(doc_id1)] += 15

    doc_dict = sorted(doc_dict.items(), key=lambda x: -x[1])
    for index, doc1 in enumerate(doc_dict):
        print(doc1)
        print(str(index) + " " + doc_ref[doc1[0]])

    end1 = time()
    print(f" Now Runtime of the program is {end1 - start1}")


if __name__ == "__main__":
    main()
