import sqlite3

class BaseTable(object):
    def open(self):
        self.db = sqlite3.connect("../data.db")
        return self.db.cursor()

    def close(self):
        self.db.commit()
        self.db.close()
