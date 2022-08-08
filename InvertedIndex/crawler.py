#import libraries
from termcolor import colored

#initialise lists for urls from the urls text file
scraping_list= []
scraping_list_final = []

#array to flag removable user links, index links and search links
urls_removed = ["?_", "#", "search", "index", "user"]

def get_links():

    try:

        #initialise array for putting the urls
        urls_list = []

        #open the url text file for parsing
        file = open('urls.txt', 'r').readlines()    

        for url in file:

            #append the urls to urls_list
            urls_list.append(url)
            
            #remove user links, index links and search links
            for url in urls_list:
                for item in urls_removed:
                    if item in url:
                        urls_list = [url for url in urls_list if url != url]

            #append urls to new list for scraping
            for url in urls_list:
                scraping_list.append(url)

        #new list with clean & unique urls
        scraping_list_final =list(dict.fromkeys(scraping_list))

        print(colored('\n----------------Successfully obtained URLs----------------\n' , 'green'))

        return sorted(scraping_list_final)
    
    except:
        print(colored('Error importing URLs from urls.txt file. Restarting.', 'red'))
