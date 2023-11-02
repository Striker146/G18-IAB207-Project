from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, TelField, SelectField, DecimalField, DateField, TimeField, MultipleFileField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp, NoneOf, NumberRange, NumberRange, StopValidation
from werkzeug.datastructures import FileStorage
from datetime import datetime
from collections.abc import Iterable

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

    
class MultiFileAllowed(object):

    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):

        # FileAllowed only expects a single instance of FileStorage
        # if not (isinstance(field.data, FileStorage) and field.data):
        #     return

        # Check that all the items in field.data are FileStorage items
        if not (all(isinstance(item, FileStorage) for item in field.data) and field.data):
            return

        for data in field.data:
            filename = data.filename.lower()

            if isinstance(self.upload_set, Iterable):
                if any(filename.endswith('.' + x) for x in self.upload_set):
                    return
                raise StopValidation(self.message or field.gettext(
                    'File does not have an approved extension: {extensions}'
                ).format(extensions=', '.join(self.upload_set)))

            if not self.upload_set.file_allowed(field.data, filename):
                raise StopValidation(self.message or field.gettext(
                    'File does not have an approved extension.'
                ))
    

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    address  = StringField("Address", validators=[InputRequired()])
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
    cost = DecimalField("Cost", validators=[InputRequired(), NumberRange(min=0)])
    location = StringField("Location", validators=[InputRequired()])
    date  = DateField('Date',validators=[InputRequired()])
    start_time = TimeField('End Time', validators=[InputRequired()])
    end_time = TimeField("Start Time", validators=[InputRequired()])
    images =MultipleFileField("Images", validators=[InputRequired(), MultiFileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    total_tickets = IntegerField("Total Tickets", validators=[InputRequired(), NumberRange(min=1)])
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
            
class EventEditForm(EventCreationForm):
    images =MultipleFileField("Images")
    submit = SubmitField("Confirm Edit to Event")
    
    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
    
    
    

class CommentForm(FlaskForm):
    message = TextAreaField("Comment", validators=[InputRequired()])
    submit = SubmitField("Create Comment")
    
class BookingForm(FlaskForm):
    amount = IntegerField("Amount of Tickets", validators=[InputRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField("Confirm Purchase")

class SearchForm(FlaskForm):
    search = StringField("Search")
    status = SelectField("Event Status")
    game_system = SelectField("GameSystem")
    age_group = SelectField("Age Group")
    campaign_focus = SelectField("Campaign Focus")
    player_skill_level = SelectField("Lower Player Skill Level")
    one_shot = BooleanField("Is oneshot")
    session_zero = BooleanField("Starting from Session Zero")
    homebrew = BooleanField("Homebrew Rules")
    open_world = BooleanField("Open World")
    submit = SubmitField("Search")
    
    def set_select_fields(self):
        from .models import EventStatus, GameSystem, AgeGroup, CampaignFocus, PlayerSkillLevel
        system_lists = [[self.status, EventStatus], [self.game_system,GameSystem], [self.age_group,AgeGroup], [self.player_skill_level,PlayerSkillLevel]]
        for system_set in system_lists:
            type_list = system_set[1].query.all()
            result = [(element_type.id, element_type.name) for element_type in type_list]
            all_select = [0,"All"]
            result.reverse()
            result.append(all_select)
            result.reverse()

            system_set[0].choices = result
            
