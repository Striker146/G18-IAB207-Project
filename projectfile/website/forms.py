from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, TelField, SelectField, DecimalField, DateField, TimeField, MultipleFileField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp, NoneOf, NumberRange, NumberRange 
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
    phone_number = TelField("Phone Number" ,validators=[Regexp('[0-9]', message='Please enter a legitimate phone number with exactly 10 digits.')])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match"),
                  Length(min=8, max=20, message='Password must be between 8 and 20 characters'),
                  Regexp('^(?=.*[0-9])(?=.*[a-zA-Z])', message='Password must contain letters and numbers only'),
                  NoneOf(" ", message='Password must not contain spaces')])

    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")
    
class EventCreationForm(FlaskForm):
    title=StringField("Title", validators=[InputRequired()])
    description=TextAreaField("Description", validators=[InputRequired()])
    game_system = SelectField("Game System")
    cost = DecimalField("Cost", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired()])
    date  = DateField('Date')
    start_time = TimeField('End Time')
    end_time = TimeField("Start Time")
    images =MultipleFileField("Images",validators=[InputRequired()])
    total_tickets = IntegerField("Total Tickets", validators=[InputRequired()])
    age_group = SelectField("Age Group")
    campaign_focus = SelectField("Campaign Focus")
    player_lower_skill_level = SelectField("Lower Player Skill Level")
    player_higher_skill_level = SelectField("Higher Player Skill Level")
    one_shot = BooleanField("Is oneshot")
    session_zero = BooleanField("Starting from Session Zero")
    homebrew = BooleanField("Homebrew Rules")
    open_world = BooleanField("Open World")
    
    bool_tags = [one_shot, session_zero, homebrew, open_world]
    
    submit = SubmitField("Create Event")
    
    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
    
    def get_choices(self):
        from .models import GameSystem, AgeGroup, CampaignFocus, PlayerSkillLevel
        game_system_list = GameSystem.query.all()
        result = [(game_system.id, game_system.name) for game_system in game_system_list]
        self.game_system.choices = result
        
        age_group_list = AgeGroup.query.all()
        result = [(age_group.id, age_group.name) for age_group in age_group_list]
        self.age_group.choices = result
        
        campaign_focus_list = CampaignFocus.query.all()
        result = [(cf.id, cf.name) for cf in campaign_focus_list]
        self.campaign_focus.choices = result
        
        player_skill_level_list = PlayerSkillLevel.query.all()
        result = [(psl.id, psl.name) for psl in player_skill_level_list]
        print(result)
        self.player_lower_skill_level.choices = result
        self.player_higher_skill_level.choices = result
        
        
        self.game_system.default = 1
        self.age_group.default = 1
        self.campaign_focus.default = 1
        
        self.player_higher_skill_level.default = 3
        self.player_lower_skill_level.default = 1

class CommentForm(FlaskForm):
    message = TextAreaField("Comment", validators=[InputRequired()])
    submit = SubmitField("Create Comment")
    
class BookingForm(FlaskForm):
    amount = IntegerField("Amount of Tickets", validators=[InputRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField("Confirm Purchase")
    
    