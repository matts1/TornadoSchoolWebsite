from functions.db import *
from functions.random import random_key
import string

class Classes(object):
    def add(self, teacher_id, name, year, key):
        if None in [name, year, key]:
            return ["", ""]
        if name == "":
            return ["", "Name should not be empty"]
        if not (year.isdigit() and 6 < int(year) < 13):
            return ["", "Year should be a number between 7 and 12"]
        if queryone("SELECT id FROM classes WHERE name=?", [name]) != None:
            return ["", "That name for a class is already taken"]

        while key == "":
            key = random_key(10, string.ascii_lowercase+string.digits)
            if queryone("SELECT id FROM classes WHERE key=?", [key]) != None:
                key = ""

        #at this point, everything is valid
        query("""INSERT INTO classes VALUES (
        NULL, ?, ?, ?, ?
        )""", [year, name, key, teacher_id])
        return ["The class {} has been created. Use the key {} to let students join".format(name, key), ""]

    def join(self, userid, key):
        classid = queryone("SELECT name, id FROM classes WHERE key=?", [key])
        if classid == None:
            return [False, "There is no class with that key"]
        res = queryone("SELECT * FROM studentclass WHERE student=? AND class=?", [userid, classid[1]])
        if res != None:
            return [False, "You are already in the class {}".format(classid[0])]
        query("INSERT INTO studentclass VALUES (?, ?)", [userid, classid[1]])
        return [True, "You have joined the class {}".format(classid[0])]