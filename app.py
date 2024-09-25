from dotenv import load_dotenv
from flask import Flask, jsonify, request
from members import read, reset_db, delete_user, create_user_in_db, update_member_in_db, toggle_member_active_status_in_db, get_member_by_id
import os
from services import fetch_github_repos

app = Flask(__name__)

load_dotenv()
github_token = os.getenv('GITHUB_ACCESS_TOKEN')

# Routes
# Reads the db
@app.route('/members')
def read_all():
    return jsonify(read())

# Create user in the db
@app.route('/members', methods=['POST'])
def create():
    create_user_in_db()
    return jsonify(read), 201

# Delete in the db by id 
@app.route('/members/<int:id_to_remove>', methods=['DELETE'])
def delete_member(id_to_remove):
    try:
        rows_affected = delete_user(id_to_remove)
        if rows_affected == 0:
            return jsonify({"error": "Member not found"}), 404
        return jsonify({"message": "Member deleted succesfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# RESET the db table
@app.route('/reset')
def reset():
    reset_db()
    return jsonify(read())

# Update users information in db 
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member_data = request.get_json()

    if not member_data:
        return jsonify({"error": "Invalid data"}), 400

    rows_affected = update_member_in_db(id, member_data)

    if rows_affected == 0:
        return jsonify({"error": "Member not found"}), 404

    return jsonify({"message": "Member updated successfully"}), 200


# Toggle members active status
@app.route('/members/<int:id>/toggle-active', methods=['PATCH'])
def toggle_member_active_status (id):
    rows_affected = toggle_member_active_status_in_db(id)

    if rows_affected == 0:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify({"message": "Member active status toggled successfully"}), 200

# GitHub API
# id nummer 3 er mit eget brugernavn fra github
@app.route('/members/<int:id>/repos', methods=['GET'])
def get_member_repos(id):
    member = get_member_by_id(id)
     
    if not member:
        return jsonify({"error": "Member not found"}), 404
    
    github_username = member.get('github_username')
    
    if not github_username:
        return jsonify({"error": "GitHub username not found"}), 400
    
    if github_username == "your_github_username":
        repos = fetch_github_repos(github_username, token=github_token)
    
    else: 
        repos = fetch_github_repos(github_username)
    
    if repos is None:
        return jsonify({"error": "Could not fetch repositories"}), 500
    
    
    return jsonify(repos), 200

app.run()




