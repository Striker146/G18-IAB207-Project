from flask import Blueprint, flash, render_template, request, url_for, redirect, current_app
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User, Event, GameSystem, EventImage
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user, current_user
from . import db
from .forms import EventCreationForm
from datetime import datetime
from werkzeug.utils import secure_filename
import os


#create a blueprint
bp = Blueprint('auth', __name__)

# this is a hint for a login function
@bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
    
     print('In Login View function')
     login_form = LoginForm()
     error=None
     if(login_form.validate_on_submit()==True):
         user_name = login_form.user_name.data
         password = login_form.password.data
         user = User.query.filter_by(username=user_name).first()
         print(user)
         if user is None:
             error='Incorrect credentials supplied'
         elif not check_password_hash(user.password_hash, password): # takes the hash and password
             error='Incorrect credentials supplied'
         if error is None:
             login_user(user)
             print("User logged in")
             nextp = request.args.get('next') #this gives the url from where the login page was accessed
             print(nextp)
             print("nextp")
             if nextp is None or not nextp.startswith('/'):
                 return redirect(url_for('main.index'))
             return redirect(nextp)
         else:
             flash(error)
     return render_template('login.html', form=login_form, heading='Login')
 
 
 
@bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form is fine, HTTP request is POST
    if (register.validate_on_submit()==True):
            #get username, password and email from the form
            uname = register.user_name.data
            pwd = register.password.data
            email = register.email_id.data
            #check if a user exists
            user = db.session.scalar(db.select(User).where(User.username==uname))
            if user:#this returns true when user is not None
                flash('Username already exists, please try another')
                return redirect(url_for('auth.register'))
            # don't store the password in plaintext!
            pwd_hash = generate_password_hash(pwd)
            #create a new User model object
            new_user = User(username=uname, password_hash=pwd_hash, email=email)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('register.html', form=register, heading='Register')
    
@bp.route('/event_creation', methods=['GET', 'POST'])
@login_required
def event_creation():
    def save_event_images(images :list, event_title):
        BASE_PATH = os.path.dirname(__file__)
        if images.count == 0:
            return
        for image in images:
            print(image)
            filename = image.filename
            upload_path = os.path.join(BASE_PATH, 'static\\uploads', secure_filename(filename))
            db_upload_path = '\\static\\uploads\\' + secure_filename(filename)
            image.save(upload_path)
            event_image = EventImage(event_id=new_event.id,image=db_upload_path)
            db.session.add(event_image)
        
    create_event_form = EventCreationForm()
    game_system_choices = [game_system_list.game_system for game_system_list in GameSystem.query.all()]
    create_event_form.game_system.choices = game_system_choices
    if (create_event_form.validate_on_submit()==True):
            title = create_event_form.title.data
            description = create_event_form.description.data
            owner_id = current_user.id
            game_system = create_event_form.game_system.data
            game_system_id = GameSystem.query.filter_by(game_system=game_system).first().id
            cost = create_event_form.cost.data
            location = create_event_form.location.data
            date = create_event_form.date.data
            time = create_event_form.time.data
            total_tickets = create_event_form.total_tickets.data
            print(game_system_id)
            event = db.session.scalar(db.select(Event).where(Event.title==title and User.id == owner_id))
            if event:
                flash("You've already made an event with this title, please try another")
                
                return redirect(url_for('auth.event_creation'))
            new_event = Event(status_id=1, owner_id=owner_id, game_system_id=game_system_id, 
                              title=title, description=description, cost=cost, location=location, 
                              time=time, date=date,total_tickets=total_tickets, remaining_tickets=total_tickets )
            db.session.add(new_event)
            db.session.flush()
            save_event_images(create_event_form.images.data, title)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('event_creation.html', form=create_event_form, heading='event_creation')