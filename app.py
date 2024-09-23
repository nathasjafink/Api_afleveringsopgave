from flask import Flask, jsonify, request
from data_dict_simple import simple

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
def delete():
    data = request.get_json()
    data.remove(remove_by_id(data, id_to_remove))
    return jsonify(simple)


app.run()



