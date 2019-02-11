### Halo Fullstack Coding Challenge 2019 -- Russell Cain:

**To run in terminal: > 'python3 cain_api.py'**

*Runtime requirements:* 

  - Project created using Python 3.6.3
  
  - `cain_api.py` will install the required libraries (see `requirements.txt`) before running the app via the computer's default browser. 

#### Project Description:

- Part 1 - Backend: 

	Write a Python Flask microservice that has two API methods: `get` and `post`.
	
	- The method `get` takes a `key` argument and returns the current value associated with the key, if it exists.
		
  - The method `post` takes two arguments, a `key` and a `value`, and sets the value of `key` to the specified value.
	 	
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

I felt this project called for two main webpages: a homepage which allows people to login or signup and an account page which allows them to make/edit/delete just their entries into the database. As this was my first Flask application, I wanted to avoid using the login libraries, allowing myself to grabble with verification and the like. Additionally, in conversations with Dennis the position I am interviewing for appeared to be more back-end-oriented, leading me to shirk some of the front-end aspects of this website a bit (my apologies). 


Moving on, it appeared to me to be easiest if we initialized two databases: one which keeps track of the users and another which houses any of the entries they submitted in their account page. The columns for the user database were restricted to just username and password, but could certainly be expanded to include registration time; this added value would aid in soft deletes of users or an understanding of our customers in the future. The KeyData database needs to at least include 'Key' and 'Value'. However, we want to include a 'creator' column, which is tied to the 'username' column of the OurUser data table. This helps us only display their entries within their account page, instead of allowing every user to see other people's values. Lastly, we need to enforce uniqueness of entries in the KeyData field, but this should be user specific. For example, if everyone used this platform to store their contacts and two users were fortunate enough to befriend Dennis, a simple uniqueness clause on the 'key' would keep each from entering 'Dennis' into the table. For this reason, we make a unique id column which concatenates the 'key' and the 'creator', ensuring that the user maintains uniqueness within their own posts, but not across users. 

From here, the api was built without many other hitches. It struck me that since users should be able to alter key values, it would be best to display all of the current rows in a table - an alteration which somewhat absorbed the api function of 'get'ting a key and returning the value. Again, I apologize for this deviation from the project statement. With regards to the code layout, I tried to separate out each function, providing them with their own app route. The one exception to this is the data entry function within the account page as I see it to be the primary function of the page. Beyond that, I hope the layout of the code is clean and the logic intuitive. Please reach out if anything requires explanation. 

As a final note I'd like to say thank you! I had been reading up on Flask for my current position and was really hankering to create something in it. Further, thank you for taking the time to read this and consider my application. It wouldn't be a complete project in my mind if I didn't mark areas for improvement below.

#### Areas for improvement:

- Login Security: 
	- Right now, someone could just enter 'http://127.0.0.1:5000/account?creator=burt' if they wanted to see all of the keys and values entered by our user, Burt. That isn't fair to Burt.
	- We would create a token or tag which remains `True` for the entirety of the user's session, until they logout.
	- This token could be passed between urls through valid api processes. We would then check that this is included in the url when a page is loaded. (However, we then have the problem that someone could enter the url 'http://127.0.0.1:5000/account?creator=burt?verified=True)
	- For this reason, we might want to look into hashing user passwords and displaying parts of them in the url so you couldn't fake admittance into another's account page unless you know their password. 

- Deletion Process:
	- "Soft" deletion is preferred. Should inactivate rows using timestamps. Strategize routine full purges of systems if space ever became an issue. 
	- This would alter the two tables with a timestamp element.

- Account recovery:
	- This could be achieved through linking to an email account, offering up verification question, or creating a super user to oversee the other users. The first two would be simpler forms which would add columns to OurUsers table. Creating a superuser would not alter the tables, but would include logic which renders the account page differently, also displaying the alter/delete table, but populated with OurUsers values, instead of the current configuration which houses their KeyData rows. (This warrants its own bullet point, I think).

- Create a superuser page which can:
	- See all the users:
		- delete users
		- update their passwords
	- See diagnostics on the keys entered by users (number of entries, maybe) or just every entry in KeyData table.

- User Interface:
	- It would be nice to have a sleeker user interface, ideally with a navigation panel on top. Not everyone likes the current sherbet design. Integrating more CSS or Javascript could be fun.

