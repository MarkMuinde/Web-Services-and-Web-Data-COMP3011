#import libraries and classes
import requests
from bs4 import BeautifulSoup
from termcolor import colored

#import function that gets clean links from the url list
import crawler

#initialise lists & dictionaries for inverted_index
raw_index_dict = {}
raw_index_list = []

#blacklisted characters and words
characters = ''':().,^+-1234567890![]{}";\<>=_@$£%*?#/'''

#fucnction to initialise inde
def initialise_index():

    try:
        
        #get links for text crawling
        links = crawler.get_links()

        for link in links:

            #initialise arrays for words
            raw_word_list = []
            cleaned_word_list = []

            #GET request for each link
            html_file = requests.get(link)

            #initialise the request as a BeautifulSoup object and parse it for text
            soup = BeautifulSoup(html_file.content, 'html.parser')
            text = soup.get_text(' ', strip=True)
            word_list = text.split()
        

            #remove the blacklisted characters and append the words to a new list 
            #for cleaning
            for word in word_list:

                if len(word) >= 3:

                    for character in characters:

                        if character in word:
                    
                            word = word.replace(character , '')

                    raw_word_list.append(word)
                    

            #remove top level domains and append them to new list 
            # for index preparation
            for word in raw_word_list:

                if len(word) >= 3:
                    cleaned_word_list.append([word, raw_word_list.count(word)])

            #put the cleaned words in a dictionary and append them to the raw index list
            raw_index_dict = {'url' : link , 'word index' : cleaned_word_list}
            raw_index_list.append(raw_index_dict)

        print(colored('\n----------------Successfully created raw index. Inversion pending----------------\n' , 'green'))

        return raw_index_list

    except:
        print(colored('Error initialising index. Restarting.', 'red'))