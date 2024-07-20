from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error


# Configuration

app = Flask(__name__)


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

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Prepare and execute SQL query to find the user
        query = "SELECT email, password FROM employer WHERE email = %s"
        cursor.execute(query, (email,))
        
        # Fetch the result
        result = cursor.fetchone()
        
        if result:
            employer_id, stored_password = result
            # Check if the password matches
            if password == stored_password:
                return jsonify({'message': 'success', 'employer_id': employer_id}), 200
            else:
                return jsonify({'error': 'Invalid email or password'}), 401
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        cursor.close()
        conn.close()
    return 

@app.route("/create-account", methods=["POST"])
def create_account():
     # Get JSON data from the POST request
    data = request.json
    
    email = data.get('email')
    password = data.get('password')
    
    # Validate input
    if not email or not password:
        return jsonify({'error': 'Username and password are required!'}), 400

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config) # How do we connect? TODO: This is incorrect 
        cursor = conn.cursor() # TODO: 
        
        # Prepare and execute SQL query
        query = "INSERT INTO employer (email, password) VALUES (%s, %s)"
        cursor.execute(query, (email, password))
        
        # Commit the transaction
        conn.commit()

        # Get the last inserted ID
        employer_id = int(cursor.lastrowid)
        
        return jsonify({
            'message': 'success, user created',
            'employer_id': employer_id
            }), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        cursor.close()
        conn.close()
    return 

@app.route("/create-quiz", methods=["POST"])
def create_quiz():
    data = request.json

    quiz_id = data.get('quiz_id')
    question_title = data.get('question_text')
    question_type = data.get('question_type')
    answers = data.get('answers')
    correct_answer_index = data.get('is_correct')

    # Validate input
    if not quiz_id or not question_title or not question_type or not answers or correct_answer_index is None:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert question into Questions table
        question_query = "INSERT INTO Questions (QuizID, QuestionText, QuestionType) VALUES (%s, %s, %s)"
        cursor.execute(question_query, (quiz_id, question_title, question_type))
        question_id = cursor.lastrowid

        # Insert answers into Answers table
        answer_query = "INSERT INTO Answers (QuestionID, AnswerText, is_correct) VALUES (%s, %s, %s)"
        for index, answer in enumerate(answers):
            is_correct = index in correct_answer_index
            cursor.execute(answer_query, (question_id, answer, is_correct))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'success, quiz created!', 'quiz_id': quiz_id}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        cursor.close()
        conn.close()
    return 

@app.route("/delete-quiz", methods=["GET", "POST"])
def delete_quiz():
    return 

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
