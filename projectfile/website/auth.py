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
         user = db.session.scalar(db.select(User).where(User.username== user_name))
         print(user)
         if user is None:
            error = 'Incorrect username'#could be a security risk to give this much info away
        #check the password - notice password hash function
         elif not check_password_hash(user.password_hash, password): # takes the hash and password
            error = 'Incorrect password'
         if error is None:
            #all good, set the login_user of flask_login to manage the user
            login_user(user)
            return redirect(url_for('main.index'))
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
    
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))