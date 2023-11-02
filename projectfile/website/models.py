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
    address = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    
    events = db.relationship('Event', backref='owner', order_by='Event.id.desc()')
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
    events = db.relationship("Event",backref='game_system', order_by='Event.id.desc()')
    
    

    
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('event_statuses.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_system_id = db.Column(db.Integer, db.ForeignKey('game_systems.id'))
    title = db.Column(db.String(100), index=True, nullable=False)
    description = db.Column(db.String(1000), index=True, nullable=False)
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
        soldout_status_id = 3
        open_status = db.session.scalar(db.select(EventStatus).where(EventStatus.id==open_status_id))
        closed_status = db.session.scalar(db.select(EventStatus).where(EventStatus.id==soldout_status_id))
        checked_statuses = [open_status, closed_status]
        for status_group in checked_statuses:
            for event in status_group.events:
                current_datetime = datetime.now()
                combined_datetime = datetime.combine(event.date, event.start_time)
                print(combined_datetime)
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
        if not event.status.id == 1:
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
    

def generate_comments():
    import random

    comments = [
        "This event looks like a blast! Can't wait to roll some dice and embark on an epic adventure with fellow gamers.",
        "I'm a newbie to TTRPGs, but this event seems perfect for beginners. Excited to learn and have fun!",
        "Hey, I'm a game master looking for players. This event caught my eye – any takers for a homebrew campaign?",
        "The setting for this game sounds so intriguing. I can't resist joining in to explore this unique world.",
        "I've been itching to play a rogue for a while. Anyone in this event need a skilled thief in their party?",
        "I'm all about roleplaying and character development. If this event emphasizes that, count me in!",
        "Do you need a cleric in your group? I'll bring the healing spells and divine wisdom!",
        "This event's DM has a reputation for amazing storytelling. Count me in for a night of immersive storytelling.",
        "Looking for a group that's LGBTQ+ friendly. Let's make some awesome memories together in this event!",
        "I'm a dedicated dice collector, and I'd love to roll some of my rare sets during this event. Who's up for some lucky rolls?",
        "What kind of snacks and drinks are you all bringing to this event? Let's share some delicious ideas!",
        "I appreciate a good balance of combat and storytelling in TTRPGs. Is this event a good mix?",
        "I'm in a different time zone but eager to join the event. Will it be recorded or have flexible scheduling?",
        "If you're a fellow artist, I'd love to collaborate on character illustrations or maps for this event!",
        "Let's discuss character backstories and plot hooks for this event – I'm all about weaving intricate tales.",
        "I'm new to this platform, but this event description is so inviting. How do I sign up and get started?",
        "I've got a bunch of miniatures and terrain pieces. Will they come in handy for this event?",
        "As a parent, I'd love to introduce my kids to TTRPGs. Is this event family-friendly?",
        "Is this event for experienced players only, or can newbies like me join in and learn the ropes?",
        "I'm looking for a long-term campaign. Is this a one-shot event, or will it lead to an ongoing adventure?"
        "I'm a seasoned adventurer, and I'm here to challenge your party's mettle in this event.",
        "I've got a unique character concept that I'm excited to bring to life in this TTRPG event. Let's make it memorable!",
        "This event's DM is known for their creativity. I can't wait to see what surprises they have in store for us.",
        "I'm all about the tactical side of TTRPGs. Let's strategize and conquer challenges together at this event.",
        "Looking for a group that enjoys a good laugh and a sense of humor in their roleplaying. Count me in!",
        "This event's theme reminds me of my favorite fantasy novels. Let's bring those stories to life at the gaming table.",
        "I've got a character idea that's a bit off the beaten path. Who's up for some unconventional roleplay?",
        "Do you prefer old-school tabletop or digital dice rollers? Let's discuss our dice-rolling methods before the event.",
        "I'm a bard at heart, and I'm ready to provide the party with some musical inspiration during our adventures.",
        "This event is my weekly highlight. Can't wait to catch up with friends and embark on new quests.",
        "I'm a dungeon master looking for a new challenge. Who's ready to tackle my devious traps and puzzles in this event?",
        "I've got a plethora of unique character voices and accents to bring to the table. Get ready for some immersive roleplay!",
        "Who's up for some in-character feasting at the tavern after a successful quest in this event?",
        "If you're a fellow lore enthusiast, let's dive deep into the world's history and legends during this event.",
        "I've got a treasure trove of rare TTRPG books. We can use them for inspiration and reference during this event.",
        "I'm a worldbuilder and love crafting unique settings. Let's explore new realms together in this event.",
        "Count me in if you appreciate a mix of traditional and indie TTRPG systems. Variety keeps the gaming experience fresh!",
        "I'm ready to flex my creative muscles in this event. Bring on the challenging puzzles and brain-teasers!",
        "Let's share our favorite in-game stories and memorable moments from past campaigns during this event.",
        "If you're new and have questions about character creation, feel free to ask. We're here to help in this event!",
        "I've got a whole arsenal of props and costumes for immersive roleplay. Who's up for some theatrical TTRPG fun?"
        "I'm excited to explore the mysteries of this world and uncover hidden secrets during this event.",
        "For those who enjoy a healthy dose of intrigue and plot twists, this event promises an engaging experience.",
        "I'm a fan of TTRPG podcasts, and I'm hoping this event will be as exciting as the stories I've heard.",
        "Let's create a diverse party with characters from different backgrounds and races for this event.",
        "This event is my escape from reality. Can't wait to immerse myself in a fantastic realm with all of you.",
        "If you appreciate a challenging puzzle or riddle, I'm your teammate for this event. Let's crack some mysteries!",
        "I'm a fan of storytelling through maps. Anyone interested in exploring detailed worlds in this event?",
        "Looking for a group that enjoys intense, character-driven drama. We'll make our own stories in this event.",
        "I'm eager to make new friends and build connections through shared adventures in this event.",
        "I'm known for my elaborate character sheets and detailed backgrounds. Ready to dive into this event's world.",
        "I'm a fan of a well-timed twist. Expect the unexpected in my campaigns, and let's embrace the chaos in this event!",
        "As a lover of mythology, I'm looking for an event with rich lore inspired by ancient legends and folklore.",
        "I enjoy mixing in a little comedy with my roleplay. Let's bring some laughter to this event's epic quests.",
        "I'm a fan of dark and gritty settings. Can't wait to explore the shadows and confront the unknown in this event.",
        "Ready to join forces and form a legendary party with fellow adventurers during this event.",
        "This event will be a chance to escape into a world of magic, monsters, and limitless possibilities.",
        "I appreciate a DM who knows how to keep the story engaging. Hoping for a thrilling narrative in this event.",
        "Looking for players who enjoy tackling moral dilemmas and tough decisions in the games we play.",
        "I'm a collector of rare in-game artifacts and relics. Who wants to trade or barter during this event?",
        "Let's create an unforgettable story together during this event. The possibilities are limited only by our imaginations!"]

    events = range(20)
    events = events[1:]
    users = range(5)
    users = users[1:]

    for event in events:
        amount = random.randint(3,9)
        for i in range(amount):
            user = random.choice(users)
            message = random.choice(comments)
            comment = Comment(user_id=user, event_id = event, created_at = datetime.now(), message = message)
            db.session.add(comment)
    db.session.commit()