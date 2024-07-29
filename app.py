from flask import Flask, request, jsonify
from flask_cors import CORS
import database_actions as dba
# import mysql.connector
# from mysql.connector import Error

#Configuration

app = Flask(__name__)
CORS(app)

# Routes 

@app.route("/login", methods=["POST"])
def login():
    # Get JSON data from the POST request
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({'message': 'Email and password are required!'}), 400

    result = dba.login_query(email, password)

    # Check for database error
    if isinstance(result, dict) and 'error' in result:
        return jsonify({'message': result['error']}), 500
    
    # Handle successful login
    if result:
        return jsonify({'message': 'success', 'employer_id': result}), 200

    # Handle invalid email or password
    return jsonify({'message': 'Invalid email or password'}), 401


@app.route("/create-account", methods=["POST"])
def create_account():
    # Get JSON data from the POST request
    data = request.json

    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({'message': 'Email and password are required!'}), 400

    # Call the function to create account
    result = dba.create_account_query(email, password)

    # Handle the result
    if 'error' in result:
        return jsonify({'message': 'account already exists for that email'}), 500

    return jsonify(result), 201


@app.route("/create-quiz", methods=["POST"])
def create_quiz():
    # Get JSON data from the POST request
    data = request.json

    # Run query and retrieve the result 
    result = dba.create_quiz_query(data)

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

    result = dba.delete_quiz_query(employer_id, quiz_id)

    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify(result), 200

@app.route("/user-quiz", methods=["POST"])
def user_quiz():
    data = request.json
    employer_id = data.get('employer_id')
    print(employer_id)
    # Validate input
    if not employer_id:
        return jsonify({'error': 'Employer ID is required!'}), 400

    result = dba.user_quiz_query(employer_id)

    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify(result)

@app.route("/send-quiz-link", methods=["POST"])
def send_quiz_link():
    data = request.json

    employer_id = data.get('employer_id')
    quiz_id = data.get('quiz_id')
    candidate_email = data.get('candidate_email')
    
    # Validate input
    if not employer_id or not quiz_id or not candidate_email:
        return jsonify({'error': 'Missing fields!'}), 400

    result = dba.send_quiz_link(employer_id, quiz_id, candidate_email)

    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify(result), 200

@app.route("/delete-user", methods=["DELETE"])
def delete_user():
    # Get JSON data from the POST request
    data = request.json
    employer_id = data.get('employer_id')

    # Validate input
    if not employer_id:
        return jsonify({'message': 'Employer ID is required!'}), 400

    # Call the function to delete user
    result = dba.delete_user(employer_id)

    # Handle the result
    if 'error' in result:
        return jsonify({'message': result['error']}), 500

    return jsonify(result), 200


@app.route("/quiz-results", methods=["GET", "POST"])
def read_quiz_results():
    data = request.json
    employer_id = data.get('employer_id')
    quiz_id = data.get('quiz_id')

    # Validate input
    if not employer_id or not quiz_id:
        return jsonify({'message': 'Missing employer id or quiz id!'}), 400

    # Call the function to delete user
    result = dba.quiz_results_query(employer_id, quiz_id)

    # Handle the result
    if 'error' in result:
        return jsonify({'message': result['error']}), 500

    return jsonify(result), 200 
    return  


@app.route("/update-user", methods=["POST"])
def update_user():
    data = request.json
    employer_id = data.get('employer_id')
    email = data.get('email')
    password = data.get('password')
    print(employer_id, email, password)

    # Validate input
    if not employer_id:
        return jsonify({'message': 'Employer ID is required!'}), 400

    # Call the function to update user
    result = dba.update_user(employer_id, email, password)

    # Handle the result
    if 'error' in result:
        return jsonify({'message': result['error']}), 400

    return jsonify(result), 200

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    data = request.json
    quiz_id = data.get('quiz_id')
    candidate_email = data.get('candidate_email')
    quiz_data = data.get('quiz_data')

    # Validate input
    if not quiz_id or candidate_email or quiz_data:
        return jsonify({'message': 'quiz_id, candidate_email, or quiz_data is required!'}), 400

    # Call the function to update user
    result = dba.submit_quiz_query(quiz_id, candidate_email, quiz_data)

    # Handle the result
    if 'error' in result:
        return jsonify({'message': result['error']}), 400

    return jsonify(result), 200
    return


@app.route("/show-quiz", methods=["POST"])
def show_quiz_query():
    data = request.json
    quiz_id = data.get('quiz_id')

    # Validate input
    if not quiz_id:
        return jsonify({'message': 'quiz_id is required!'}), 400

    # Call the function to update user
    result = dba.show_quiz_query(quiz_id)

    # Handle the result
    if 'error' in result:
        return jsonify({'message': result['error']}), 400

    return jsonify(result), 200


# Listener
if __name__ == "__main__":

    app.run(port=4546, debug=True)