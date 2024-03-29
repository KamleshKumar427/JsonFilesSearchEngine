# JsonFilesSearchEngine
# techniques used are according to Google's initial research paper : [Google Research Paper](http://infolab.stanford.edu/~backrub/google.html)
Description: This is a simple search engine that can be used to index a dataset containing json files to obtain relevant search results when a query is entered by a user. It stores a lexicon, inverted index in the form of small barrels, comp file, and some reference files and uses them to obtain search results in responses to a query.

**comp_file** contains the record of files which are already been read by the program, last doc_id and last lexicon index. (These things are being used when a new file is inserted in between already read files)
Lexicon , Doc_ref, comp file and Inverted_index: All of these are saved in json files. Lexicon contain all the unique words from all files being read, with each word assigned a specific word id. Doc_ref stores the URLs of the files against their doc_ids. Forward index is created as a dictionary but not stored in a file. Forward index contains the word id of each word present in an article, along with the lists of word positions against every word id. And in Inverted_index against every word it stores the article id in which it occurs. Inverted_index will also contain the lists of positions of words in a particular article as well. Inverted index is stored in the form of barrels, each named as the highest word_id stored in it. (So that when searching for a word literal only that particular barrel is opened)
	
 
 NOTE :  Before that we were storing the complete Inverted Index in one file. And it was working very well for 100k. But when we tried for 160k articles there were an memory error. There-fore to make it scalable we did a trade-off between speed and scalability. After making the barrels we suffered a little slow down in speed but achieved scalability.

 
Program hierarchy: To beautify the project directory we have created hierarchy using folders and partitions. There is folder with name 

“sample_data” to store the json files, within the same directory as of main code. After the execution of main file a new folder with name 

“Generated_files” will be created in a directory containing main code. if not exist already, this folder will store the files for storing Lexicon, Doc_ref, comp_file, and the barrels of the inverted index. The Generated_files folder also contains a reference document that stores the names of already indexed files and some other relevant information. For inserting a new file there is a button in GUI that opens a dialogue box and allows user to select the json file from anywhere in the disk. A single new barrel is created for storing the data of all next incoming file.

![Picture1](https://user-images.githubusercontent.com/95052507/155599891-402feb4b-5724-4e1a-b707-1d1e6b93dd10.png)
![Picture2](https://user-images.githubusercontent.com/95052507/155599898-1957e997-93c3-4e70-88e7-dde4838fb552.png)
![Picture3](https://user-images.githubusercontent.com/95052507/155599901-1be4d989-9f02-4a14-9a6c-92f4bdf431c5.png)
