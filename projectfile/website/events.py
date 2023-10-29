from flask import Blueprint, flash, render_template, request, url_for, redirect, current_app
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User, Event, GameSystem, EventImage, Comment, AgeGroup, CampaignFocus, PlayerSkillLevel, EventStatus, EventTag, Booking
from flask_login import login_user, login_required,logout_user, current_user
from . import db
from .forms import EventCreationForm, CommentForm, BookingForm, SearchForm
from datetime import datetime
from werkzeug.utils import secure_filename
import os


bp = Blueprint('events', __name__)

@bp.route('/event/<id>', methods=['GET', 'POST'])
def showevent(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    comment_form = CommentForm()
    booking_form = BookingForm()
    if request.method == 'POST':
        if (comment_form.validate_on_submit()==True):
            user_id = current_user.id
            event_id = id
            message = comment_form.message.data
            created_at = datetime.now()
            print("Check Check!")
            new_comment = Comment(user_id=user_id,event_id=event_id,message=message, created_at=created_at)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('events.showevent', id=id))
        
        if (booking_form.validate_on_submit()==True):
            user_id = current_user.id
            event_id = id
            unique_identifier = Booking.generate_uid()
            tickets = booking_form.amount.data
            purchase_date =  datetime.now()
            new_booking = Booking(user_id = user_id, event_id = event_id, unique_identifier = unique_identifier,
                            tickets = tickets, purchase_date = purchase_date)
            
            db.session.add(new_booking)
            db.session.flush()
            event.update_purchased_tickets()
            db.session.commit()
            return redirect(url_for('events.showevent', id=id))
            flash("Tickets Purchased Sucessfully")
            
        

    return render_template('events/show.html', event=event, comment_form=comment_form, booking_form=booking_form)


@bp.route('/event/creation', methods=['GET', 'POST'])
@login_required
def creation():
    def save_event_images(images :list, event_title):
        BASE_PATH = os.path.dirname(__file__)
        if images.count == 0:
            return
        for image in images:
            print(image)
            filename = image.filename
            upload_path = os.path.join(BASE_PATH, 'static//uploads', secure_filename(filename))
            db_upload_path = 'uploads/' + secure_filename(filename)
            image.save(upload_path)
            event_image = EventImage(event_id=new_event.id,filepath=db_upload_path)
            db.session.add(event_image)
    
    def get_choices(create_event_form):
        game_system_list = GameSystem.query.all()
        result = [(game_system.id, game_system.name) for game_system in game_system_list]
        create_event_form.game_system.choices = result
        
        age_group_list = AgeGroup.query.all()
        result = [(age_group.id, age_group.name) for age_group in age_group_list]
        create_event_form.age_group.choices = result
        
        campaign_focus_list = CampaignFocus.query.all()
        result = [(cf.id, cf.name) for cf in campaign_focus_list]
        create_event_form.campaign_focus.choices = result
        
        player_skill_level_list = PlayerSkillLevel.query.all()
        result = [(psl.id, psl.name) for psl in player_skill_level_list]
        print(result)
        create_event_form.player_lower_skill_level.choices = result
        create_event_form.player_higher_skill_level.choices = result
        
        
        create_event_form.game_system.default = 1
        create_event_form.age_group.default = 1
        create_event_form.campaign_focus.default = 1
        
        create_event_form.player_higher_skill_level.default = 3
        create_event_form.player_lower_skill_level.default = 1
        
    create_event_form = EventCreationForm()
    game_system_choices = [game_system_list.name for game_system_list in GameSystem.query.all()]
    create_event_form.game_system.choices = game_system_choices
    get_choices(create_event_form)
    if (create_event_form.validate_on_submit()==True):
            title = create_event_form.title.data
            description = create_event_form.description.data
            owner_id = current_user.id
            game_system_id = create_event_form.game_system.data[0]
            age_group_id = create_event_form.age_group.data[0]
            campaign_focus_id = create_event_form.campaign_focus.data[0]
            lower_player_skill_level_id = create_event_form.player_lower_skill_level.data[0]
            higher_player_skill_level_id = create_event_form.player_higher_skill_level.data[0]
            cost = create_event_form.cost.data
            location = create_event_form.location.data
            date = create_event_form.date.data
            start_time = create_event_form.start_time.data
            end_time = create_event_form.end_time.data
            total_tickets = create_event_form.total_tickets.data
            one_shot = create_event_form.one_shot.data
            session_zero = create_event_form.session_zero.data
            homebrew = create_event_form.homebrew.data
            open_world = create_event_form.open_world.data
            
            event = db.session.scalar(db.select(Event).where(Event.title==title and User.id == owner_id))
            #if event:
            #    flash("You've already made an event with this title, please try another")
            #    
            #    return redirect(url_for('events.event_creation'))
            new_event = Event(status_id=1, owner_id=owner_id, game_system_id=game_system_id, 
                              title=title, description=description, cost=cost, location=location, 
                              start_time=start_time, end_time=end_time, date=date,total_tickets=total_tickets, remaining_tickets=total_tickets )
            
            
            db.session.add(new_event)
            db.session.flush()
            new_event_tag = EventTag(event_id = new_event.id, age_group_id = age_group_id, campaign_focus_id = campaign_focus_id,
                                     lower_player_skill_level_id = lower_player_skill_level_id,
                                     higher_player_skill_level_id = higher_player_skill_level_id,
                                     one_shot = one_shot, session_zero = session_zero,
                                     homebrew= homebrew, open_world = open_world)
            db.session.add(new_event_tag)
            
            save_event_images(create_event_form.images.data, title)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('events/creation.html', form=create_event_form, heading='event_creation')


@bp.route('/event/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():
        comment = Comment(text= form.text.data, event=event, user=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added', 'success')    
    
    return redirect(url_for('event.show', id=id))



@bp.route('/my_events')
@login_required
def my_events():
    user_events = get_events_by_username(current_user.username)

    return render_template('events/my_events.html', events=user_events)

def get_events_by_username(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return []
    
    events_by_user = Event.query.filter_by(owner_id=user.id).all()
    return events_by_user

@bp.route('/events/list')
def list():
    search_form = SearchForm()
    search_form.set_select_fields()
    events = db.session.scalars(db.select(Event)).all()
    print(len(events))
    return render_template('events/list.html', events=events,search_form=search_form)


    