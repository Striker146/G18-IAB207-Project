class Event:
    def __init__(self):
        self.id = None
        self.title = None
        self.owner = None
        self.description = None
        self.cost = None
        self.location = None
        self.time = None
        self.date = None
        self.image = None
        self.total_tickets = None
        self.purchased_tickets = None
        self.status = None
        self.age_range = None
        self.game_system = None
        self.new_campaign = None
        self.is_oneshot = None
        self.player_experience = None
        
    def register(self, title,owner, description, cost, location, time,
                 date, image, total_tickets, purchased_tickets, status,
                 age_range, game_system, new_campaign, is_oneshot, player_experience):
        self.title = title
        self.owner = owner
        self.description = description
        self.cost = cost
        self.location = location
        self.time = time
        self.date = date
        self.image = image
        self.total_tickets = total_tickets
        self.purchased_tickets = purchased_tickets
        self.status = status
        self.age_range = age_range
        self.game_system = game_system
        self.new_campaign = new_campaign
        self.is_oneshot = is_oneshot
        self.player_experience = player_experience

    def __repr__(self):
        str = f"""title:{self.title},owner:{self.owner},description:{self.description},cost:{self.cost},location:{self.location},time:{self.time},date:{self.date},image:{self.image},total_tickets{self.total_tickets}
        purchased_tickets:{self.purchased_tickets},status:{self.status},age_range:{self.age_range},game_system:{self.game_system},new_campaign:{self.new_campaign},is_oneshot{self.is_oneshot},player_experience{self.player_experience}"""
        return str
    
if __name__ == "__main__":
    test_event = Event()
    test_event.register("a","a","a","a","a","a","a","a","a","a","a","a","a","a","a","a")
    print(test_event)