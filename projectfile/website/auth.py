from flask import Blueprint, flash, render_template, request, url_for, redirect, current_app
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User, Event, GameSystem, EventImage
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user, current_user
from . import db
from werkzeug.utils import secure_filename


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
    
