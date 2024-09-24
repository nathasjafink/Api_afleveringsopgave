import sqlite3
import requests
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

def update_member_in_db (id, member_data):
    with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()

        # Gets the current values for the member 
        cur.execute('SELECT * FROM members WHERE id = ?', (id,))
        current_member = cur.fetchone()

        # get the current values in the db and use the existing if it's not all values there have to be changed.
        # Therefore you can change only some of the values without getting an error. 
        updated_first_name = member_data.get('first_name', current_member[1])  # First name is index 1 in the result set
        updated_last_name = member_data.get('last_name', current_member[2])  # Last name is index 2
        updated_birth_date = member_data.get('birth_date', current_member[3])  # Birth date is index 3
        updated_gender = member_data.get('gender', current_member[4])  # Gender is index 4
        updated_email = member_data.get('email', current_member[5])  # Email is index 5
        updated_phonenumber = member_data.get('phonenumber', current_member[6])  # Phone number is index 6
        updated_address = member_data.get('address', current_member[7])  # Address is index 7
        updated_nationality = member_data.get('nationality', current_member[8])  # Nationality is index 8
        updated_active = member_data.get('active', current_member[9])  # Active status is index 9
        updated_github_username = member_data.get('github_username', current_member[10])  # GitHub username is index 10

        cur.execute('''
            UPDATE members
            SET first_name = ?, last_name = ?, birth_date = ?, gender = ?, email = ?,
                phonenumber = ?, address = ?, nationality = ?, active = ?, github_username = ?
            WHERE id = ?
        ''', (updated_first_name, updated_last_name, updated_birth_date, updated_gender, updated_email,
              updated_phonenumber, updated_address, updated_nationality, updated_active, updated_github_username, id))
        
        rows_affected = cur.rowcount
        return rows_affected
    
def toggle_member_active_status_in_db (id):
     with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()
        
        cur.execute('SELECT active FROM members WHERE id = ?', (id,))
        result = cur.fetchone()

        # if member is not found it remains 0 as in not active
        if result is None:
            return 0  
        
        # Toggle the active status
        current_active_status = result[0]
        new_active_status = not current_active_status  
        
        cur.execute('UPDATE members SET active = ? WHERE id = ?', (new_active_status, id))
        
        rows_affected = cur.rowcount
        return rows_affected
     

# GitHub API
def get_member_by_id(member_id):
    with sqlite3.connect('members.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members WHERE id = ?', (member_id,))
        row = cur.fetchone

        if row is None:
            return None
        
        member = {
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'birth_date': row[3],
            'gender': row[4],
            'email': row[5],
            'phonenumber': row[6],
            'address': row[7],
            'nationality': row[8],
            'active': row[9],
            'github_username': row[10]
        }
        return member
