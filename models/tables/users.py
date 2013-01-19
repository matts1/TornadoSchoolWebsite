from base import BaseTable
#import student

class Student(BaseTable):
    def login(self, email, password):
        try:
            user = Student(email)
        except AssertionError: #no user matches
            return False
        if not user.login(password):
            return False
        return True
    
    def get_user(self, identity):
        """identity is either the user's email or id. Returns a user class with the correct user, or an AssertionError if no user matches"""
        return Student(identity)
   
   def register(self, email, first, last, pwd, conf-pwd):
        """validates the data then registers and returns True if it is valid (otherwise returns false)"""
        if pwd != conf-pwd:
            return False
        try:
            User(email)
            return False
            #AssertionError is good
        except AssertionError:
            fields = [email, first, last, pwd]
            if None not in fields and "" not in fields:
                cur = self.open()
                cur.execute("INSERT INTO student VALUES (?, ?, ?, ?);", fields)
                self.close()
                return True
