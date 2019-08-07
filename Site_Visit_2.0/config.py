## this is the secret key configuration for web forms to protect against CSRF

import os

##
basedir = os.path.abspath(os.path.dirname(__file__))
#key for login and contract form
class Config(object):

    ## since our security is low (right now) we will allow the hardcode string to work for the SECRET_KEY
    ## we would change this when deployed on a production server
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    ## configuring a variable that will take the environment variable 'DATABASE_URL' or app.db (if the env var is undefined)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    ## this is to disable the signal done everytime a change made to the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    '''
    The below code, if used, will email error logs:

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    To setup these variables, use export [variable]=[value] 
    '''
