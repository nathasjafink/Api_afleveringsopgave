from flask import Flask, jsonify, request
from members import read, reset_db, delete_user, create_user_in_db


app = Flask(__name__)


# Routes
# Reads the db
@app.route('/members')
def read_all():
    return jsonify(read())

# Create user in the db
@app.route('/members', methods=['POST'])
def create():
    data = request.get_json()
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

# RESET 
@app.route('/reset')
def reset():
    reset_db()
    return jsonify(read())

# Update users information in db 
@app.route('/members/<int:id>', methods=['PUT'])
def update_user(id):
    member_data = request.get_json()
    if not member_data:
        return jsonify({"error": "Invalid data"}), 400
    
    rows_affected = update_user(id, member_data)
    if rows_affected == 0:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify({"message": "Member updated successfully"}), 200


# Patch 
@app.route('/members/<int:id>/toggle-active', methods=['PATCH'])
def toggle_member_active_status (id):
    rows_affected = toggle_member_active_status(id)

    if rows_affected == 0:
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify({"message": "Member active status toggled successfully"}), 200

app.run()



