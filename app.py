from flask import Flask, request, jsonify
from flask_cors import CORS
import database_actions as dba
# import mysql.connector
# from mysql.connector import Error

#Configuration

app = Flask(__name__)
CORS(app)

# Routes 
# Mostly just placeholders based on the specs until the database communication is implemented

@app.route("/login", methods=["POST"])
def login():
    # Get JSON data from the POST request
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({'error': 'Email and password are required!'}), 400

    result = dba.login_query(email, password)

    # Check for database error
    if isinstance(result, dict) and 'error' in result:
        return jsonify({'error': result['error']}), 500
  
    # Handle successful login
    if result:
        employer_id = result[0]  # Extract the employer ID from the tuple
        return jsonify({'message': 'success', 'employer_id': employer_id}), 200
  
    # Handle invalid email or password
    return jsonify({'error': 'Invalid email or password'}), 401


@app.route("/create-account", methods=["POST"])
def create_account():
    # Get JSON data from the POST request
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({'error': 'Email and password are required!'}), 400

    result = dba.create_account_query(email, password)

    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify(result), 201


@app.route("/create-quiz", methods=["POST"])
def create_quiz():
    # Get JSON data from the POST request
    data = request.json

    # Run query and retrieve the result 
    result = dba.create_quiz(data)

    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify(result), 201


@app.route("/delete-quiz", methods=["POST"])
def delete_quiz():
    data = request.json
    employer_id = data.get('employer_id')
    quiz_id = data.get('quiz_id')

    if not employer_id or not quiz_id:
        return jsonify({'error': 'Employer ID and Quiz ID are required!'}), 400

    result = dba.delete_quiz(employer_id, quiz_id)

    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify(result), 200

@app.route("/update-quiz", methods=["GET", "POST"])
def update_quiz():
    return 

@app.route("/read-quiz", methods=["GET", "POST"])
def read_quiz():
    return 

@app.route("/quiz-results", methods=["GET", "POST"])
def read_quiz_results():
    return 

@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    return 

@app.route("/delete-question", methods=["GET", "POST"])
def delete_question():
    return 

@app.route("/modify-question", methods=["GET", "POST"])
def modify_question():
    return 

@app.route("/read-question", methods=["GET", "POST"])
def read_question():
    return 

# Listener
if __name__ == "__main__":

    app.run(port=4546, debug=True)