""""
some methods and functions used are acquired from Django documentation
available at https://www.djangoproject.com and https://www.django-rest-framework.org
as well as COMP3011 Lecture Notes
"""

from urllib.request import *
from django.http import *
import json
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate as auth_auth, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import Module, Professor, Rating
from django.db.models import *
from decimal import *
from termcolor import colored

# Create your views here.


@csrf_exempt
def home_page(request):
    return render(request, "home.html")
    
#register a user
@csrf_exempt
def register_backend(request):

    #if HTML method is correct 
    if request.method == 'POST':
        
        #get username, email and password via json
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        
        try:

            #custom functions to check if a username or email is in use
            #wasn't sure if django has that inbuilt
            validate_username(username)
            validate_email (email)

            #create the student
            student = User.objects.create_user(
                username=username, email=email, password=password)

            #save the student
            student.save()

            #http response saying user created successfully
            return HttpResponse('User created successfully', status=201)
            
        
        except:
            #http response saying error creating user
            print(colored('\nUsername or email already in use, please try again\n', 'red'))
            return HttpResponseBadRequest ()

    else:
        #return http response saying method not allowed
        print(colored('Method not allowed', 'red'))
        return HttpResponse('Method not allowed', status=405)


#check if username is already in use
def validate_username(username):
    try:
        username = User.objects.filter(username=username).exists()
        if username is None:
            pass
    except:
        print(colored('\nUsername already in use, please try again\n', 'red'))
        return HttpResponseForbidden('< h1 > Username already in use </h1>')        

#check if email is already in use
def validate_email(email):
    try:
        email = User.objects.filter(email=email).exists()
        if email is None:
            pass
    except:
        print(colored('\nEmail already in use, please try again\n', 'red'))
        return HttpResponseForbidden('< h1 > Username already in use </h1>')


#user login
@csrf_exempt
def login_backend(request):

    #check if method is valid
    if request.method == 'POST':

        #get username and password via json
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        print(username, password)


        try:
            #use django documentation to authenticate a user
            student = auth_auth(username=username, password=password)
            print (student)

            #check if a user is authenticated and is active
            if student is not None and student.is_active:

                #use django documentation to login a user
                auth_login(request, student)

                #return a http response saying credentials accepted
                return HttpResponse ('Credentials Accepted', status = 200)
        except:
            #return http response saying access is forbidden
            print (colored('Credentials Invalid.', 'red'))
            return HttpResponse('Credentials Denied', status=400)

    else: 
        #return http response saying method not allowed
        print(colored('Method not allowed', 'red'))
        return HttpResponse('Method not allowed', status = 405)



#logout
@csrf_exempt
def logout_backend(request):

    #use django documentation to logout a user
    auth_logout(request)
    messages.success(request, 'Logout successful')
    return HttpResponse('Logout successful', status=200)


#list modules and professors
@csrf_exempt
def List_backend(request):

    #return http response saying method not allowed
    if request.method != 'GET':
        print(colored('Method not allowed', 'red'))
        return HttpResponse('Method not allowed', status=405)

    try:
        #get a dict of all the modules
        module_list = Module.objects.all()

        #initialise a list to put the module data
        new_list = []

        for record in module_list:

            #get the data from each record in the dict an append them in a new list
            module_code = record.module_code
            module_name = record.module_name
            year = record.year
            semester = record.semester
            professor_id = record.module_professor.all().values('professor_id')[0]['professor_id']

            item = {'Code': module_code,
                    'Name': module_name, 
                    'Professor': professor_id,
                    'Year': year, 
                    'Semester': semester}
            
            new_list.append(item)
        
        #payload to jsonify
        payload = {'module_list' : new_list}

        #http response if successful
        http_response = HttpResponse (json.dumps(payload))
        http_response['Content-Type'] = 'application/json'
        http_response.status_code = 200
        http_response.reason_phrase = 'OK'
        return http_response

    except:
        #return http response error message 
        print(colored('Error processing List. There may not be any modules in the database to list','red'))
        return HttpResponseBadRequest()


#view professor rating
@csrf_exempt
def view_backend(request):
    
    #return http response saying method not allowed
    if request.method != 'GET':
        return HttpResponse('Method not allowed', status=405)


    try:
        #get an object of all the professors and initialise two lists
        professor_list = Professor.objects.all().values('professor_id')
        id_list = []
        final_list = []

        #get the data from each record in the dict an append them in a new list
        for record in professor_list:

            item = record ['professor_id']
            id_list.append(item)
        
        #use the id data from the id list to get the rating of professors via a queryset and django documentation
        for record in id_list:
            professor = Professor.objects.filter(professor_id = record).get()
            initial_rating = Rating.objects.filter(professor=professor).aggregate(Avg('rating'))
            integer_rating = int(Decimal(initial_rating.get('rating__avg')).quantize(Decimal('1'), rounding = ROUND_HALF_UP))

            #translate the ratings into stars
            if integer_rating == 0:
                star_rating = "-"
            if integer_rating == 1:
                star_rating = "*"
            elif integer_rating == 2:
                star_rating = "**"
            elif integer_rating == 3:
                star_rating = "***"
            elif integer_rating == 4:
                star_rating = "****"
            elif integer_rating == 5:
                star_rating = "*****"

            #put the data into a new list 
            item = {'ID' : professor.professor_id,
                    'Name' : professor.professor_name,
                    'rating' : star_rating}
            
            final_list.append (item)

        #payload to jsonify
        payload = {'view_list': final_list}

        #http response
        http_response = HttpResponse(json.dumps(payload))
        http_response['Content-Type'] = 'application/json'
        http_response.status_code = 200
        http_response.reason_phrase = 'OK'
        messages.success(request, 'View successful')
        return http_response

    except:
        #return http response error message
        print(colored('Error processing View. There may not be any professors in the database to list, or they may have not been rated yet.', 'red'))
        return HttpResponseBadRequest()


#average of a professor
@csrf_exempt
def average_backend(request):

    #http method error
    if request.method != 'POST':
        print('Method not allowed')
        return HttpResponse('Method not allowed', status=405)


    try:
        #get professor_id and module_code via json
        professor_id = json.loads(request.body).get('professor_id')
        module_code = json.loads(request.body).get('module_code')

        #get an object of the specific professor and module from the get method
        professor = Professor.objects.get(professor_id = professor_id)
        code = Module.objects.get(module_code = module_code)

        if professor is not None and code is not None:

            #use the id data from the professor object 
            #and the module data from the module object 
            # to get the  avg rating of professors via a queryset
            initial_rating = Rating.objects.filter(professor=professor, 
                                            module=code).aggregate(Avg('rating'))
            

            if initial_rating:
                integer_rating = int(Decimal(initial_rating.get('rating__avg')).quantize(
                                    Decimal('1'), rounding=ROUND_HALF_UP))
                

                #translate the ratings into stars
                if integer_rating == 0:
                    star_rating = "-"
                if integer_rating == 1:
                    star_rating = "*"
                elif integer_rating == 2:
                    star_rating = "**"
                elif integer_rating == 3:
                    star_rating = "***"
                elif integer_rating == 4:
                    star_rating = "****"
                elif integer_rating == 5:
                    star_rating = "*****"

                #payload to jsonify
                payload = {'average_rating': star_rating}

                #http response
                http_response = HttpResponse(json.dumps(payload))
                http_response['Content-Type'] = 'application/json'
                http_response.status_code = 200
                http_response.reason_phrase = 'OK'
                return http_response
    except:
        #return http response error message
        print(colored('Error processing Average. Professor and Module either do not exist or have been mismatched', 'red'))
        return HttpResponseBadRequest('Professor or module does not exist or have been mismatched')
    
#rate a professor, login required
@csrf_exempt
#@login_required
def rate_backend(request):

    #http method error
    if request.method != 'POST':
        print('Method not allowed')
        return HttpResponse('Method not allowed', status=405)

    try:
        #get data via json
        professor_id = json.loads(request.body).get('professor_id')
        module_code = json.loads(request.body).get('module_code')
        year = json.loads(request.body).get('year')
        semester = json.loads(request.body).get('semester')
        rating = json.loads(request.body).get('rating')

        #get an object of the specific professor and module from the get method
        professor = Professor.objects.get(professor_id=professor_id)
        module = Module.objects.get(module_code=module_code, module_professor = professor, year = year, semester = semester)

        #if the data resolves
        if professor and module:
            Rating.objects.create(
                professor = professor,
                rating = rating,
                module = module
            )
            print (colored('RATE SUCCESSFUL', 'green'))
            return HttpResponse('User created successfully', status=201)

    except:
        #return http response error message
        print(colored('Professor or module does not exist, or have been mismatched. Alternatively, you may have entered the wrong semester or year.', 'red'))
        return HttpResponseBadRequest('Professor or module does not exist, or have been mismatched')
