import sqlite3

class Base(object):
    def open(self):
        self.db = sqlite3.connect("models/data.db")
        return self.db.cursor()

    def close(self):
        self.db.commit()
        self.db.close()
