## import our app variable and database(db) from app package
from app import app, db
## we are allowing access to template folder via flask app and jinja2 (render_template), flash is used to show messages,
from flask import render_template, flash, redirect, request, url_for, json, make_response
## calling the Login/Registration/EditProfile classes from 'forms.py' used in login function below
from app.forms import LoginForm, RegistrationForm, EditProfileForm, SurveyForm, RouteForm
from app.api_keys import bing_key, zillow_key, google_key
from flask_login import current_user, login_user, logout_user, login_required ## importing our current_user and login info
from app.models import User, Assessment  ## importing our User class from models (contains user info, such as passwords)
from werkzeug.urls import url_parse ## importing url_parse for login function
from app.address import Address
from datetime import datetime
from geopy import geocoders
import zillow
import os
import requests
import re
import exifread  ## I likely won't need this
from urllib.parse import quote_plus
from urllib.request import urlretrieve

## importing functions to use for optimizer
from app.siviro import prompt_address


## it creates an association between the URLs given '/' & '/index' and invokes the function below when the URLs are called
@app.route('/', methods=['GET', 'POST'])  ## this is a 'decorator'
@app.route('/index', methods=['GET', 'POST'])  ## they work with the below function
@login_required ## redirects to login page, if not logged in
def index():  ## this is run when the URLs are called ('view function')
    form = SurveyForm() ## instantiating our SurveyForm(), values taken from the users

    if form.validate_on_submit():  ## if form passed via submit in html

        address = Address(form.raw_address.data)  ## instantiating our Address class from address.py with the raw_address data passed from html (via SurveyForm)

        ## assigning the input values to our Assessment database in models.py
        assessment = Assessment(raw_address=form.raw_address.data,
                                lat = address.lat,
                                lng = address.lng,
                                street_number = address.street_number,
                                street_name = address.street_name,
                                city_name = address.city_name,
                                state_abr = address.state_abr,
                                postal_code = address.postal_code,
                                formatted_address = address.formatted_address,
                                agent_est = form.agent_est.data,
                                applicant_est = form.applicant_est.data,
                                google_place_id = address.google_place_id,
                                street_pic = address.street_pic,
                                zillow_estimate = address.zillow_estimate,
                                zillow_baths = address.zillow_baths,
                                zillow_bedrooms = address.zillow_bedrooms,
                                damage = form.damage.data,
                                other_damage = form.other_damage.data,
                                exterior = form.exterior.data,
                                interior = form.interior.data,
                                other_exterior = form.other_exterior.data,
                                other_interior = form.other_interior.data,
                                disaster_type = form.disaster_type.data,
                                disaster_name = form.disaster_name.data,
                                comments = form.comments.data,
                                author=current_user)
        db.session.add(assessment)  ## adding assessment to the db
        db.session.commit()  ## committing this addition
        flash('You have logged an assessment')  ## displaying success
        return redirect(url_for('index'))  ## redirecting to index URL

    ## conducting query from User db (in models.py) to access all assessments
    assessments = current_user.assessment_list().all()

    ## we return, to the html file in our template folder the forms and assessments
    return render_template('index.html', title='Home Page', form=form, assessments=assessments)


## decorator to modify the /login url and override default methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  ## if user logged in already, send to 'index'
        return redirect(url_for('index'))
    form = LoginForm()  ## instantiating LoginForm()
    ## browser sends a 'post' request when 'send' is pressed - returns True and run all validators
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  ## loading user from the database, first returns user object or None
        if user is None or not user.check_password(form.password.data): ## checking user password, whether value present or not
            ## flash is used to display message to user
            flash('Invalid username or password')
            return redirect(url_for('login')) ## redirecting user to login screen
        login_user(user, remember=form.remember_me.data) ## if login info is correct, this will set current user to this user
        next_page = request.args.get('next') ## setting next_page command for login
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page) ## instructing browser to redirect to 'index'
    ## returning the title and form info to the html file
    return render_template('login.html', title='Sign In', form=form)


## decorator to call the logout method
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


## decorator to modify the /register url and override default methods
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  ## verifying user isn't logged in
        return redirect(url_for('index'))
    form = RegistrationForm() ## importing user information from RegForm
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data) ## setting user info
        user.set_password(form.password.data) ## setting user password
        db.session.add(user) ## adding user to db
        db.session.commit() ## committing user to db
        flash('Congratulations, you are now a registered user!') ## displaying text to user
        return redirect(url_for('login')) ## redirecting to 'login' page
    return render_template('register.html', title='Register', form=form)


## this decorator has a dynamic input <username>
@app.route('/user/<username>')
@login_required  ## requires logged in users to access
## this contains the info that is attached to the _post html file
def user(username):
    ## database query to validate user given or send 404 error
    user = User.query.filter_by(username=username).first_or_404()
    assessments = current_user.assessment_list().all()
    return render_template('user.html', user=user, assessments=assessments)


## this decorator executes the function right before the view function
@app.before_request ## before_request executes before any view function
def before_request():
    if current_user.is_authenticated:  ## checking if user is logged in
        current_user.last_seen = datetime.utcnow() ## setting last_seen to current time
        db.session.commit() ## committing time


## standard
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required  ## requires logged in users to access
def edit_profile():
    form = EditProfileForm(current_user.username) ## setting form to our object class, passing in the current username to validate
    if form.validate_on_submit():  ## if form value is true
        current_user.username = form.username.data ## change username
        current_user.title = form.title.data ## change title
        db.session.commit()  ## commit the change to the database
        flash('Your changes have been saved.')  #display message
        return redirect(url_for('edit_profile')) ## go back to edit_profile page
    elif request.method == 'GET':  ## if request method is 'get'
        form.username.data = current_user.username ##impute current info
        form.title.data = current_user.title ##impute current info
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)



''' The below code has not been utilized fully.  This can be used to loop in the route_optimizer 'SIVIRO' - likely need to incorporate Javascript into the HTML to utilize a Dynamic Field for Flask'''

## this is the route function for our optimizer
@app.route('/optimizer', methods=[ 'POST'])
@login_required ## redirects to login page, if not logged in
def optimizer():  ## this is run when the URLs are called ('view function')
    form = RouteForm() ## instantiating our RouteForm()
    if form.validate_on_submit():  ## if form passed

        ## these four lines of code are used to interact with the Javascript in the html template 'optimizer'
        tot_sites = int(request.form.get('num_sites'))
        choices = [('device{}'.format(i), i) for i in range(tot_sites)]
        response = make_response(json.dumps(choices))
        response.content_type = 'application/jsons'


        ## taking in inputs from web form submission
        origin = form.origin.data
        address = form.addresses.data
        #origin_return = form.origin_return.data
        return_location = form.return_location.data

        ## uses function from siviro code to return url string of google route map
        map_url = prompt_address(origin=origin, web_dicta=address, final_destination=return_location)

        ## assigning the input values to our Optimizer database in models.py
        optimizer = Optimizer(map_url = map_url)
        db.session.add(optimizer)  ## adding assessment to the db
        db.session.commit()  ## committing this addition
        flash('Your optimal route')  ## displaying success
        return redirect(url_for('optimizer'))  ## redirecting to index URL

    ## conducting query from User db (in models.py) to access the opt_route
    #opt_route = current_user.route_optimizer().all()

    ## we return, to the html file in our template folder the forms and assessments
    return response
    #return render_template('optimizer.html', title='Site Visit Route Optimizer', form=form) #opt_route=opt_route)



@app.route('/optimizer', methods=['GET'])
def route_input():
    form = RouteForm() ## instantiating our RouteForm()
    return render_template('optimizer.html', form=form)
