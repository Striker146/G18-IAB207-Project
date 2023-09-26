from user import User

class Event:
    def __init__(self):
        self.id = None
        self.title = None
        self.owner:user.User = None
        self.description = None
        self.cost = None
        self.location = None
        self.time = None
        self.date = None
        self.image = None
        self.total_tickets = None
        self.purchased_tickets = 0
        self.remaining_tickets = None
        self.status = None
        self.age_range = None
        self.game_system = None
        self.new_campaign = None
        self.is_oneshot = None
        self.player_experience = None
        
    def register(self, title,owner:User, description, cost, location, time,
                 date, image, total_tickets,age_range, game_system,
                 new_campaign, is_oneshot, player_experience):
        self.title = title
        self.owner:User = owner
        self.description = description
        self.cost = cost
        self.location = location
        self.time = time
        self.date = date
        self.image = image
        self.total_tickets = total_tickets
        self.remaining_tickets = total_tickets
        self.age_range = age_range
        self.game_system = game_system
        self.new_campaign = new_campaign
        self.is_oneshot = is_oneshot
        self.player_experience = player_experience

    def __repr__(self):
        str = f"""title:{self.title},owner:{self.owner.id},description:{self.description},cost:{self.cost},location:{self.location},time:{self.time},date:{self.date},image:{self.image},total_tickets{self.total_tickets}
        purchased_tickets:{self.purchased_tickets},status:{self.status},age_range:{self.age_range},game_system:{self.game_system},new_campaign:{self.new_campaign},is_oneshot{self.is_oneshot},player_experience{self.player_experience}"""
        return str
    
    def purchase_tickets(self,amount):
        self.purchased_tickets = self.purchased_tickets + amount
        self.remaining_tickets = self.total_tickets - self.purchased_tickets
    
if __name__ == "__main__":
    test_event = Event()
    test_user = User()
    test_user.register("a","a","a")
    test_event.register("a",test_user,"a","a","a","a","a","a","a","a","a","a","a","a")
    print(test_event)