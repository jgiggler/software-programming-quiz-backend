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
    data = request.json

    employer_id = data.get('employer_id')
    quiz_title = data.get("title")
    for quizID in range(10):
        if data.get(str(quizID)) is None:
            return
        quiz_description = data.get("description")
        quiz_id = data.get(str(quizID))
        question_title = data.get('question_text')
        question_type = data.get('question_type')
        answers = data.get('answers')
        correct_answer_index = data.get('is_correct')

        # Validate input
        if not quiz_id or not question_title or not question_type or not answers or correct_answer_index or quiz_title or quiz_description is None:
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            # Connect to the database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert into Quiz table
            quiz_query = "INSERT INTO Questions (QuizID, EmployerID, title, description) VALUES (%s, %s, %s, %s)"
            cursor.execute(quiz_query, (quiz_id, employer_id, quiz_title, quiz_description))

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

# Listener
if __name__ == "__main__":

    app.run(port=4546, debug=True)