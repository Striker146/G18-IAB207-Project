from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, TelField, SelectField, DecimalField, DateField, TimeField, MultipleFileField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from datetime import datetime



#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone_number = TelField("Phone Number")
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")
    
class EventCreationForm(FlaskForm):
    title=StringField("Title", validators=[InputRequired()])
    description=TextAreaField("Description", validators=[InputRequired()])
    game_system = SelectField("Game System",choices=["Dnd 5e", "DnD 4e"])
    cost = DecimalField("Cost", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired()])
    date  = DateField('Date')
    time = TimeField('Time')
    images =MultipleFileField("Images",validators=[InputRequired()])
    total_tickets = IntegerField("Total Tickets", validators=[InputRequired()])
    submit = SubmitField("Create Event")
    
    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
            
class CommentForm(FlaskForm):
    message = TextAreaField("Comment", validators=[InputRequired()])
    submit = SubmitField("Create Comment")
    
    