from ..base import Base
from hashlib import sha512
from functions.email import *
from functions.random import random_key

def encrypt(text):
    return sha512(text.encode()).hexdigest()

class User(Base):
    def __init__(self, identity):
        """A class which represents a single row in the table users.
Can be called either as User(email) or User(id)"""
        cur = self.open()
        values = cur.execute("SELECT * FROM users where id=? OR email=?", [identity, identity]).fetchone()
        self.close()
        if values == None: #invalid ID
            raise ValueError("No user has {} as their id or email".format(identity))
        self.id, self.email, self.state, self.key, self.first, self.last, self.pwd = values

    def save(self):
        """saves the changes made to the instance to the database"""
        cur = self.open()
        cur.execute("UPDATE users SET email=?, state=?, key=? first=?, last=?, password=? WHERE id=?", [self.email, self.state, self.key, self.first, self.last, self.pwd, self.id])
        self.close()

    def discard(self):
        """discards any changes made to the instance since the last save to the database"""
        self.__init__(self.id)

    def __repr__(self):
        return "{}: {} {}".format(self.email, self.first, self.last)

    def login(self, password):
        """returns a boolean corresponding to whether the password was correct"""
        if self.pwd == encrypt(password):
            #create some session data. do that later
            return True
        else:
            return False

    def chgPwd(self, newpwd):
        """changes the password for this user (check authentication BEFORE using this) and saves the user to the database"""
        self.pwd = newpwd
        self.save()

    def getClasses(self):
        cur = self.open()
        cur.execute("SELECT classid FROM studentclass WHERE studentid=?", [self.id])
        result = [x[0] for x in cur.fetchall()] #turns list of 1-item tuples into list
        self.close()
        return result

    def prepareReset(self):
        cur = self.open()
        new_key = random_key(200)
        cur.execute("UPDATE users SET key=? WHERE ID=?", [new_key, self.id])
        send_email(self.email, "Password reset for CHS assignment management system",
        """A password reset has been requested for this account on the CHS assignment management system. If you did not click this link, discard this message
{address}/reset/{key}""".format(address=WEBSITE_ADDRESS, key=new_key))
        self.close()