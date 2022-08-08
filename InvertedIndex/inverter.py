#import libraries
import os
import json
from termcolor import colored

#import function that gets the index
import initialiser

#initialise lists & dictionaries for inverted_index
inverted_index = {}

def invert():

    try:

        #get raw index for inverting
        raw_index_list = initialiser.initialise_index()

        #invert and append to index, then send to text file
        #the index has a range of 180
        for url in range(len(raw_index_list)):

            for cleaned_word in raw_index_list[url]['word index']:

                if cleaned_word[0] in inverted_index:        
                        inverted_index[cleaned_word[0]].append([raw_index_list[url]['url'], cleaned_word[1]])
                        
                elif cleaned_word[0] not in inverted_index:
                    inverted_index[cleaned_word[0]] = [[raw_index_list[url]['url'], cleaned_word[1]]]
        

        #create or edit the inverted index text file
        if os.path.exists('index.json'):
            file = open ("index.json", "w")
            json.dump(inverted_index, file)
            print(colored('\n----------------Successfully inverted the index and written it to "index.json"----------------\n' , 'green'))
        
        else:
            file = open ("index.json", "x")
            json.dump(inverted_index, file)
            print(colored('\n----------------Successfully inverted the index and written it to "index.json"----------------\n' , 'green'))

        return inverted_index
    
    except:
        print(colored('Error inverting index. Restarting.', 'red'))
