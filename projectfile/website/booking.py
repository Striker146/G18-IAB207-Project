from user import User
from event import Event

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
    
    
if __name__ == "__main__":
    test_booking = Booking()
    test_user = User()
    test_user.register("Hello", "blah blah blah","I am and a emailoo")
    test_event = Event()
    test_event.register("The scandaviation fligcer",test_user,"blah",40,"your house","Time of birth","date of birth","www.lmao.com.au",20,"enumer","DnD 5e",True,True,"low - mid")
    test_booking.register(2,"now",test_user,test_event)
    print(test_booking)