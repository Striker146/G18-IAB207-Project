class User:
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.email = None

    def register(self, username, password, email):
        self.user_name = username
        self.password = password
        self.email = email

    def __repr__(self):
        str = "Name :{}, Email: {}, User type: {}"
        str = str.format(self.user_name,self.email,self.user_type)
        return str