from base import BaseModel
from hashlib import sha512

def encrypt(text):
    return sha512(text.encode()).hexdigest()

class Student(BaseModel):
    table = "student"
    def __init__(self, identity):
        """A class which represents a singls row in the table {0}.
Can be called either as {0}(email) or {0}(id)""".format(self.table)
        cur = self.open()
        values = cur.execute("SELECT * FROM {} where id=? OR email=?".format(self.table), [identity, identity]).fetchone()
        assert(values != None) #invalid ID
        self.id, self.email, self.first, self.last, self.pwd = values
        self.close()

    def save(self):
        """saves the changes made to the instance to the database"""
        cur = self.open()
        cur.execute("UPDATE {} SET email=?, first=?, last=?, password=? WHERE id=?".format(self.table), [self.email, self.first, self.last, self.pwd, self.id])
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

    def chg_pwd(self, newpwd):
        """changes the password for this user (check authentication BEFORE using this) and saves the user to the database"""
        self.pwd = newpwd
        self.save()

    def get_classes(self):
        cur = self.open()
        cur.execute("SELECT classid FROM studentclass WHERE studentid=?", [self.id])
        self.close()
        return [x[0] for x in cur.fetchall()] #turns list of 1-item tuples into list

    
        
a = Student(1)
print(a)
a = Student("abc@gmail.com")
print(a)
