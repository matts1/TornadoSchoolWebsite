import sqlite3

class BaseModel(object):
    def open(self):
        self.db = sqlite3.connect("../data.db")
        return self.db.cursor()

    def close(self):
        self.db.commit()
        self.db.close()
