from datetime import datetime ## importing datetime to use in Assessment class
from app import db, login  ## importing db and login from app/__init__.py
from werkzeug.security import generate_password_hash, check_password_hash  ## importing password hashing library, used in User class
from flask_login import UserMixin  ## importing UserMixin class that implements four required items for flask_login (is_authenticated, is_active, is_anonymous, and get_id())

## User inherits from db.Model from Flask-SQLAlchemy
## creates our initial database structure/schema. this is also the user table
class User(UserMixin, db.Model):
    ## we create fields here as instances of db.Column class for User table
    id = db.Column(db.Integer, primary_key=True) ## setting our primary key for SQL database
    ## these are 2 unique fields that are indexed (important for queries)
    username = db.Column(db.String(64), index=True, unique=True) ## string capped at 64 characters
    email = db.Column(db.String(120), index=True, unique=True)
    ## we use password_hash as a security protocol, we will not store in db
    password_hash = db.Column(db.String(128))

    ## these are not db fields, but high level views of user relationship (will allow us to call the 'many' from 'one')
    assessments = db.relationship('Assessment', backref='author', lazy='dynamic')
    optimizer = db.relationship('Optimizer', backref='author', lazy='dynamic')

    title = db.Column(db.String(80))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  ## this method tells pyhon how to print objects of this class
        return (f'<User {self.username}>')

    ## method that sets a password for User, using encrypted password_hasing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) ##assigning the hashed password to the user

    ## method of User that checks password entry
    def check_password(self, password):
        ## returns boolean response to password entry vs. stored value
        return check_password_hash(self.password_hash, password)

    ## I neeed to loop this in to the posts
    def assessment_list(self):
        ## returns all assessments attached to user in desc order
        return Assessment.query.filter(
                Assessment.user_id== self.id).order_by(
                    Assessment.timestamp.desc())

    def route_optimizer(self):
        ## returns the most recent optimized route for user
        return Optimizer.query.filter(
                Optimizer.user_id== self.id).first()

## this creates our assessment table (database)
## need to create add'l columns for the database (Google Picture, Zillow Info, etc)
class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  ## assessment id
    raw_address = db.Column(db.String(80))
    agent_est = db.Column(db.String(15))
    applicant_est = db.Column(db.String(15))
    lat = db.Column(db.String(25))
    lng = db.Column(db.String(25))
    street_number = db.Column(db.String(10))
    street_name = db.Column(db.String(60))
    city_name = db.Column(db.String(60))
    state_abr = db.Column(db.String(5))
    postal_code = db.Column(db.String(12))
    formatted_address = db.Column(db.String(120))
    google_place_id = db.Column(db.String(40))
    street_pic = db.Column(db.String(100))
    zillow_estimate = db.Column(db.Integer)
    zillow_baths = db.Column(db.String(3))
    zillow_bedrooms = db.Column(db.String(3))
    damage = db.Column(db.String(60))  ## contents of assessment
    other_damage = db.Column(db.String(60))
    exterior = db.Column(db.String(60))
    interior = db.Column(db.String(60))
    other_exterior = db.Column(db.String(60))
    other_interior = db.Column(db.String(60))
    disaster_type = db.Column(db.String(60))
    disaster_name = db.Column(db.String(60))
    comments = db.Column(db.String(300))

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) ## creates time of assessment, utcnow creates uniform timestamps
    ## this is the relational link to the 'user' table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):  ## this method tells python how to print objects of this class
        return (f'<Assessment {self.address}>')

@login.user_loader  ## decorator used to register flask_login
def load_user(id):
    return User.query.get(int(id)) ## id is passed as a string, so we turn to int for db processing


''' The below code has not been utilized fully.  This can be used to loop in the route_optimizer 'SIVIRO' '''

class Optimizer(db.Model):  ## creates database table for our Optimizer
    id = db.Column(db.Integer, primary_key=True)  ## optimized route id
    map_pic = db.Column(db.String(100)) ## to store path for map_pic

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    ## this is the relational link to the 'user' table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):  ## this method tells python how to print objects of this class in html
        return (f'<Optimizer {self.optimizer}>')
