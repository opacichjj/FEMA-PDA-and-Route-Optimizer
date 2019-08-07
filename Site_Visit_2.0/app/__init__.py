from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy  ## importing our database extension
from flask_migrate import Migrate  ##importing our database migration engine
from flask_login import LoginManager  ## importing extension to manage user logged in state
from flask_bootstrap import Bootstrap

'''  This code will import the ability to log errors
import logging
from logging.handler import SMTPHandler'''

## instantiating Flask class as app
app = Flask(__name__, static_url_path='', static_folder='images')

bootstrap = Bootstrap(app)

login = LoginManager(app) ## initializing our login manager
login.login_view = 'login' ## establishing the URL call for login

## using app.config.from_object() method to read and apply Config class
app.config.from_object(Config)
##
db = SQLAlchemy(app) ## instantiating our database
migrate = Migrate(app, db) ## instantiating our migrating engine

## importing routes from the 'app' folder and models which will define the structure of the database and how to route information and errors to redirect error pages
from app import routes, models, errors


'''
The below code is used to email error logs

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
'''
