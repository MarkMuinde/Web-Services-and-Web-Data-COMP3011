#import libraries
import os
import json
from termcolor import colored


file = {}
#load the text file
def load():

    try:
        #call the file variable
        global file

        #check if the file exists. If so, open & print it. If not, return relevant error message.
        if os.path.exists('index.json') and os.path.getsize('index.json') > 0:
            file = json.load(open('index.json'))
            #file.close()
            print(colored('\n----------------SUCCESS----------------\n' , 'green'))
        
        else:
            print(colored('\nThe inverted index file is empty or does not exist.\nKindly build the index by typing "build" and pressing the Enter button. Restarting.\n' , 'red'))

    except:
        print(colored('Error loading inverted index. Restarting.', 'red'))

def print_word_index(cleaned_word):

    try:

        #check if the word is in the index. If so, print the word's index. If not, return relevant error message.
        if cleaned_word in file:

            print(colored('\n The inverted index for the word %s is :\n' %cleaned_word , 'blue'))

            for location in file[cleaned_word]:
                print (location)
            print(colored('\n----------------SUCCESS----------------\n\n' , 'green'))

        else:
            print(colored('\nThe word has not been found. It either does not exist, or the index was not loaded.\nKindly ensure you have loaded the index by typing "load" and pressing the Enter button.\nRestarting.\n' , 'red'))
    
    except:
        print(colored('Error printing index for %s. Restarting.' %cleaned_word, 'red'))

def find_word(cleaned_word):
    
    try:
        #load the index
        #index = inverter.invert()

        #initialise arrays for printing
        initial_array = []
        printing_array = []

        #check if the word is in the index. If so, print the word's index's URL. If not, return relevant error message.
        if cleaned_word in file:

            print(colored('\n The URLs for the pages containing the word %s is :\n' %cleaned_word , 'blue'))
            for location in file[cleaned_word]:
                initial_array.append(location[0])

            printing_array = list(dict.fromkeys(initial_array))
            for item in printing_array:
                print(item)
            print(colored('\n----------------SUCCESS----------------\n\n' , 'green'))
        
        else:
            print(colored('\nThe word %s could not be found. It either does not exist, or the index was not loaded.\nKindly ensure you have loaded the index by typing "load" and pressing the Enter button.\nRestarting.\n' %cleaned_word , 'red'))

    except:
       print(colored('Error finding URL for the page containing %s. Restarting.' %cleaned_word, 'red'))

def find_words(cleaned_words):
    
    try:

        #initialise arrays for printing
        initial_array = []
        cleaning_array = []
        printing_array = []   

        print(colored('\nThe URLs for the pages containing the search terms %s are: \n' %[term for term in cleaned_words], 'blue'))


        #for each word in the command line argument array
        for cleaned_word in cleaned_words:
            
            #check if the word is in the index. If so, continue. If not, return relevant error message.
            if cleaned_word in file:     

                for location in file[cleaned_word]:

                    #append the word's URL to an initial index
                    initial_array.append(location[0])
            
            else:
                print(colored('\nThe word %s could not be found. It either does not exist, or the index was not loaded.\nKindly ensure you have loaded the index by typing "load" and pressing the Enter button.\n' %cleaned_word , 'red'))
        
        #for each URL in the array
        for item in initial_array:

            #if the URL appears as many times as the count of words being parsed, meaning the all words have been found on a page
            if initial_array.count(item) == len(cleaned_words):
                cleaning_array.append(item)
        
        #remove repeated URLs
        printing_array =list(dict.fromkeys(cleaning_array))
        
        
        #print the URLs
        for item in printing_array:
            print (item)

        print(colored('\n----------------SUCCESS----------------\n\n' , 'green'))
        

    except:
        print(colored('Error finding URL for the page containing %s. Restarting.' %[term for term in cleaned_words], 'red'))