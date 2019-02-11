### Halo Fullstack Coding Challenge 2019 -- Russell Cain:

**To run in terminal: > 'python3 cain_api.py'**

Runtime requirements: this was written in Python 3.6.3
	- The cain_api.py code will install the required libraries (see requirements.txt) before it runs the app. 

#### Project Description:

- Part 1 - Backend: 

	Write a Python Flask microservice that has two API methods: “get” and “set”.
	
	- The method “get” takes a “key” argument and returns the current value associated with the key, if it exists.
		
  - The method “set” takes two arguments, a “key” and a “value”, and sets the value of “key” to the specified value.
	 	
  The data should be persisted to a database using sqlalchemy.

- Part 2 - Frontend: 

	Design and code a front end for the above key/value API service.

  - Users should be able to load an HTML page and get/set keys.
		
  Use HTML, CSS, and Javascript/JQuery as necessary.

- Part 3 - Advanced: 

	Add a user model to the above service.
	
  - A user should be able to sign up, log in, and log out.
		
  While logged in, they should only be able to 
	
  - Interact with and modify keys they have created 
		
  - Not see or modify another users key/value pairs.
		
  Logged out users should not be able to do anything other than log in.

#### My Notes / Comments / Logic: 
** Further explanation of creative process to come in next github push. **

#### Areas for improvement:

- Login Security: 
	- Right now, someone could just enter 'http://127.0.0.1:5000/account?creator=burt' if they wanted to see all of the keys and values entered by our user, Burt. That isn't fair to Burt.
	- We would create a token or tag which remains `True` for the entirety of the user's session, until they logout.

- Deletion Process:
	- "Soft" deletion is preferred. Should inactivate rows using timestamps. Strategize routine full purges of systems if space ever became an issue. 

- Account recovery:
	- Goodness knows I have trouble remembering passwords. 

- Create a superuser page which can:
	- See all the users:
		- delete users
		- update their passwords
	- See diagnostics on the keys entered by users (number of entries, maybe) or just every entry in KeyData table.

- User Interface:
	- It would be nice to have a sleeker user interface, ideally with a navigation panel on top. Not everyone likes the current sherbet design. Integrating more CSS or Javascript could be fun.

