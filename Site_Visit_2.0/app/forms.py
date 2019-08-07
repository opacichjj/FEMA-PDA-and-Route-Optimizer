from flask_wtf import FlaskForm, Form  ## used to create the Forms
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, SelectMultipleField, FormField, FieldList, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Required
from app.models import User ## calling our User class
from flask_wtf.file import FileField, FileRequired
from app.state_info import StateInfo


## creating a class to accept our wtforms classes
class LoginForm(FlaskForm): ## takes the import FlaskForm

    ## The 4 wtform classes, validators can be changed to accept other values 'DataRequired' only validates cells aren't empty
    ## these get sent to forms.py and render themselves as html
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


## creating an object for registration form that takes the same wtforms
class RegistrationForm(FlaskForm):
    ## creating the input forms and accepting the following inputs
    username = StringField('Username', validators=[DataRequired()])
    ## the 2nd validator here 'Email' verifies email format
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    ## validating the correct password by the user
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    ## custom validator for wtforms to verify username is not in database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:  ## if user has a value, raise the error
            raise ValidationError('Please use a different username.')

    ## custom validator for wtforms to verify email is not in database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None: ## if email has a value, raise the error
            raise ValidationError('Please use a different email address.')


## Edit profie object that accepts values for new_username and title
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    title = TextAreaField('Title', validators=[Length(min=0, max=80)])
    submit = SubmitField('Submit')

    ## this method will virtually do nothing, if the username remains the same
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs) ## super calls the class constructor from the 'parent class' FlaskForm
        self.original_username = original_username

    ## this method will run a query to check if the username is available
    def validate_username(self, username):
        if username.data != self.original_username:
            ## query to check originality of name
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:  ## error given if name not unique
                raise ValidationError('Please use a different username.')


class SurveyForm(FlaskForm):  ## creating our SurveyForm to collect assessments
    # state_list = StateInfo.state_list()  ## this is not used, calls a master list of states that can be place in a dropdown list

    ## photo = FileField(validators=[FileRequired()])
    raw_address = StringField('Address', validators = [DataRequired()])
    applicant_est = StringField('Applicant Estimate', validators = [DataRequired()])
    damage = SelectField(u'Main Building', choices = [('Affected/Not Accessible', 'Affected/Not Accessible'), ('Major', 'Major'), ('Minor', 'Minor'), ('Destroyed', 'Destroyed'), ('None', 'None')], validators = [DataRequired()])  ## the damage drop down box
    exterior = StringField('Main Exterior Damage')
    interior = StringField('Main Interior Damage')
    other_damage = SelectField(u'Other Buildings', choices = [('N/A', 'N/A'), ('Affected', 'Affected'), ('Major', 'Major'), ('Minor', 'Minor'), ('Destroyed', 'Destroyed'), ('None', 'None')], validators = [DataRequired()])
    other_exterior = StringField('Other Exterior Damage')
    other_interior = StringField('Other Interior Damage')
    agent_est = StringField('Agent Assessment Estimate', validators = [DataRequired()])
    disaster_type = SelectField(u'Type of Disaster', choices = [('Fire', 'Fire'), ('Flood', 'Flood'), ('Hurricane','Hurricane'), ('Earthquake','Earthquake'), ('Tornado','Tornado'), ('Other', 'Other')], validators = [DataRequired()])
    disaster_name = StringField('Name of Disaster')
    comments = StringField('Other Notes')

    submit = SubmitField('Submit Damage Assessment')



''' The below code has not been utilized fully.  This can be used to loop in the route_optimizer 'SIVIRO' '''

## Subclass for RouteForm, see below.  This allows us to take in multiple entries
class AddressEntryForm(Form):
    place = StringField('Address')

## Parent class for AddressEntryForm to take in all necessary address entries for Site Visit Route Optimization
class RouteForm(FlaskForm):
    """A form for one or more addresses"""
    num_sites = IntegerField('Number of Sites to Visit', validators = [DataRequired()], default = 5)
    origin = StringField('Starting Address', validators = [DataRequired()])
    addresses = FieldList(FormField(AddressEntryForm), min_entries=1, max_entries=20, validators = [DataRequired()])
    #origin_return = 'SelectField or Check Box'
    return_location =  StringField('Return Location', validators = [DataRequired()])
    submit = SubmitField('Find Optimal Route')

    def __init__(self, *args, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        default_amount = self.num_sites.data
        self.addresses.choices = [('address{}'.format(i), i) for i in range(default_amount)]



''' This can be used to accept a photo submission.  This should be used to add the damaged photo for the assessment file.  It can be added to DSI-6s code to use exif data to read in coordinates

    class PhotoForm(FlaskForm):
        photo = FileField(validators=[FileRequired()])  ## FileField takes in a file
        submit = SubmitField('Submit Photo')'''
