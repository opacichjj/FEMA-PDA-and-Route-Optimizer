# Site Visit Operation

Contained in this README.md
- How to run the package
- Basic structure/info
- How to migrate/upgrade database


### To run the package

Everything contained in the 'app' folder is utilized to run our Flask application, Site Visit 2.0.  Follow the below steps to operate:

1) Ensure that you start on the command line from /Site_visit_2.0 folder.

2) The libraries needed to run this should be contained in a virtual environment (venv).  Once you install the virtual environment, you can activate the virtual machine by typing source bin/venv/activate.  This will put you in the venv environment.

3) In the 'app' folder, locate the api_keys.py file and enter the appropriate API keys.  Each API requires, specific keys.  If you get an error with the keys later, please verify the correct access key has been obtained.

4) To run the package, type 'flask run.'  Note: the command 'FLASK_APP' does not need to be entered as this command is called automatically in file .flaskenv.

5) You will likely get errors for libraries that were loaded in prior to creating venv.  Use PyPI to get the 'pip install' information for each library needed.

6) Once all the libraries are loaded, type 'flask run' again.  You should see some code run that ends in a local IP address.

7) Go to a web browser and enter in localhost:5000.  This should take you to the Login page.

8) You have successfully accessed Site Visit 2.0!


### Basic structure/info

config.py, .flaskenv, microblog.py, & app/__init__.py
  - These scripts are used to initiate the app

app folder
  - Contains all the python scripts and html templates to run the application

app/address.py
  - Takes in an address and utilizes Google and Zillow APIs to gather information on coordinates, property information, and location picture.

app/api_keys.py
  - Insert API keys here

app/errors.py
  - This handles our 404 and 500 http errors

app/forms.py
  - This script holds the input fields that are displayed via html.  
  - These forms are often called in routes.py to capture information to be processed and transferred to our Database

app/models.py
  - This script is used to create our database tables with appropriate relationship links
  - Can be queried via routes.py to gather information to display on the web pages

app/routes.py
  - This is a series of functions that are used take in data from other sources and 'route' it to the html templates

app/siviro.py
  - Uses the google API to return an optimal travel route based on the given inputs
  - It is integrated directly with 'routes.py' to process the inputs provided from other scripts
  - It currently accepts 3 inputs (origin, addresses_list(in dictionary form), and return_location) and returns a link to a custom route link for googlemaps.
  - This link is currently set up to enter a database to be stored
  - You can test this code in a Jupyter notebook, if you pull all of the functions in.  Enter the inputs into 'prompt_address()' to get output.

app.state_info.py
  - This file was created to store all applicable state information to create drop down menus for our forms.
  - It currently contains a list of states
  - Could be expanded to take in cities/counties for all states

images folder
  - currently holds all of our database links for photos
  - a better, more dynamic file storing system should be evaluated

templates/_post.HTML
  - displays the picture and assessment forms that have previously been entered
  - this is placed inside the user.html template

templates/404.html & template/500.HTML
  - These are used to display our error codes

templates/base.html
  - Essentially our navigation bar
  - It will change as user login status changes
  - It gets extended to virtually all other html templates

templates/edit_profile.html
  - Contains the information for updating a profile

templates/index.html
  - This is our main input form
  - All assessment inputs are routed through this form

templates/login.html
  - This contains the fields and output for our login form

templates/optimizer.html
  - This is a non-functioning template
  - To create dynamic fields, we'll likely need Javascript/Ajax capabilities to render
  - Currently contains a generic error code when clicked on

templates/register.html
  - Generates our registration form
  - Uses a wtf_quick form which automatically places the entry field and formatting
  - You may want to look into this form and see if it can be exported to other simple templates (cleaner code)

templates/user.html
  - Contains the user information, including assessment log
  - Includes (and loops through) the assessment info contained in _post.html

migrations folder
  - Contains all versions of our database.  You can reference back to previous versions, in the event an error is made.

venv folder
  - Contains all of the python extensions related to this package

### Upgrading Database with new fields/inputs

The database management is incredibly easy.  Any fields that you would like to adjust or change can be adjusted as you see fit by deleting all associated table column information.  The database columns are mainly found in models.py (where they're created) and routes.py (where they're assigned values and committed tot he dtabase)

To officially make the changes for your app, all changes must be migrated and then updated.  To do this, you can follow these steps:

1) Ensure you are in the 'Site_Visit_2.0' directory.

2) Type 'flask db migrate'.  You should see a list of the added and deleted columns.

3) Type 'flask db upgrade'.  You should see a confirmation and you're done!  If an error occurs referring to not having a certain column or table (either here or while running Flask), proceed to the next step.  

4) Locate the current migration by typing in 'flask db current.'  If it doesn't say (head) at the end of the migration code (e.g. b8f2a201eb31 (head) ) then you will need to identify the head

5) Type 'flask db heads' to identify the migration head.  If this number is different than the 'current' migration code, then we will address this.

6) Type 'flask db stamp heads' to force your current migration to the be the head.  Assuming this has been done, the error messages should be gone.  Run Flask again.  If there are any further issues related to the database, refer to SQLAlchemy's documentation.
