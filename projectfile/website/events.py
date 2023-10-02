from flask import Blueprint, flash, render_template, request, url_for, redirect, current_app
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User, Event, GameSystem, EventImage, Comment
from flask_login import login_user, login_required,logout_user, current_user
from . import db
from .forms import EventCreationForm, CommentForm
from datetime import datetime
from werkzeug.utils import secure_filename
import os


bp = Blueprint('events', __name__)

@bp.route('/event/<id>', methods=['GET', 'POST'])
def showevent(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    comments = Comment.query.filter_by(event_id=id).all()
    comment_form = CommentForm()
    if (comment_form.validate_on_submit()==True):
        user_id = current_user.id
        event_id = id
        message = comment_form.message.data
        
        new_comment = Comment(user_id=user_id,event_id=event_id,message=message)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('events.showevent', id=id))

    return render_template('events/show.html', event=event, form=comment_form)


@bp.route('/event/creation', methods=['GET', 'POST'])
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
            db_upload_path = 'uploads/' + secure_filename(filename)
            image.save(upload_path)
            event_image = EventImage(event_id=new_event.id,filepath=db_upload_path)
            db.session.add(event_image)
        
    create_event_form = EventCreationForm()
    game_system_choices = [game_system_list.name for game_system_list in GameSystem.query.all()]
    create_event_form.game_system.choices = game_system_choices
    if (create_event_form.validate_on_submit()==True):
            title = create_event_form.title.data
            description = create_event_form.description.data
            owner_id = current_user.id
            game_system_name = create_event_form.game_system.data
            game_system_id = GameSystem.query.filter_by(name=game_system_name).first().id
            cost = create_event_form.cost.data
            location = create_event_form.location.data
            date = create_event_form.date.data
            time = create_event_form.time.data
            total_tickets = create_event_form.total_tickets.data
            print(game_system_id)
            event = db.session.scalar(db.select(Event).where(Event.title==title and User.id == owner_id))
            if event:
                flash("You've already made an event with this title, please try another")
                
                return redirect(url_for('events.event_creation'))
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
        return render_template('events/creation.html', form=create_event_form, heading='event_creation')