"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todo
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }
#     return jsonify(response_body), 200


#Todo list

@app.route('/todos', methods=['GET'])
def get_todos():
    response = Todo.get_all()

    todos = []
    for todo in response:
        todos.append(todo.serialize())

    return jsonify(todos), 200

@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.get(id)

    return jsonify(todo.serialize()), 200


@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.get(id)
    todo.update(request.get_json())

    return jsonify(todo.serialize()), 200

@app.route('/todos', methods=['POST'])
def create_todos():
    todo = Todo.create(request.get_json())

    return jsonify(todo.serialize()), 200

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.get(id)
    todo = todo.destroy()

    return "Todo " + str(id) + " was successfully deleted", 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)