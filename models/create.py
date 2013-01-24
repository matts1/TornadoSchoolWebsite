import sqlite3

import os
db_file = "{}/data.db".format(__file__[::-1].split("/",1)[1][::-1])
print("creating db at {}".format(db_file))
os.system("rm " + db_file)

with sqlite3.connect(db_file) as db:
    cur = db.cursor()
    cur.execute("""CREATE TABLE users (
        id INTEGER,
        email TEXT UNIQUE NOT NULL,
        state INTEGER NOT NULL,
        key TEXT UNIQUE NOT NULL,
        first TEXT NOT NULL,
        last TEXT NOT NULL,
        password TEXT NOT NULL,
        PRIMARY KEY (id)
    );""")#need to add settings

    cur.execute("""CREATE TABLE courses (
        id INTEGER,
        name TEXT NOT NULL,
        subject TEXT NOT NULL,
        year INTEGER NOT NULL,
        class INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY (class) REFERENCES classes (id)
    );""")

    cur.execute("""CREATE TABLE work (
        id INTEGER,
        type TEXT NOT NULL,
        course INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (course) REFERENCES courses (id)
    );""")#need to add more stuff into work - no clue what yet

    cur.execute("""CREATE TABLE classes (
        id INTEGER,
        year INTEGER NOT NULL,
        subject TEXT NOT NULL,
        letter TEXT NOT NULL,
        teacher INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (teacher) REFERENCES users (id)
    );""")

    cur.execute("""CREATE TABLE studentwork (
        student INTEGER NOT NULL,
        work INTEGER NOT NULL,
        completed INTEGER NOT NULL,
        mark INTEGER NOT NULL,
        comment TEXT,
        PRIMARY KEY (student, work),
        FOREIGN KEY (student) REFERENCES users (id),
        FOREIGN KEY (work) REFERENCES work (id)
    );""")

    cur.execute("""CREATE TABLE studentclass (
        student INTEGER,
        class INTEGER,
        PRIMARY KEY (student, class),
        FOREIGN KEY (student) REFERENCES users (id),
        FOREIGN KEY (class) REFERENCES class (id)
    );""")

    cur.execute("""CREATE TABLE session (
        session_id TEXT,
        user INTEGER,
        FOREIGN KEY (user) REFERENCES users (id),
        UNIQUE (session_id)
    );""")
