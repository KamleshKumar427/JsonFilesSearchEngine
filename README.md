# JsonFilesSearchEngine

Group members:
Duaa Omer : 331320
Kamlesh Kumar : 348395
Mastora Alizada : 359696
Abdullah Fazeel : 337188

Description :

Lexicon , Doc_ref, and Inverted_index:
	All of these are saved in json files. Lexicon contain all the unique words from all files being read, with each word assigned a specific word id. Doc_ref stores the URLs of the files against their doc_ids. Forward index is created as a dictionary but not stored in a file. Forward index contains the word id of each word present in an article, along with the lists of word positions against every word id. And in Inverted_index against every word it stores the article id in which it occurs. Inverted_index will also contain the lists of positions of words in a particular article as well.
Program hierarchy:
	To beautify the project directory we have created hierarchy using folders and partitions. There is folder with name “sample_data” to store the json files, within the same directory as of main code. After the execution of main file a new folder with name “Generated_files” will be created in directory containg main code.  if not exist already, this folder will store the files for storing Lexicon , Doc_ref and Inverted_index.