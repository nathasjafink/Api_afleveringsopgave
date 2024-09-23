import sqlite3

def create():

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS members (id INTEGER, name TEXT)')
        cur.execute("INSERT INTO members VALUE('1, 'Nathasja')")
        cur.execute("INSERT INTO members VALUE('2, 'Patrick')")
        cur.execute("INSERT INTO members VALUE('3, 'Magnus')")
        

def read():
    members = []

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members')

        for i in cur.fetchall():
            members.append(i)
    
    return members

create()
