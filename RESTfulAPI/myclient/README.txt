Instructions for use:

To install the necessary dependencies and run the client program:

-If you do not have python installed, from the links below paste the link that relates to your device in a browser and install it before doing step A:
		
		Windows: https://www.python.org/ftp/python/3.9.2/python-3.9.2.exe
						OR
			https://www.python.org/ftp/python/3.9.2/python-3.9.2-amd64.exe


		MacOS: https://www.python.org/ftp/python/3.9.2/python-3.9.2-macosx10.9.pkg


(A)Assuming you already have python installed, open a terminal, cd into the root directory of the client application and activate the virtual environment as follows:

			"source django/bin/activate"

-Once the virtual environment is activated, run the following:
			"python3 client.py"

You should see a menu like this:

1. Type 'register' to register a new user
2. Type 'login https://sc19msmm.pythonanywhere.com/' to log into your account
3. Type 'logout' to log out of your session
4. Type 'list' to get a list of all modules and their corresponding professors
5. Type 'view' to view ratings for all the professors
6. Type 'average <professor_id> <module_code>' with the required arguments to get the average rating of a professor in a given module
7. Type 'rate <professor_id> <module_code> <year> <semester> <rating>' with the required arguments to rate a professor in a given module

Follow the instructions exactly to use the API.



Name of python anywhere domain: https://sc19msmm.pythonanywhere.com/

Admin username: ammar
Admin email: ammar@email.com
Admin password: ammar

Further Instructions:
For the Module table in the database I had to give each module a unique module code in the 'module_code' field based 
on their years so as to make my implementations work, for example 'CD1 taught in 2017' as per the coursework brief 
becomes 'CD17 taught in 2017' in my implementation, 'CD1 taught in 2018' as per the coursework brief becomes 'CD18 taught in 2018' in my implementation, 
'PG1 taught in 2017' as per the coursework brief becomes 'PG17 taught in 2017' in my implementation. 
Whenever I called view() and average() with the module codes given in the coursework brief 
I couldn’t get them to work as the .get() method returned two module instances and so could not work. 
With the unique module codes my implementations work perfectly.


