import os
from os.path import exists

from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
from copy import copy
from copy import deepcopy
from os import listdir
from os import chdir
from os import mkdir
from json import dump
from json import load
from ijson import items
from time import time
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from re import split
from os import path
from itertools import product
from itertools import pairwise
from os import getcwd
from math import floor

stemmer = SnowballStemmer("english")  # creating stemmer object
stop_words = set(stopwords.words('english'))  # importing stopwords and putting them in a set

ui,_ =  loadUiType("finalwindow.ui")

class MainApp(QMainWindow , ui ):

    if not path.isdir('./Generated_files'):
        mkdir('./Generated_files')
    global query
    global file_path
    global itr
    global state   # if state = 1 make barral for new inserted file if state = 0 make berrals for previous files
    global rScreenNo
    global data_array
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.UiComponents()
        self.main_page_window()
        # self.tabWidget.tabBar().setVisible(True)
        self.state = 0
        self.query = ""
        self.data_array = [""]
        self.rScreenNo = 0
        self.buttonHandler()
        # self.showResult()
        # urlLink = "<a href=\"http://www.google.com\">http://www.google.com</a>"

    def buttonHandler(self):
        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.searchButton2.clicked.connect(self.searchButton2Clicked)
        self.nextButton.clicked.connect(self.nextButtonHandler)
        self.previousButton.clicked.connect(self.previousButtonHandler)
        self.uploadButton.clicked.connect(self.uploadButtonHandler)
        self.uploadButton2.clicked.connect(self.uploadButtonHandler)
        self.stateButton.clicked.connect(self.stateHomeHandler)

    def UiComponents(self):

        # self.searchButton.clicked.connect(self.search_result_window)
        self.tabWidget.tabBar().setVisible(False)

        # self.uploadButton.setStyleSheet(
        #     "QPushButton {"
        #     "border: 2px solid rgb(51,51,51);"
        #     "border-radius: 5px;"
        #     "color:rgb(255,255,255);"
        #     "background-color: rgb(51,51,51);"
        #     "}"
        #     "QPushButton:hover {"
        #     "border: 2px solid rgb(0,143,150);"
        #     "background-color: rgb(0,143,150);"
        #     "}"
        #     "QPushButton:pressed {"
        #     "border: 2px solid rgb(0,143,150);"
        #     "background-color: rgb(51,51,51);"
        #     "}"
        #     "QPushButton:disabled {"
        #     "border-radius: 5px;"
        #     "border: 2px solid rgb(112,112,112);"
        #     "background-color: rgb(112,112,112);"
        #     "}"
        # )

    def uploadButtonHandler(self):
        print("button Pressed")
        self.open_dialog_box()
        self.data_fun()
    def stateHomeHandler(self):
        self.state = 0
        self.data_fun()

    def open_dialog_box(self):
        fdlg = QFileDialog()
        fdlg.setFileMode(QFileDialog.AnyFile)
        filter = "json(*.json)"
        filename = QFileDialog.getOpenFileName(None, "", "", filter)
        self.file_path = filename[0]
        print(self.file_path)
        self.state = 1

    def showResult(self):
        print("Iterator is : " , self.itr)
        print("rscreenNo is : " , self.rScreenNo)
        if(len(self.data_array) == 1):
            self.noResultLbl.setVisible(True)
        if (self.itr < len(self.data_array)):
            splitText = self.data_array[self.itr].split("\n")
            myUrl = "<a href=\"" + splitText[1] + "\">" + splitText[1] + "</a>"
            self.label1.setText(myUrl)
            self.topicLbl1.setText(str(self.itr) + "- "+splitText[0])
            self.topicLbl1.adjustSize()

        else:
            self.label1.setVisible(False)
            self.topicLbl1.setVisible(False)

        self.itr += 1
        if (self.itr < len(self.data_array)):
            splitText = self.data_array[self.itr].split("\n")
            myUrl = "<a href=\"" + splitText[1] + "\">" + splitText[1] + "</a>"
            self.label2.setText(myUrl)
            self.topicLbl2.setText(str(self.itr) + "- "+splitText[0])
            self.topicLbl2.adjustSize()
        else:
            self.label2.setVisible(False)
            self.topicLbl2.setVisible(False)

        self.itr += 1
        if (self.itr < len(self.data_array)):
            splitText = self.data_array[self.itr].split("\n")
            myUrl = "<a href=\"" + splitText[1] + "\">" + splitText[1] + "</a>"
            self.label3.setText(myUrl)
            self.topicLbl3.setText(str(self.itr) + "- "+splitText[0])
            self.topicLbl3.adjustSize()
        else:
            self.label3.setVisible(False)
            self.topicLbl3.setVisible(False)

        self.itr += 1
        if (self.itr < len(self.data_array)):
            splitText = self.data_array[self.itr].split("\n")
            myUrl = "<a href=\"" + splitText[1] + "\">" + splitText[1] + "</a>"
            self.label4.setText(myUrl)
            self.topicLbl4.setText(str(self.itr) + "- "+splitText[0])
            self.topicLbl4.adjustSize()
        else:
            self.label4.setVisible(False)
            self.topicLbl4.setVisible(False)

        self.itr += 1
        if (self.itr < len(self.data_array)):
            splitText = self.data_array[self.itr].split("\n")
            myUrl = "<a href=\"" + splitText[1] + "\">" + splitText[1] + "</a>"
            self.label5.setText(myUrl)
            self.topicLbl5.setText(str(self.itr) + "- "+splitText[0])
            self.topicLbl5.adjustSize()
        else:
            self.label5.setVisible(False)
            self.topicLbl5.setVisible(False)

        self.itr += 1
        if (self.itr < len(self.data_array)):
            splitText = self.data_array[self.itr].split("\n")
            myUrl = "<a href=\"" + splitText[1] + "\">" + splitText[1] + "</a>"
            self.label6.setText(myUrl)
            self.topicLbl6.setText(str(self.itr) + "- "+splitText[0])
            self.topicLbl6.adjustSize()
        else:
            self.label6.setVisible(False)
            self.topicLbl6.setVisible(False)

        self.itr += 1

        if (self.rScreenNo == int(len(self.data_array) / 6 )):
            print("Print screen no is : " , self.rScreenNo)
            print("answer is : " , int(len(self.data_array) / 6))
            self.nextButton.setEnabled(False)

        if (self.rScreenNo == 0):
            self.previousButton.setEnabled(False)

    def nextButtonHandler(self):
        self.rScreenNo += 1
        print(self.itr)
        self.previousButton.setEnabled(True)
        self.showResult()

    def previousButtonHandler(self):
        self.rScreenNo -= 1
        self.itr -= 12
        self.nextButton.setEnabled(True)
        self.label2.setVisible(True)
        self.topicLbl2.setVisible(True)
        self.label3.setVisible(True)
        self.topicLbl3.setVisible(True)
        self.label4.setVisible(True)
        self.topicLbl4.setVisible(True)
        self.label5.setVisible(True)
        self.topicLbl5.setVisible(True)
        self.label6.setVisible(True)
        self.topicLbl6.setVisible(True)
        self.showResult()

    def main_page_window(self):
        self.tabWidget.setCurrentIndex(0)
        self.noResultLbl.setVisible(False)
        self.itr = 1

    def search_result_window(self):
        self.tabWidget.setCurrentIndex(1)

    def searchButtonClicked(self):
        self.itr = 1
        self.rScreenNo = 0
        if(self.searchBarLe.text() != ''):
            self.noResultLbl.setVisible(False)
            self.label1.setVisible(True)
            self.topicLbl1.setVisible(True)
            self.label2.setVisible(True)
            self.topicLbl2.setVisible(True)
            self.label3.setVisible(True)
            self.topicLbl3.setVisible(True)
            self.label4.setVisible(True)
            self.topicLbl4.setVisible(True)
            self.label5.setVisible(True)
            self.topicLbl5.setVisible(True)
            self.label6.setVisible(True)
            self.topicLbl6.setVisible(True)

            self.searchResultLb.setText(self.searchBarLe.text())
            self.searchResultLb.adjustSize()
            self.query = self.searchBarLe.text()
            self.search_result_window()
            self.searching()
            self.showResult()
        else:
            self.searchBarLe.setText("Write something!!")

    def searchButton2Clicked(self):
        self.nextButton.setEnabled(True)
        self.itr = 1
        self.rScreenNo = 0
        if (self.searchBarLe2.text() != ''):
            self.noResultLbl.setVisible(False)
            self.label1.setVisible(True)
            self.topicLbl1.setVisible(True)
            self.label2.setVisible(True)
            self.topicLbl2.setVisible(True)
            self.label3.setVisible(True)
            self.topicLbl3.setVisible(True)
            self.label4.setVisible(True)
            self.topicLbl4.setVisible(True)
            self.label5.setVisible(True)
            self.topicLbl5.setVisible(True)
            self.label6.setVisible(True)
            self.topicLbl6.setVisible(True)

            self.searchResultLb.setText(self.searchBarLe2.text())
            self.searchResultLb.adjustSize()
            self.query = self.searchBarLe2.text()
            print("sb2 cp" + self.query)
            self.searching()
            self.showResult()
        else:
            self.searchBarLe2.setText("Write something!!")


    # def data_fun(self):
    #     print("inside data function")
    #     print(os.getcwd())               # here we are in project directory
    #     chdir('./Generated_files')
    #     print(os.getcwd())               # here we are in project directory
    #     chdir('../')
    #     print(os.getcwd())               # here we are in project directory

    # def searching(self):
    #     print("in searching")
    #     print(os.getcwd())               # here we are in project directory
    #     chdir('./Generated_files')
    #     print(os.getcwd())               # here we are in project directory
    #     chdir('../')
    #     print(os.getcwd())               # here we are in project directory


    def data_fun(self):
        start = time()

        doc_id = 0
        url_id = 0
        url_id = 0
        word_id = 0

        Lex_dict = {}
        doc_ref = {}
        files_already_read = {}

        print("path in start of data_func " + os.getcwd())

        chdir('./Generated_files')
        Name_of_file = []
        max_barral_size = 0
        if (self.state == 1):
            with open("comp_files.json", 'r') as j:
                files_already_read = load(j)
            Name_of_file = [self.file_path]
            # Name_of_file = [os.path.basename(self.self.file_path)]
            print(files_already_read['1'])
            print(os.path.basename(self.file_path))
            if (os.path.basename(self.file_path) in files_already_read['1']):
                print("file already read")

            files_already_read['1'].append(os.path.basename(self.file_path))  # considering the file to be read
            with open("lexicon.json", 'r') as LEX:
                Lex_dict = load(LEX)
            with open("Doc_ref.json", 'r') as doc:
                doc_ref = load(doc)
                max_barral_size = doc_ref["-1"]

            doc_id = files_already_read['2']
            url_id = files_already_read['3']
            word_id = files_already_read['4']
        else:
            # we are in generated_files folder
            my_new_list = listdir('../sample_data')
            files_already_read['1'] = []
            for x in my_new_list:
                files_already_read['1'].append(x)
            string = "../sample_data/"
            Name_of_file = [string + x for x in my_new_list]
            print(Name_of_file)

        # with open("lexicon.json", 'r') as LEX:
        #     Lex_dict = load(LEX)

        for elements in Name_of_file:  # for every file in the sample_data directory
            print(elements)
            with open(elements, "rb") as f:  # opening each file
                print("file opened")
                objects = items(f, 'item')  # loading only the contents of each article into memory
                for data in objects:  # going through the contents of each article
                    data = data['title'] + data['content']
                    words_list = split(':|;|,|\s|\n|&|\?|\t|-|/|\|@|"|!',
                                       data)  # splitting the contents into words using multiple delimiters
                    for word in words_list:  # going through the list of words
                        temp = "".join(
                            c for c in word if c.isalpha() or c == '.')  # keeping only the alphabet and . in each word
                        temp = copy(temp.lower())
                        if len(temp) > 2 and temp not in stop_words:  # filtering
                            tmp = stemmer.stem(temp)  # stemming the filtered words.
                            if tmp not in Lex_dict:  # if the word is not in lexicon
                                Lex_dict[tmp] = word_id  # insert it in lexicon
                                word_id += 1

        Last_lex_key = list(Lex_dict.keys())[-1]
        Last_lex_word = Lex_dict[Last_lex_key]
        files_already_read['4'] = Last_lex_word
        print(Last_lex_word)
        print("storing the last id of lexicon")

        dump(Lex_dict, open("lexicon.json", "w"))
        end12 = time()
        print(f" Now Runtime of the program is {end12 - start}")

        # if not path.exists("../Generated_files/Doc_ref.json"):
        #     doc_ref[1] = ""  # temporary initialization of dictionary this will wip while writing again the lexicon.
        #     dump(doc_ref, open(r"../Generated_files/Doc_ref.json", "w"))

        forwardIndex = {}  # dictionary for complete forward index:
        forwardIndexWords = {}  # dictionary to store word_ids and hit lists for each article
        for elements in Name_of_file:  # for every file in the sample_data directory
            with open(elements, "rb") as f:
                objects = items(f, 'item')  # loading contents of each article into memory
                for data in objects:  # for every article in the file
                    url = data['title'] + '\n' + data['url']
                    doc_ref[str(doc_id)] = copy(str(url))
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
                    forwardIndex[doc_id] = deepcopy(
                        forwardIndexWords)  # putting wordids and hitlists for each article into forward index
                    doc_id += 1

            with open(elements, "rb") as f:
                urls = items(f, 'item')  # loading urls of articles into memory
                for item in urls:
                    url = item['title'] + '\n' + item['url']
                    doc_ref[str(url_id)] = copy(str(url))  # putting urls into doc ref dictionary
                    url_id += 1

        files_already_read['2'] = doc_id
        files_already_read['3'] = url_id

        dump(files_already_read, open("comp_files.json", "w"))

        end13 = time()
        print(f" Now Runtime of the program is {end13 - start}")

        barrel_size = 2000
        lower_limit = 0
        upper_limit = barrel_size  # upper limit changes in following code :

        Inv_index = {}  # dictionary to store inverted index
        if self.state == 0:
            print("creating barrals for the file")
            while lower_limit < Last_lex_word:
                for docID in forwardIndex:  # for every article
                    for wordID in forwardIndex[docID]:  # for every word present in the article
                        if lower_limit <= wordID <= upper_limit:
                            if str(wordID) not in Inv_index:  # if the word is not already in inverted index
                                Inv_index[str(wordID)] = {}  # create an empty dict with word_id as key
                            Inv_index[str(wordID)][str(docID)] = forwardIndex[docID][
                                wordID]  # put doc_id and hitlist into the dict of correesponding word
                inv_name = "../Generated_files/" + str(upper_limit) + ".json"
                dump(Inv_index, open(inv_name, "w"))  # put inverted index into file
                Inv_index.clear()
                lower_limit += barrel_size
                upper_limit += barrel_size
        doc_ref["-1"] = upper_limit - barrel_size
        if self.state == 1:  # here we make another barrel for the external file insertion.
            print("above" + str(doc_ref["-1"]))

            if not path.exists("../Generated_files/new_file_barrel.json"):
                Inv_index[
                    -1] = {}  # temprary initalization of dictoinary this will wip while writing again the lexicon.
                Inv_index[-1][-1] = []
                dump(Inv_index, open(r"../Generated_files/new_file_barrel.json", "w"))

            with open("../Generated_files/new_file_barrel.json", 'r') as Inv:
                Inv_index = load(Inv)
            for Doc_id in forwardIndex:  # for every article
                for wordID in forwardIndex[Doc_id]:  # for every word present in the article
                    if str(wordID) not in Inv_index:  # if the word is not already in inverted index
                        Inv_index[str(wordID)] = {}  # create an empty dict with word_id as key
                    Inv_index[str(wordID)][str(Doc_id)] = forwardIndex[Doc_id][
                        wordID]  # put doc_id and hitlist into the dict of correesponding word

            dump(Inv_index, open("../Generated_files/new_file_barrel.json", "w"))  # put inverted index into file
            doc_ref["-1"] = max_barral_size

        dump(doc_ref, open("Doc_ref.json", "w"))  # store doc_ref in file

        chdir('../')
        end = time()

        print(f" Now Runtime of the program is {end - start}")
        print("path at end of data_func " + os.getcwd())

    def searching(self):
        print(self.query)
        self.data_array = [""]

        terms = self.query.split()

        start1 = time()

        barrel_size = 2000
        lower_limit = 0
        upper_limit = barrel_size

        docs = {}
        docs_list = []
        total_docs = set()
        temp_docs = {}
        hitlists = {}

        print(os.getcwd())
        chdir('./Generated_files')
        doc_ref = load(open("../Generated_files/Doc_ref.json", "r"))
        Lex_dict = load(open("../Generated_files/lexicon.json", "r"))
        new_barral_exist = 0
        if exists("../Generated_files/new_file_barrel.json"):
            new_barral = load(open("../Generated_files/new_file_barrel.json", "r"))
            new_barral_exist = 1
        req_barrel = {}
        for word in terms:
            temp = "".join(c for c in word if c.isalpha() or c == '.')
            tmp = stemmer.stem(temp.lower())
            if tmp in Lex_dict:
                word_id = int(Lex_dict[tmp])
                if word_id < doc_ref["-1"]:
                    print("Max barrla = " + str(doc_ref["-1"]))
                    barrel_name = r"../Generated_files/" + (str(floor(word_id / barrel_size) * 2000 + 2000)) + ".json"
                    print(os.getcwd())
                    with open(barrel_name, "r") as barrel_file:  # opening word according to word id
                        req_barrel = load(barrel_file)  # loading only the contents of each article into memory
                        docs = req_barrel[str(word_id)]
                        for doc_id in docs:
                            print("1")
                            freq = len(req_barrel[str(word_id)][str(doc_id)])
                            hitlists[doc_id] = []
                            hitlists[doc_id].append(req_barrel[str(word_id)][str(doc_id)])
                            for pos in req_barrel[str(word_id)][str(doc_id)]:
                                if pos < 15:
                                    freq += 10
                            temp_docs[str(doc_id)] = int(freq)
                            print("2")
                if new_barral_exist == 1:
                    if word_id in new_barral:
                        docs = new_barral[str(word_id)]
                        print("4")
                        for doc_id in docs:
                            freq = len(new_barral[str(word_id)][str(doc_id)])
                            if doc_id not in hitlists:
                                hitlists[doc_id] = []
                            hitlists[doc_id].append(new_barral[str(word_id)][str(doc_id)])
                            for pos in new_barral[str(word_id)][str(doc_id)]:
                                if pos < 15:
                                    freq += 10
                            temp_docs[str(doc_id)] = int(freq)
                        print("5")
            req_barrel.clear()
            docs_list.append(deepcopy(temp_docs))
            temp_docs.clear()
            docs_list1 = [x.keys() for x in docs_list]
        print("7")

        total_docs = copy(set(docs_list1[0]).intersection(*docs_list1))
        doc_dict = {}

        for doc in total_docs:
            freq_sum = sum([x[str(doc)] for x in docs_list])
            doc_dict[str(doc)] = freq_sum

        for doc_id1 in total_docs:
            for element in product(x for x in hitlists[doc_id1]):
                for num in [y - x for (x, y) in pairwise(element[0])]:
                    if num < 5:
                        doc_dict[str(doc_id1)] += 15

        doc_dict = sorted(doc_dict.items(), key=lambda x: -x[1])
        for index, doc1 in enumerate(doc_dict):
            self.data_array.append(doc_ref[doc1[0]])

        print(" here - > " + str(len(self.data_array)))
        extra_doc_dict = {}
        # if len(doc_dict) < 20:
        #     extra_docs = copy(set(docs_list1[0]).union(*docs_list1))
        #     extra_docs = extra_docs - set([x[0] for x in doc_dict])
        #     for x in extra_docs:
        #         extra_doc_dict[x] = 0
        #         for doc_list in docs_list:
        #             if x in doc_list:
        #                 extra_doc_dict[x] += doc_list[x]
        #
        #     extra_doc_dict = sorted(extra_doc_dict.items(), key=lambda x: -x[1])
        #     for index, doc1 in enumerate(extra_doc_dict):
        #         self.data_array.append(doc_ref[doc1[0]])
        # print("hello here")
        #
        if len(self.data_array) < 20:
            extra_docs = copy(set(docs_list1[0]).union(*docs_list1))
            extra_docs = extra_docs - set([x[0] for x in doc_dict])
            for x in extra_docs:
                extra_doc_dict[x] = 0
                for doc_list in docs_list:
                    if x in doc_list:
                        extra_doc_dict[x] += doc_list[x]

            extra_doc_dict = sorted(extra_doc_dict.items(), key=lambda x: -x[1])
            for index, doc1 in enumerate(extra_doc_dict):
                self.data_array.append(doc_ref[doc1[0]])
        # print("7")

        print(self.data_array)
        print(len(self.data_array))
        noOfSearches = str(len(self.data_array)-1)
        print(noOfSearches)
        self.numSearchesLbl.setText(str(noOfSearches))
        # TODO: rank the appended articles better
        end1 = time()
        print(f" Now Runtime of the program is {end1 - start1}")
        self.timeLbl.setText(str(end1 - start1))
        self.query = ""
        chdir('../')
        print("path in end of Searching " + os.getcwd())


def main():
    app = QApplication(sys.argv)
    window =  MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()