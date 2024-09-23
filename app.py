from flask import Flask, jsonify, request
from data_dict_simple import simple
from members import read, reset_db

app = Flask(__name__)

# function to remove based on the ids
def remove_by_id(data, id_to_remove):
    data = [item for item in data if data['id'] != id_to_remove]

# routes
@app.route('/members')
def read_all():
    return jsonify(simple)

@app.route('/members', methods=['POST'])
def create():
    data = request.get_json()
    simple.append(data)
    return jsonify(simple), 201


@app.route('/members/<int:id_to_remove', methods=['DELETE'])
def delete_member(id_to_remove):
    try:
        rows_affected = remove_by_id(id_to_remove)
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

app.run()



