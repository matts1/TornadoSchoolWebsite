from models.rows.users import User, encrypt
from functions.email import *
from functions.random import random_key
from functions.db import *

class Users(object):
    def login(self, email, password):
        if None in [email, password]:
            return None
        try:
            user = User(email)
        except ValueError: #no user matches
            return False
        if not user.login(password):
            return False
        return User(email)

    def get_user(self, identity):
        """identity is either the user's email or id. Returns a user class with
        the correct user, or a ValueError if no user matches"""
        return User(identity)

    def get_activated_user(self, identity):
        user = User(identity)
        if user.is_activated():
            return user
        raise ValueError("User not activated")

    def get_users_by_reset(self, reset):
        result = queryone("SELECT id FROM users WHERE key=? AND (state=1 OR state=4 OR state=5)", [reset])
        if result == None:
            return None
        return User(result[0])

    def get_teachers(self):
        teachers = queryall("SELECT id FROM users WHERE state>2")
        return [User(teacher[0]) for teacher in teachers]

    def register(self, fields):
        """validates the data then registers and returns True if it is valid (otherwise returns false)"""
        if len(fields) != 6:
            raise ValueError("fields needs to contain 6 items")
        fields[-1] = bool(fields[-1]) * 2
        email, first, last, pwd, conf_pwd, teacher = fields
        if pwd != conf_pwd:
            return False
        try:
            User(email)
            return False
        #ValueError means that user could not be found, and the username is free
        except ValueError:
            fields = [email, teacher, random_key(200), first, last, pwd]
            if None not in fields and "" not in fields:
                if len(pwd) < 6:
                    return False
                first = fields[3] = first.title()
                last = fields[4] = last.title()
                fields[-1] = encrypt(fields[-1])
                send_email([email], "Registration for assignment management system",
                    """Hi {first} {last}.
You have signed up for the CHS assignment management system. In order to activate your account, you must click on this link.
{address}/activate/{code}
If you did not register for this account, delete this email and nothing will happen.""".format(first=first, last=last, address=WEBSITE_ADDRESS, code=fields[2]))
                query("INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?, ?);", fields)
                return True

    def activate(self, key):
        query("UPDATE users SET state=state+1, key=? WHERE (state=0 OR state=2) AND key=?", [random_key(200), key])
