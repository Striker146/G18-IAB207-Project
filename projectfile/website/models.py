from flask_login import UserMixin
from datetime import datetime
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
    statusType = db.Column(db.String(100))
    events = db.relationship("Event",backref='event_status')
    

class GameSystem(db.Model):
    __tablename__ = 'game_systems'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
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
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    purchased_tickets = db.Column(db.Integer, default=0, nullable=False)
    remaining_tickets = db.Column(db.Integer, default=0, nullable=False)
    comments = db.relationship('Comment', backref='event')
    images = db.relationship('EventImage',backref="event")
    bookings = db.relationship("Booking",backref="event")
    
    def __repr__(self):
        str = f"id {self.id}, title:{self.title}"
        return str
    
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
    purchase_date =  db.Column(db.DateTime, default=datetime.now())

    
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    message = db.Column(db.String(100), nullable=False)