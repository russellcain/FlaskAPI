"""
For a more concise writeup on my methodologies and reasoning behind this project, please look through the 'readme.txt' file. Thank you for taking the time to play around with this creation! - Russell Cain
"""


### Required libraries
from flask import request, render_template, redirect, Flask 
from flask_sqlalchemy import SQLAlchemy
import os #boots webpage for user in saved browser of choice (not needed)
#----------------------------------------------------------------------

### App Configuration:
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/HaloProject.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #This was annoying me
db = SQLAlchemy(app)
#----------------------------------------------------------------------

### Models:
class OurUsers(db.Model):
	
	""" Database to store and track our users. This ensures clean logins and is tied to the KeyData database as follows: OurUsers.username --> KeyData.creator """

	username = db.Column(db.String(100), unique = True, nullable = False, primary_key = True)
	password = db.Column(db.String(100), nullable = False)

	def __repr__(self):
		""" Command line registering (debugging purposes) """
		return 'Username: %r \t Password: %r \n' % (self.username, self.password) 


class KeyData(db.Model):
	
	""" Database for our user's keys and adjoining values. Each entry is tied to a user and uniqueness is ensured for that user with unique_flag. """

	key = db.Column(db.String(100), unique = False, nullable = False) #Different users should be ablet to store same key
	value = db.Column(db.String(100), unique = False, nullable = False)
	creator = db.Column(db.String(100), unique = False, nullable = False) 
	unique_flag = db.Column(db.String(220), unique = True, nullable = False, primary_key = True) #But no user should be allowed to store the same key twice.

	def __repr__(self):
		""" Command line registering (debugging purposes) """
		return 'OWNER: %r created: \tKey = %r \tValue = %r \n\n' % (self.creator, self.key, self.value)
#----------------------------------------------------------------------


### ### Webpages: 

"""
There are two base pages ('login.html' and 'account.html') for this project:

1) Users are first sent to '/' ('login.html') where they can 
		- Create an account ('/signup')
		- Log into their account ('/login')
		- Delete an existing account ('/')

	The homepage ('/') also populates the usernames of the existing members. 

2) Upon signing up or logging in, users are taken to their ('account.html') page where they can:
		- Enter a new 'key' and 'value' to their database
		- Modify an existing key's value
		- Delete an entry in their database
		- Logout and go back to '/' ('login.html')

Again, error handling and methodology is more fully explained in readme.txt.
"""

### Login functions: 
@app.route("/", methods = ['GET','POST'])
def home():
	return render_template('login.html', current_users = OurUsers.query.all()) 

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
	""" function which verifies uniqueness of username and redirects user to new account page """
	username = request.form.get("new_user")
	if not OurUsers.query.filter_by(username = username).first(): #ensure uniqueness of username
		new_member = OurUsers(username = request.form.get("new_user"), password = request.form.get("new_password"))
		db.session.add(new_member) #add them to OurUsers database
		db.session.commit()
	else:
		return render_template('login.html', error = "Sorry, '%s' is already taken as a username!" %username, current_users = OurUsers.query.all()) # keep them on login page with alert that they can't use that name.
	return render_template("account.html", creator = username) #Success! Send them on to their new account page!


@app.route("/login", methods = ['GET', 'POST'])
def login():
	""" function which verifies user's credentials before sending them to their account page """
	username, password = request.form.get("login_username"), request.form.get("login_password") #api info pull
	user = OurUsers.query.filter_by(username = username).first() #pull user info, assuming they are in database
	if user: #ensure the above query didn't come back as 'None'
		if password == user.password: #authenticate password
			return redirect("/account?creator=%s"% username) #Congrats! Welcome back to your account page
		else:
			error = "Looks like the wrong password! Give it another whirl." #Alert user of wrong password
	else:
		error = "We don't have a '%s' in our system! Would you like to sign up?" % username #can't log in if the account does exist
	return render_template("login.html", error = error, current_users = OurUsers.query.all()) #stay on login page if either of the two errors were triggered.

@app.route("/delete_user", methods = ['POST'])
def delete_user():
	""" function which deletes user and all of their (key,value)s from our two databases """
	username, password = request.form.get("delete_username"), request.form.get("delete_password") #api info pull
	user = OurUsers.query.filter_by(username = username).first()
	if user:
		if password == user.password: #make sure they are authorized to delete the account
			db.session.delete(user) #clear user from OurUser database
			KeyData.query.filter_by(creator = user.username).delete() #Allow future users to occupy that username and post with similar keys in the future by clearing from KeyData table. (rework in future versions)
			db.session.commit() #commit these deletions (see readme.txt for soft delete desires)
			return render_template("login.html", error = "%s deleted!" % username, current_users = OurUsers.query.all()) #return to homepage, alerting user that the user has been deleted.
		else:
			error = "We need the proper password to delete that user!" #alert user authentification failed
	else:
		error = "We can't delete %s! We don't even know them!" % username #need a user to delete a user, eh?
	return render_template('login.html', current_users = OurUsers.query.all(), error = error) 
#----------------------------------------------------------------------


### Account functions
@app.route("/account", methods=["GET", "POST"])
def account():
	""" User's home account page - displays their previous entries and allows them to add more """
	error = False
	creator = request.args['creator'] #pull user's information from url
	entries = KeyData.query.filter_by(creator = creator) #don't allow them to see anyone else's data!

	if request.form: # user would like to add an entry:
		""" Ability for user to add data. Point of the account page so included on this app route. """
		if not KeyData.query.filter_by(unique_flag = '%s_%s' %(creator, request.form.get("new_key"))).first(): #ensure uniqueness of key for this user. 
			new_entry = KeyData(key = request.form.get("new_key"), value = request.form.get("new_value"), creator = creator, unique_flag = '%s_%s' %(creator, request.form.get("new_key")))
			db.session.add(new_entry) #add the new value to the data table
			db.session.commit()
		else:
			error = "You already have that key called '%s'! Try something else, please!" % request.form.get("new_key") #let them know they need a different key value
	return render_template("account.html", entries = entries, creator = creator, error = error)

@app.route("/update", methods=["POST"])
def update():
	""" Allows users to update the value for a given key """
	creator = request.args["creator"] #pull username from url for 'creator' value in table
	newvalue, key = request.form.get("newvalue"), request.form.get("key_to_update") #api info pull
	entry = KeyData.query.filter_by(unique_flag = '%s_%s' %(creator, key)).first()
	entry.value = newvalue #update value associated with the queried key row
	db.session.commit() #reflect change in our database
	return redirect("/account?creator=%s"% creator)

@app.route("/delete_post", methods=["POST"])
def delete_post():
	""" Gives user ability to permanently delete an entry """
	creator = request.args["creator"] #pull username from url for 'creator' value in table
	key = request.form.get("key_to_delete")
	entry = KeyData.query.filter_by(unique_flag = '%s_%s' %(creator, key)).first()
	db.session.delete(entry) #hard delete - future versions ought to rework this.
	db.session.commit()
	return redirect("/account?creator=%s"% creator)
#----------------------------------------------------------------------


#------------------   RUN THE APP HERE!    ----------------------------
db.create_all() #configures databases for user
os.system("pip3 install -r requirements.txt")
os.system("open http://127.0.0.1:5000/") #opens webpage for user
app.run(debug = False) #runs this bad boy! Enjoy!
#----------------------------------------------------------------------

