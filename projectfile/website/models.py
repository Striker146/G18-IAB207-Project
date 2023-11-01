from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import desc
from . import db
from uuid import uuid1
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
        if self.remaining_tickets ==0:
            self.status_id == 3
    
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
    
    def get_tag_messages(self):
        tags = [self.age_group.get_tag_message(),
                self.campaign_focus.get_tag_message(),
                PlayerSkillLevel.get_tag_message(self.lower_player_skill_level,self.higher_player_skill_level)]
        if self.one_shot:
            tags.append("One Shot")
        if self.session_zero:
            tags.append("Session Zero")
        if self.homebrew:
            tags.append("Homebrew")
        if self.open_world:
            tags.append("Open World")
        
        return tags
        

    
class AgeGroup(db.Model):
    __tablename__ = 'event_age_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False, unique=True)
    event_tags = db.relationship('EventTag', backref='age_group')
    def get_tag_message(self):
        match self.id:
            case 1:
                return "All Ages"
            case 2:
                return "18+ Only"
            case 3:
                return "Under 18 Only"
                
            
        
class CampaignFocus(db.Model):
    __tablename__ = 'event_campaign_focuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False, unique=True)
    event_tags = db.relationship('EventTag', backref='campaign_focus')
    
    def get_tag_message(self):
        match self.id:
            case 1:
                return "Roleplay and Combat Focused"
            case 2:
                return "Combat Focused"
            case 3:
                return "Roleplay Focused"

class PlayerSkillLevel(db.Model):
    __tablename__ = 'event_player_skill_levels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False, unique=True)
    
    def get_event_tags(self):
        db.session.scalar(db.select(EventTag).where(EventTag.lower_player_skill_level_id <= self.id and EventTag.lower_player_skill_level_id >= self.id))
    
    @staticmethod
    def get_tag_message(lower_level, higher_level):
        if lower_level.id == higher_level.id:
            return f"{lower_level.name} Player's Only"
        else:
            return f"For {lower_level.name} - {higher_level.name} Players"
        
    
    

            
        
        
    
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
    total_cost = db.Column(db.Float(100), index=True, nullable=False)
    
    def format_datetime(self):
        str = self.purchase_date.strftime("%d/%m/%Y, %H:%M:%S")
        return str
    
    @staticmethod
    def generate_uid():
        unique_id = str(uuid1())
        unique_id = unique_id[0:8]
        return unique_id
    
    @staticmethod
    def is_valid_booking(event,tickets_purchased):
        valid_booking = [True,'']
        if event.status.id == 2 or event.status.id == 3 or event.status.id == 4:
            valid_booking[1] =  """Error: This event is no longer available for purchase"""
            valid_booking[0] = False
            return valid_booking
        if event.remaining_tickets < tickets_purchased:
            valid_booking[1] = """Error: Insufficient Tickets Available. You have requested more tickets than are currently available for purchase. Please update the quantity and try again."""
            valid_booking[0] = False
            return valid_booking
        else:
            return valid_booking

    
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(100), nullable=False)
    def format_datetime(self):
        str = self.created_at.strftime("%d/%m/%Y, %H:%M:%S")
        return str
    
