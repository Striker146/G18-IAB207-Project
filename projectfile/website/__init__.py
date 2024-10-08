#from package import Class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import datetime

db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    app.secret_key='somesecretgoeshere'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydbname.sqlite'
    UPLOAD_FOLDER = '\\static\\uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #initialise db with flask app
    db.init_app(app)

    bootstrap = Bootstrap5(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    


    #importing views module here to avoid circular references
    # a common practice.
    from . import views
    app.register_blueprint(views.bp)


    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import events
    app.register_blueprint(events.bp)
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", error=e)
    
    @app.context_processor
    def get_context():
      year = datetime.datetime.today().year
      return dict(year=year)
  
    return app

def create_data_table(table : db.Model,data : list):
    if len(table.query.all()) == 0:
        for element in data:
            row = table(name = element)
            db.session.add(row)
            
            

def create_data():
    from .models import AgeGroup, CampaignFocus, PlayerSkillLevel, EventStatus, GameSystem
    age_group_strs = ["Everybody", "18+", "Under 18"]
    game_systems_str = ['Cybergeneration','Cyberpunk 2013', 'Cyberpunk 2020','Cyberpunk RED', 'Cyberspace', 'ADnD', 'DnD 4e', 'DnD 5e','Star Wars Roleplaying Game', 'Stormbringer', 'Supervillains', "Thieves' Guild", 'Trinity', 'Vampire: The Masquerade']
    event_status_strs = ["Open","Inactive","Sold out", "Cancelled"]
    player_skill_strs = ["Amateur","Intermediate","Veteran"]
    campaign_focus_strs = ["Balanced", "Combat Focused", "Roleplay Focused"]
    
    create_data_table(AgeGroup, age_group_strs)
    create_data_table(GameSystem, game_systems_str) 
    create_data_table(EventStatus, event_status_strs)
    create_data_table(PlayerSkillLevel, player_skill_strs) 
    create_data_table(CampaignFocus, campaign_focus_strs) 
    
    db.session.commit()