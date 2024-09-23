import sqlite3
from data_dict import create_random_user

def create_table():
    with sqlite3.connect('members.db') as conn:
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

    with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members')

        for i in cur.fetchall():
            members.append(i)
    
    return members

def reset_db():
    with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS members')
        
        create_table()
        create_user_in_db(10)

def delete_user(id_to_remove):
    with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()

        cur.execute('DELETE FROM members WHERE id = ?', (id_to_remove,))  

        rows_affected = cur.rowcount
        return rows_affected  

def update_user (id, member_data):
    with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()

        cur.execute('''
        UPDATE members
        SET first_name = ?, last_name = ?, birth_date = ?, gender = ?, email = ?,
            phonenumber = ?, address = ?, nationality = ?, active = ?, github_username = ?
        WHERE id = ?
    ''', (member_data['first_name'], member_data['last_name'], member_data['birth_date'],
          member_data['gender'], member_data['email'], member_data['phonenumber'],
          member_data['address'], member_data['nationality'], member_data['active'],
          member_data['github_username'], id))
        
        rows_affected = cur.rowcount
        return rows_affected
    
def toggle_member_active_status (id):
     with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()
        cur.execute('''
        UPDATE members
        SET active = NOT active
        WHERE id = ?
    ''', (id,))
        
        rows_affected = cur.rowcount
        return rows_affected