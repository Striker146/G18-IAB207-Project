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
        