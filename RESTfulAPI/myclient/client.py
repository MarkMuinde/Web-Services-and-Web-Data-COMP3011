""""
some methods and functions used are acquired from Django documentation
available at https://www.djangoproject.com and https://www.django-rest-framework.org
as well as COMP3011 Lecture Notes
"""

from urllib.request import *
from django.http import *
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.db.models import *
from decimal import *
import pandas
#from application import *
from termcolor import colored
from django.conf import settings


# Create your views here.

#urls
#base_url = 'http://127.0.0.1:8000/api/'
#register_url = 'http://127.0.0.1:8000/api/register/'
#login_url = 'http://127.0.0.1:8000/api/login/'
#logout_url = 'http://127.0.0.1:8000/api/logout/'
#list_url = 'http://127.0.0.1:8000/api/list/'
#view_url = 'http://127.0.0.1:8000/api/view/'
##average_url = 'http://127.0.0.1:8000/api/average/'
#rate_url = 'http://127.0.0.1:8000/api/rate/'


base_url = 'http://sc19msmm.pythonanywhere.com/api/'
register_url = 'http://sc19msmm.pythonanywhere.com/api/register/'
login_url = 'http://sc19msmm.pythonanywhere.com/api/login/'
logout_url = 'http://sc19msmm.pythonanywhere.com/api/logout/'
list_url = 'http://sc19msmm.pythonanywhere.com/api/list/'
view_url = 'http://sc19msmm.pythonanywhere.com/api/view/'
average_url = 'http://sc19msmm.pythonanywhere.com/api/average/'
rate_url = 'http://sc19msmm.pythonanywhere.com/api/rate/'


#global boolean variable to determine if a user is logged in or not
user_logged_in = False

#register a user
def register():

    #input a username, email and password from command line
    try:
        print("- - - — — — - - - - - - - -User Registration — — — - - - - - - - - - - -\n")
        username = input("Please enter a username: ")
        email = input("Please enter a valid email address: ")
        password = input("Please enter a password (8 characters minimum): ")

        
        #save student data in a structure to be sent over the url
        student = {'username': username,
                    'email': email,
                    'password': password}

        #post the data to the api via a url
        created = requests.Session().post(register_url, data=json.dumps(student))

        #if registration was successful
        if created.status_code != 201:
            print (colored('\nERROR SAVING DATA: Username or Email may already be in use\n', 'red'))

        elif created.status_code ==201:
            print (colored('\n\n DATA SUCCESSFULLY SAVED \n', 'green'))
            settings.configure()
            return HttpResponse(status=201)
    except:
        print (colored('Error registering user!', 'red'))



#user login
def log_in(login_url):

    #call global variable to check if user is logged in
    global user_logged_in

    #input a username and password from command line
    print("- - - — — — - - - - - - - -User Login — — — - - - - - - - - - - -\n")
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")


    #save student data in a structure to be sent over the url
    student = {'username': username,
               'password': password}

    try:
        #post the data to the api via a url
        logged_in = requests.Session().post(login_url, data=json.dumps(student))

        #check if login was successful
        if logged_in.status_code == 200:
            user_logged_in = True
            print(colored('\n\nLOGIN SUCCESSFUL\n', 'green'))
            settings.configure()
            return HttpResponse(status=200)
        else:
            user_logged_in = False
            print(colored('\n\nLOGIN FAILURE\n', 'red'))
            settings.configure()
            return HttpResponse(status=403)
    except:
        print(colored('\n\nLOGIN FAILURE\n', 'red'))



#logout
def log_out():

    #call global variable to check if user is logged in
    global user_logged_in

    #use django documentation to logout a user
    requests.Session().get(logout_url)

    #flag the user as logged out
    user_logged_in = False

    print(colored('\n\nLOGOUT SUCCESSFUL\n', 'green'))
    return HttpResponse(status=200)


#list modules and professors
def List():

    #get the data from the url
    try:
        data = urlopen(list_url)
        data_string = data.read().decode('utf-8')
        data_parsed = json.loads(data_string)

        #parse the json response from the server
        module_list = data_parsed['module_list']

        #print the result in a pandas dataframe
        print(colored('\n\nLIST SUCCESSFUL. RENDERING: \n', 'green'))
        print("-" * 100)
        print(pandas.DataFrame(module_list).reindex(columns=['Code', 'Name', 'Professor', 'Year', 'Semester']))
        print("-" * 100)
        print('\n')
    except:
        print(colored('\n\nError processing List \n', 'red'))


#view professor rating
def view():

    try:
        #open the url data 
        data = urlopen(view_url)
        data_string = data.read().decode('utf-8')
        data_parsed = json.loads(data_string)

        #parse the json response from the server and initialise a new list
        view_list = data_parsed['view_list']
        new_list = []

        #put the data in a new list
        for record in view_list:

            item = {'Professor Code': record['ID'],
                    'Professor Name' : record ['Name'],
                    'Rating': record['rating']}
            new_list.append(item)
        
        #print the result in a pandas dataframe
        print(colored('\n\nVIEW SUCCESSFUL. RENDERING: \n', 'green'))
        print("-" * 100)
        print(pandas.DataFrame(new_list))
        print("-" * 100)
        print('\n')
    except:
        print(colored('\nError processing View. There may not be any professors in the database to list, or they may have not been rated yet.', 'red'))


#average of a professor
def average(professor_id, module_code):

    #put data in structure to sent via post
    data = {
        'professor_id': professor_id,
        'module_code': module_code
    }

    try:
        #send data to url via json
        data_parsed = json.loads(requests.Session().post(average_url, data = json.dumps(data)).text)
        
        #parse the json response from the server
        average_rating = data_parsed['average_rating']

        print(colored('\n\nAVERAGE SUCCESSFUL. RENDERING: \n', 'green'))
        print("The average rating of Professor {0} in module {1} is {2} \n".format(professor_id, module_code, average_rating))
        
    except:
        print(colored('Error processing Average. Professor and Module either do not exist or have been mismatched\n', 'red'))


#rate a professor
def rate(professor_id, module_code, year, semester, rating):

    #call global variable to check if user is logged in
    #global user_logged_in

    #if user_logged_in == False:
        #print('You have to log in to rate a professor.')

    #elif user_logged_in == True:

    # send data to api via url
    try:
        data = {
            'professor_id': professor_id,
            'module_code': module_code,
            'year': year,
            'semester': semester,
            'rating': rating
        }
        requests.Session().post(rate_url, data = json.dumps(data))
    except:
        print(colored('Error rating professor', 'red'))


#main function
@csrf_exempt
def main():

    try:
        #print out the command line interface menu
        while True:
            print(" — — — - - - - Rating System — — — - - - - \n")
            print(" — — — - - - - Choose one of the following options — — — - - - - \n\n")
            print("1. Type 'register' to register a new user\n")
            print("2. Type 'login http://sc19msmm.pythonanywhere.com' to log into your account\n")
            print("3. Type 'logout' to log out of your session\n")
            print("4. Type 'list' to get a list of all modules and their corresponding professors\n")
            print("5. Type 'view' to view ratings for all the professors\n")
            print("6. Type 'average <professor_id> <module_code>' with the required arguments to get the average rating of a professor in a given module\n")
            print("7. Type 'rate <professor_id> <module_code> <year> <semester> <rating>'with the required arguments to rate a professor in a given module\n     Ratings are from 0 - 5")
            print("\n\n")

            user_input = input("Type the command you want to execute from the menu:\n ").split()

            if user_input[0] == 'register':
                register()

            elif user_input[0] == 'login' and len(user_input) == 2:
                log_in(user_input[1])
            
            elif user_input[0] == 'login' and len(user_input) != 2:
                print("Incorrect syntax. Restarting. \n\n")
                main()

            elif user_input[0] == 'logout':
                log_out()

            elif user_input[0] == 'list':
                List()

            elif user_input[0] == 'view':
                view()

            elif user_input[0] == 'average' and len(user_input) == 3:
                average( user_input[1], user_input[2])
            
            elif user_input[0] == 'average' and len(user_input) != 3:
                print("Incorrect syntax. Restarting. \n\n")
                main()

            elif user_input[0] == 'rate' and len(user_input) == 6:
                try:
                    if (5 < int(user_input[5]) or 0 > int(user_input[5])):
                        print ("Rate value out of range. Restarting.\n")
                        main()
                    else:
                        rate(user_input[1], user_input[2],
                            user_input[3], user_input[4], user_input[5])
                except:
                    print(colored('Please enter an integer in the rating field\n', 'red'))

            elif user_input[0] == 'rate' and len(user_input) != 6:
                print("Incorrect syntax. Restarting. \n\n")
                main()

            else:
                print ("Invalid choice/syntax, please follow the instructions and try again \n\n")
                main()
    
    except KeyboardInterrupt:
        print (colored('\nKeyboard Interrupt Detected. Stopping.', 'blue'))


if __name__ == "__main__":
    main()
