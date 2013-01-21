import sqlite3

import os
os.system("rm data.db")

with sqlite3.connect("data.db") as db:
    cur = db.cursor()
    for tablename in ["student", "teacher"]:
        cur.execute("""CREATE TABLE {} (
            id INTEGER,
            email TEXT UNIQUE NOT NULL,
            first TEXT NOT NULL,
            last TEXT NOT NULL,
            password TEXT NOT NULL,
            PRIMARY KEY (id)
        );""".format(tablename))

    cur.execute("""CREATE TABLE course (
        id INTEGER,
        name TEXT NOT NULL,
        subject TEXT NOT NULL,
        year INTEGER NOT NULL,
        class INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY (class) REFERENCES class (id)
    );""")

    cur.execute("""CREATE TABLE work (
        id INTEGER,
        type TEXT NOT NULL,
        course INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (course) REFERENCES course (id)
    );""")#need to add more stuff into work - no clue what yet

    cur.execute("""CREATE TABLE class (
        id INTEGER,
        year INTEGER NOT NULL,
        subject TEXT NOT NULL,
        letter TEXT NOT NULL,
        teacher INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (teacher) REFERENCES teacher (id)
    );""")

    cur.execute("""CREATE TABLE studentwork (
        student INTEGER NOT NULL,
        work INTEGER NOT NULL,
        completed INTEGER NOT NULL,
        mark INTEGER NOT NULL,
        comment TEXT,
        PRIMARY KEY (student, work),
        FOREIGN KEY (student) REFERENCES student (id),
        FOREIGN KEY (work) REFERENCES work (id)
    );""")

    cur.execute("""CREATE TABLE studentclass (
        student INTEGER,
        class INTEGER,
        PRIMARY KEY (student, class),
        FOREIGN KEY (student) REFERENCES student (id),
        FOREIGN KEY (class) REFERENCES class (id)
    );""")

    cur.execute("""CREATE TABLE session (
        session_id TEXT,
        user INTEGER,
        FOREIGN KEY (user) REFERENCES users(id),
        UNIQUE (session_id)
    );""")
