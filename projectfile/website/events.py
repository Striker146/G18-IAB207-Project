from flask import Blueprint, flash, render_template, request, url_for, redirect, current_app
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User, Event, GameSystem, EventImage, Comment, AgeGroup, CampaignFocus, PlayerSkillLevel, EventStatus, EventTag, Booking, EventImage, generate_comments
from flask_login import login_user, login_required,logout_user, current_user
from . import db
from .forms import EventCreationForm, CommentForm, BookingForm, EventEditForm, SearchForm
from datetime import datetime
from werkzeug.utils import secure_filename
import os


bp = Blueprint('events', __name__)

@bp.route('/event/<id>', methods=['GET', 'POST'])
def showevent(id):
    Event.compare_dates()
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
            total_cost = event.cost * tickets
            purchase_date =  datetime.now()
            booking_valid = Booking.is_valid_booking(event,tickets)
            if booking_valid[0]:
                new_booking = Booking(user_id = user_id, event_id = event_id, unique_identifier = unique_identifier,
                                tickets = tickets, purchase_date = purchase_date, total_cost = total_cost)
                db.session.add(new_booking)
                db.session.flush()
                event.update_purchased_tickets()
                db.session.commit()
                flash("Tickets Purchased Sucessfully")
                return redirect(url_for('events.showevent', id=id))
               
            else:
                flash(booking_valid[1])
                return redirect(url_for('events.showevent', id=id))
            
        

    return render_template('events/show.html', event=event, comment_form=comment_form, booking_form=booking_form)


@bp.route('/event/creation', methods=['GET', 'POST'])
@login_required
def creation():
    Event.compare_dates()
    create_event_form = EventCreationForm()
    create_event_form.get_choices()

    
    if (create_event_form.validate_on_submit()==True):
            title = create_event_form.title.data
            description = create_event_form.description.data
            owner_id = current_user.id
            game_system_id = create_event_form.game_system.data
            age_group_id = create_event_form.age_group.data
            campaign_focus_id = create_event_form.campaign_focus.data
            lower_player_skill_level_id = create_event_form.player_lower_skill_level.data
            higher_player_skill_level_id = create_event_form.player_higher_skill_level.data
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
            if lower_player_skill_level_id > higher_player_skill_level_id:
                carry = higher_player_skill_level_id
                higher_player_skill_level_id = lower_player_skill_level_id
                lower_player_skill_level_id = carry
                
            #if event:
            #    flash("You've already made an event with this title, please try another")
            #    
            #    return redirect(url_for('events.event_creation'))
            new_event = Event(status_id=1, owner_id=owner_id, game_system_id=game_system_id, 
                              title=title, description=description, cost=cost, location=location, 
                              start_time=start_time, end_time=end_time, date=date,total_tickets=total_tickets, remaining_tickets=total_tickets )
            
            db.session.add(new_event)
            db.session.flush()
            print(f"New Game System is: {new_event.game_system.name}")
            new_event_tag = EventTag(event_id = new_event.id, age_group_id = age_group_id, campaign_focus_id = campaign_focus_id,
                                     lower_player_skill_level_id = lower_player_skill_level_id,
                                     higher_player_skill_level_id = higher_player_skill_level_id,
                                     one_shot = one_shot, session_zero = session_zero,
                                     homebrew= homebrew, open_world = open_world)
            
            db.session.add(new_event_tag)
            
            EventImage.save_event_images(create_event_form.images.data,event=new_event)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('events.my_events'))
        
    #the else is called when the HTTP request calling this page is a GET
    else:
        print(create_event_form.errors)
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
    Event.compare_dates()
    user_events = current_user.events
    return render_template('events/my_events.html', events=user_events, heading="my_events")


@bp.route('/events/list', methods=['GET', 'POST'])
def list():
    search_term = ''
    try:
        search_term = request.args.getlist('search')[0]
    except IndexError:
        pass
    game_system_id = request.args.get('game_system')
    status_id = request.args.get('status')
    if game_system_id == None:
        redirect_flag = True
        game_system_id = "0"
    if status_id == None:
        redirect_flag = True
        status_id = "0"
    Event.compare_dates()
    print(search_term)
    print(game_system_id)
    print(status_id)
    search_form = SearchForm()
    search_form.set_select_fields()
    search_form.game_system.data = game_system_id
    search_form.status.data = status_id
    search_form.game_system.default = game_system_id
    search_form.status.default = status_id
    search_form.process()
    search_form.search.data = search_term

    
    events_query = db.session.query(Event)
    events = events_query.all()
    
    # If the form is submitted
    if request.method == 'GET':
        if search_term:
            search = f"%{search_term}%"
            events_query = events_query.filter(Event.title.like(search))
            events = events_query.all()


        if not game_system_id == "0":
            print("Searching Game System")
            print(game_system_id) 
            events_query = events_query.filter_by(game_system_id=game_system_id)
            events = events_query.all()

        if not status_id == "0":
            print("Searching status")
            print(status_id)
            events_query = events_query.filter_by(status_id=search_form.status.data)
            events = events_query.all()
        # Add more filters as needed...

    events = events_query.all()
    return render_template('events/list.html', events=events,search_form=search_form)



@bp.route('/event/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if event == None:
        return render_template('404.html', error="No Event found")
    edit_event_form = EventEditForm()
    edit_event_form.get_choices()
    if event.owner_id == current_user.id:
        if (edit_event_form.validate_on_submit()==True):
            event_tags = event.tags[0]
            event.title = edit_event_form.title.data
            event.description = edit_event_form.description.data
            event.game_system_id = edit_event_form.game_system.data
            event_tags.age_group_id = edit_event_form.age_group.data
            event_tags.campaign_focus_id = edit_event_form.campaign_focus.data
            event_tags.lower_player_skill_level_id = edit_event_form.player_lower_skill_level.data
            event_tags.higher_player_skill_level_id = edit_event_form.player_higher_skill_level.data
            event.cost = edit_event_form.cost.data
            event.location = edit_event_form.location.data
            event.date = edit_event_form.date.data
            event.start_time = edit_event_form.start_time.data
            event.end_time = edit_event_form.end_time.data
            event.total_tickets = edit_event_form.total_tickets.data
            event_tags.one_shot = edit_event_form.one_shot.data
            event_tags.session_zero = edit_event_form.session_zero.data
            event_tags.homebrew = edit_event_form.homebrew.data
            event_tags.open_world = edit_event_form.open_world.data
            print(edit_event_form.images.data[0].filename)
            if edit_event_form.images.data[0].filename == "":
                print("No new Images")
            else:
                EventImage.delete_event_images(event=event)
                EventImage.save_event_images(images=edit_event_form.images.data, event=event)
            db.session.commit()
            flash('Event updated successfully', 'success')
            return redirect(url_for('events.my_events'))
        else:

            
            event_tags = event.tags[0]
            edit_event_form.game_system.data = event.game_system_id
            edit_event_form.age_group.data = event_tags.age_group_id
            edit_event_form.campaign_focus.data = event_tags.campaign_focus_id
            edit_event_form.player_lower_skill_level.data = event_tags.lower_player_skill_level_id
            edit_event_form.player_higher_skill_level.data = event_tags.higher_player_skill_level_id
            
            edit_event_form.game_system.default = event.game_system_id
            edit_event_form.age_group.default = event_tags.age_group_id
            edit_event_form.campaign_focus.default = event_tags.campaign_focus_id
            edit_event_form.player_lower_skill_level.default = event_tags.lower_player_skill_level_id
            edit_event_form.player_higher_skill_level.default = event_tags.higher_player_skill_level_id
            edit_event_form.process()
            edit_event_form.title.data = event.title
            edit_event_form.description.data = event.description
            

            
            edit_event_form.cost.data = event.cost
            edit_event_form.images.data = event.images
            edit_event_form.location.data = event.location
            edit_event_form.date.data = event.date
            edit_event_form.start_time.data = event.start_time
            edit_event_form.end_time.data = event.end_time
            edit_event_form.total_tickets.data = event.total_tickets
            edit_event_form.one_shot.data = event_tags.one_shot
            edit_event_form.session_zero.data = event_tags.session_zero
            edit_event_form.homebrew.data = event_tags.homebrew
            edit_event_form.open_world.data = event_tags.open_world
            return render_template('events/creation.html', form=edit_event_form, event=event, heading='edit_event')
    else:
        return render_template('404.html', error="No Event found")

    

@bp.route('/events/cancel/<id>', methods=['GET', 'POST'])
def cancel_event(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if event.status.id == 2:
        flash("You can't cancel an event in the past")
    elif event.status.id == 4:
        flash("The event is already cancelled")
    else:
        event.status_id = 4
        db.session.commit()
        flash("Event Cancelled Successfully")
    return redirect(url_for('events.my_events', id=id))


@bp.route('/events/my_bookings', methods=['GET', 'POST'])


@bp.route('/my_bookings')
@login_required
def my_bookings():  
    Event.compare_dates()
    return render_template('events/my_bookings.html', bookings=current_user.bookings, heading="my_bookings")
