from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import desc
from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(100), index=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    events = db.relationship('Event', backref='owner')
    comments = db.relationship('Comment', backref='user')
    bookings = db.relationship('Booking', backref='user')




class EventStatus(db.Model):
    __tablename__ = 'event_statuses'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True)
    events = db.relationship("Event",backref='event_status')
    

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
    def get_events(self):
        pass
            
        
        
    
class EventImage(db.Model):
    __tablename__ = 'event_images'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    filepath = db.Column(db.String(400))
    

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    unique_identifier = db.Column(db.String(100), index=True, nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False)
    purchase_date =  db.Column(db.DateTime, nullable=False)

    
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(100), nullable=False)
    def format_datetime(self):
        str = self.created_at.strftime("%d/%m/%Y, %H:%M:%S")
        return str
    
