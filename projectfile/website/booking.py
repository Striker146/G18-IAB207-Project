class Booking:
    def __init__(self):
        self.id = None
        self.unique_identifier = None
        self.seats_booked = None
        self.purchase_date =  None
        self.user = None
        self.event = None
        
    def register(self,seats_booked,purchase_date,user,event):
        self.seats_booked = seats_booked
        self.purchase_date = purchase_date
        self.user = user
        self.event = event
        
    def __repr__(self):
        str = f"id{self.id},unique_identifier:{self.unique_identifier},seats_booked:{self.seats_booked},purchased_date:{self.purchase_date},user:{self.user}, event:{self.event}"
        return str
    
    
    