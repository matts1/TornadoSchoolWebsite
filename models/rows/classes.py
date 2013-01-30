from functions.db import *

class Class(object):
    def __init__(self, id):
        self.id = id
        result = queryone("SELECT * FROM classes WHERE id=?", [self.id])
        if result == None:
            raise ValueError("There is no class with the ID specified")
        self.id, self.year, self.name, self.key, self.teacher = result