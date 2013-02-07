from functions.random import random_key
from functions.db import *

class Sessions(object):
    def register(self, id):
        key = random_key(200)
        query("INSERT INTO sessions VALUES (?, ?, NULL)", [id, key])
        self.refresh(key)
        return key

    def expire(self):
        query("DELETE FROM sessions WHERE expiry < datetime('now', 'localtime');")

    def refresh(self, key):
        #12 hour expiry on sessions
        self.expire()
        query("UPDATE sessions set expiry=datetime('now','localtime','+12 hours') WHERE key=?;", [key])

    def validate(self, key):
        self.expire()
        user = queryone("SELECT user FROM SESSIONS WHERE key=?", [key])
        if user == None:
            return None
        self.refresh(key)
        return user[0]

    def delete(self, key):
        query("DELETE FROM sessions WHERE key=?", [key])

    def deleteuser(self, user):
        query("DELETE FROM sessions WHERE user=?", [user])