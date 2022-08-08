#import libraries
import time
from termcolor import colored

#import the functions
import functions
import inverter

def main():

    try:
        #print out the command line interface menu
        while True:
            print("\n — — — - - - - Crawling System — — — - - - - \n")
            print(" — — — - - - - Choose one of the following options — — — - - - - \n\n")
            print("1. To crawl the website and build the index, type 'build'\n")
            print("2. To load the inverted index, type 'load'\n")
            print("3. To print the inverted index for a particular word, type 'print <word>'\n")
            print("4. To find a word, type 'find <word>'. The words are case-sensitive.\n")
            print("5. To find more than one word, type 'find <word> <word>'. The words are case-sensitive.\n")
            print("6. To exit the program, press 'Control + C' on your keyboard or type 'exit'\n")
            print("\n")

            #split user input into array for the functions
            user_input = input("Type the command you want to execute from the menu:\n ").split()

            if user_input[0] == 'build':
                start_time = time.time()
                print(colored('\n----------------BUILDING----------------\n' , 'green'))
                inverter.invert()
                print (colored("Time Taken: %i seconds" %(time.time() - start_time) , 'blue'))
            

            elif user_input[0] == 'load':
                print(colored('\n----------------LOADING----------------\n' , 'green'))
                functions.load()


            elif user_input[0] == 'print' and len(user_input) ==2:
                print(colored('\n----------------Parsing Inverted Index to Print Index for %s----------------\n' %user_input[1], 'green'))
                functions.print_word_index(user_input[1])
            

            elif user_input[0] == 'print' and len(user_input) !=2:
                print(colored('\nIncorrect syntax. Restarting.\n' , 'red'))


            elif user_input[0] == 'find' and len(user_input) ==2:
                print(colored('\n----------------Parsing Inverted Index to Find Pages Containing the Term %s----------------\n' %user_input[1], 'green'))
                functions.find_word(user_input[1])


            elif user_input[0] == 'find' and len(user_input) >2:
                print(colored('\n----------------Parsing Inverted Index to Find Pages containing the Terms %s----------------\n' %[term for term in user_input[1:]], 'green'))     
                functions.find_words(user_input[1:])


            elif user_input[0] == 'find' and len(user_input) < 2:
                print(colored('\nIncorrect syntax. Restarting.\n' , 'red'))

            
            elif user_input[0] == 'exit':
                quit()

            else:
                print (colored("\nInvalid choice/syntax, please follow the instructions and try again. Restarting\n", 'red'))

    except KeyboardInterrupt:
        print (colored('\nKeyboard Interrupt Detected. Stopping.\n', 'blue'))


if __name__ == "__main__":
    main()