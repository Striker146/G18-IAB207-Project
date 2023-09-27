from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    

class EventStatus(db.Model):
    __tablename__ = 'event_statuses'
    id = db.Column(db.Integer, primary_key=True)
    statusType = db.Column(db.String(100), primary_key=True)
    

class GameSystem(db.Model):
    __tablename__ = 'game_systems'
    id = db.Column(db.Integer, primary_key=True)
    game_system = db.Column(db.String(100), primary_key=True)
    
    

    
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
    time = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String(400))
    total_tickets = db.Column(db.Integer, nullable=False)
    purchased_tickets = db.Column(db.Integer, default=0, nullable=False)
    remaining_tickets = db.Column(db.Integer, default=0, nullable=False)
    

class Booking:
    def __init__(self):
        self.id = None
        self.unique_identifier = None
        self.seats_booked = None
        self.purchase_date =  None
        self.user:User = None
        self.event:Event = None
        
    def register(self,seats_booked,purchase_date,user:User, event : Event):
        self.seats_booked = seats_booked
        self.purchase_date = purchase_date
        self.user = user
        self.event = event
        self.event.purchase_tickets(seats_booked)
        
    def __repr__(self):
        str = f"id{self.id},unique_identifier:{self.unique_identifier},seats_booked:{self.seats_booked},purchased_date:{self.purchase_date},user:{self.user.id}, event:{self.event.id}"
        return str
    
class Comment:
    def __init__(self):
        self.id = None
        self.user = None
        self.message = None
        self.date = None
        self.time = None
        
    def register(self, user, message, date,time):
        self.user = user
        self.message = message
        self.date = date
        self.time = time
        
    