from ..base import Base
from models.rows.users import User, encrypt
from functions.email import send_email
from functions.random import random_key

WEBSITE_ADDRESS = "http://220.233.10.213:8888"

class Users(Base):
    def login(self, email, password):
        try:
            user = User(email)
        except ValueError: #no user matches
            return False
        if not user.login(password):
            return False
        return True

    def get_user(self, identity):
        """identity is either the user's email or id. Returns a user class with
        the correct user, or a ValueError if no user matches"""
        return User(identity)

    def register(self, fields):
        """validates the data then registers and returns True if it is valid (otherwise returns false)"""
        if len(fields) != 5:
            raise ValueError("fields needs to contain 5 items")
        email, first, last, pwd, conf_pwd = fields
        if pwd != conf_pwd:
            return False
        try:
            User(email)
            return False
        #ValueError means that user could not be found, and the username is free
        except ValueError:
            fields = [email, random_key(200), first, last, pwd]
            if None not in fields and "" not in fields:
                first = fields[2] = first.title()
                last = fields[3] = last.title()
                fields[-1] = encrypt(fields[-1])
                send_email([email], "Registration for assignment management system",
                        """Hi {first} {last}.
You have signed up for the CHS assignment management system. In order to activate your account, you must click on this link.
{address}/activate/{code}
If you did not register for this account, delete this email and nothing will happen.""".format(first=first, last=last, address=WEBSITE_ADDRESS, code=fields[1]))
                cur = self.open()
                cur.execute("INSERT INTO users VALUES (NULL, ?, 0, ?, ?, ?, ?);", fields)
                self.close()
                return True

    def activate(self, key):
        cur = self.open()
        cur.execute("UPDATE users SET state=1 WHERE state=0 AND key=?", [key])
        self.close()
