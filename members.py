import sqlite3
from data_dict import create_random_user
from app import delete_member

def create_table():
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            birth_date TEXT,
            gender TEXT,
            email TEXT,
            phonenumber TEXT,
            address TEXT,
            nationality TEXT,
            active BOOLEAN,
            github_username TEXT
        )
    ''')

def create_user_in_db(num_users):

    with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()
        users = [create_random_user() for _ in range(num_users)]
        
        cur.executemany('''
        INSERT INTO members (
            first_name, last_name, birth_date, gender, email, phonenumber, 
            address, nationality, active, github_username
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [(user["first_name"], user["last_name"], user["birth_date"], user["gender"],
           user["email"], user["phonenumber"], user["address"], user["nationality"],
           user["active"], user["github_username"]) for user in users])
        

def read():
    members = []

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members')

        for i in cur.fetchall():
            members.append(i)
    
    return members

def reset_db():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS members')
        
        create_table()
        create_user_in_db(10)

def delete_user():
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()

    cur.execute('DELETE FROM members WHERE id = ?', (id_to_remove,))  

    rows_affected = cur.rowcount
    return rows_affected  

