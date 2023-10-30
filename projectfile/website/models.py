from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import desc
from . import db
from uuid import uuid4
import os
from werkzeug.utils import secure_filename
from sqlalchemy import delete

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(100), index=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    events = db.relationship('Event', backref='owner')
    comments = db.relationship('Comment', backref='user')
    bookings = db.relationship('Booking', backref='user', order_by='Booking.id.desc()')




class EventStatus(db.Model):
    __tablename__ = 'event_statuses'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True)
    events = db.relationship("Event",backref='status')
    

class GameSystem(db.Model):
    __tablename__ = 'game_systems'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True)
    events = db.relationship("Event",backref='game_system')
    
    

    
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('event_statuses.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_system_id = db.Column(db.Integer, db.ForeignKey('game_systems.id'))
    title = db.Column(db.String(100), index=True, nullable=False)
    description = db.Column(db.String(100), index=True, nullable=False)
    cost = db.Column(db.Float(100), index=True, nullable=False)
    location = db.Column(db.String(100), index=True, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    purchased_tickets = db.Column(db.Integer, default=0, nullable=False)
    remaining_tickets = db.Column(db.Integer, default=0, nullable=False)

    comments = db.relationship('Comment', backref='event', order_by='Comment.id.desc()')
    images = db.relationship('EventImage',backref="event")
    bookings = db.relationship("Booking",backref="event")
    
    
    def __repr__(self):
        str = f"id {self.id}, title:{self.title}"
        return str
    
    def update_status(self):
        if self.remaining_tickets <=0:
            self.remaining_tickets = 0
            self.status_id = 3
    @staticmethod  
    def compare_dates():
        open_status_id = 1
        open_status = db.session.scalar(db.select(EventStatus).where(EventStatus.id==open_status_id ))
        for event in open_status.events:
            current_datetime = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            combined_datetime = datetime.combine(event.date, event.start_time).strftime("%d/%m/%Y, %H:%M:%S")
            if current_datetime > combined_datetime:
                event.status_id = 2
        db.session.commit()
    
        
    def update_purchased_tickets(self):
        bookings = Booking.query.filter(Booking.event_id == self.id).all()
        new_purchased_tickets = sum(booking.tickets for booking in bookings)
        print(new_purchased_tickets)
        new_remaining_tickets = self.total_tickets - new_purchased_tickets
        print(new_remaining_tickets)
        self.purchased_tickets = new_purchased_tickets
        self.remaining_tickets = new_remaining_tickets
        self.update_status()
        
    
        
        
        
    
    
class EventTag(db.Model):
    __tablename__ = 'event_tags'
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    age_group_id = db.Column(db.Integer, db.ForeignKey('event_age_groups.id'), nullable=False)
    campaign_focus_id = db.Column(db.Integer, db.ForeignKey('event_campaign_focuses.id'), nullable=False)
    lower_player_skill_level_id = db.Column(db.Integer, db.ForeignKey('event_player_skill_levels.id'), nullable=False)
    higher_player_skill_level_id = db.Column(db.Integer, db.ForeignKey('event_player_skill_levels.id'), nullable=False)
    one_shot = db.Column(db.Boolean, default=False)
    session_zero = db.Column(db.Boolean, default=False)
    homebrew = db.Column(db.Boolean, default=False)
    open_world = db.Column(db.Boolean, default=False)
    event = db.relationship("Event", backref="tags", uselist=False)
    lower_player_skill_level = db.relationship("PlayerSkillLevel", foreign_keys=[lower_player_skill_level_id],uselist=False)
    higher_player_skill_level = db.relationship("PlayerSkillLevel", foreign_keys=[higher_player_skill_level_id],uselist=False)
    
class AgeGroup(db.Model):
    __tablename__ = 'event_age_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False, unique=True)
    event_tags = db.relationship('EventTag', backref='age_group')
        
class CampaignFocus(db.Model):
    __tablename__ = 'event_campaign_focuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False, unique=True)
    event_tags = db.relationship('EventTag', backref='campaign_focus')
    
class PlayerSkillLevel(db.Model):
    __tablename__ = 'event_player_skill_levels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False, unique=True)
    
    def get_event_tags(self):
        db.session.scalar(db.select(EventTag).where(EventTag.lower_player_skill_level_id <= self.id and EventTag.lower_player_skill_level_id >= self.id))
    
    

            
        
        
    
class EventImage(db.Model):
    __tablename__ = 'event_images'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    filepath = db.Column(db.String(400))
    
    @staticmethod
    def save_event_images(images :list, event):
        BASE_PATH = os.path.dirname(__file__)
        if images.count == 0:
            return
        for image in images:
            print(image)
            filename = image.filename
            upload_path = os.path.join(BASE_PATH, 'static//uploads', secure_filename(filename))
            db_upload_path = 'uploads/' + secure_filename(filename)
            image.save(upload_path)
            event_image = EventImage(event_id=event.id,filepath=db_upload_path)
            db.session.add(event_image)
    
    @staticmethod
    def delete_event_images(event):
        for old_image in event.images:
            db.session.delete(old_image)
    

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    unique_identifier = db.Column(db.String(100), index=True, nullable=False)
    tickets = db.Column(db.Integer, nullable=False)
    purchase_date =  db.Column(db.DateTime, nullable=False)
    
    def format_datetime(self):
        str = self.purchase_date.strftime("%d/%m/%Y, %H:%M:%S")
        return str
    
    @staticmethod
    def generate_uid():
        unique_id = str(uuid4())
        return unique_id

    
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(100), nullable=False)
    def format_datetime(self):
        str = self.created_at.strftime("%d/%m/%Y, %H:%M:%S")
        return str
    
