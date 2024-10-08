from database_connector import DatabaseConnection
import mysql.connector
import random
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

def login_query(email, password):
    """
    /login
    tested with valid input
    """
    db = None
    cursor = None
    try:
        db = DatabaseConnection()
        query = "SELECT ID FROM Employer WHERE Email = %s AND Password = %s"
        data = (email, password)
        cursor = db.execute(query, data)
        result = cursor.fetchone()
        
        if result is None:
            return None
        
        employer_id = result[0]
        return employer_id
    
    except mysql.connector.Error as err:
        return {'error': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def create_account_query(email, password):
    """
    /create-account
    tested with valid input
    """
    db = None
    cursor = None
    try:
        db = DatabaseConnection()
        query = "INSERT INTO Employer (Email, Password) VALUES (%s, %s)"
        data = (email, password)

        cursor = db.execute(query, data)
        db.commit()
        # Returns the value generated for an AUTO_INCREMENT column by the previous INSERT or UPDATE statement or None when there is no such value: https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-lastrowid.html
        employer_id = int(cursor.lastrowid)
        return {'message': 'success', 'employer_id': employer_id}

    except mysql.connector.Error as err:
        return {'error': str(err)}
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def create_quiz_query(employer_id, quiz_title, quiz_description, timer):
    """
    /create-quiz
    tested with valid input
    """
    db = None
    cursor = None
    
    try:
        db = DatabaseConnection()
        # Insert into Quiz table
        query = "INSERT INTO Quiz (EmployerID, Title, QuizDescription, Timer) VALUES (%s, %s, %s, %s)"
        data = (employer_id, quiz_title, quiz_description, timer,)
        cursor = db.execute(query, data)
        db.commit()
        quiz_id = int(cursor.lastrowid)
        return {'message': 'success, quiz created!', 'quiz_id': quiz_id}
        
    except mysql.connector.Error as err:
        return {'error': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def create_question_query(QuizID, Question, QuestionType):
    """
    /create-quiz
    tested with valid inputs
    """
    db = None
    cursor = None
    try:
        db = DatabaseConnection()
        query = "INSERT INTO Questions (QuizID, Question, QuestionType) VALUES (%s, %s, %s)"
        data = (QuizID, Question, QuestionType)

        cursor = db.execute(query, data)
        db.commit()
        question_id = int(cursor.lastrowid)

        return {'message': 'success', 'question_id': question_id}

    except mysql.connector.Error as err:
            return {'error': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def create_answer_query(QuestionID, Answer, is_correct):
    """
    /create-quiz
    tested with valid input
    """
    db = None
    cursor = None
    try:
        db = DatabaseConnection()
        query = "INSERT INTO Answers (QuestionID, Answer, is_correct) VALUES (%s, %s, %s)"
        data = (QuestionID, Answer, is_correct)

        cursor = db.execute(query, data)
        db.commit()

        if cursor.rowcount is None:
            return {'error': 'Quiz not found or you do not have permission to delete it'}

        return {'message': 'success, quiz was deleted'}

    except mysql.connector.Error as err:
            return {'error': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def delete_quiz_query(employer_id, quiz_id):
    """
    /delete-quiz
    tested with valid input
    """
    db = None
    cursor = None
    try:
        db = DatabaseConnection()
        query = "DELETE FROM Quiz WHERE EmployerID = %s AND ID = %s"
        data = (employer_id, quiz_id)

        cursor = db.execute(query, data)
        db.commit()

        if cursor.rowcount is None:
            return {'error': 'Quiz not found or you do not have permission to delete it'}

        return {'message': 'success, quiz was deleted'}

    except mysql.connector.Error as err:
            return {'error': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def user_quiz_query(employer_id):
    """
    /user-quiz
    tested with valid input (querying multiple quizzes from one employer in quiz table)
    """
    db = None
    cursor = None
    try:
        # Connect to the database
        db = DatabaseConnection()
        
        # Prepare and execute SQL query
        query = """
        SELECT ID, Title, QuizDescription FROM quiz WHERE EmployerID = %s
        """
        data = (employer_id,)
        cursor = db.execute(query, data)

        # Fetch all results
        quizzes = cursor.fetchall()
        quiz_id = []
        title = []
        description = []
        for element in quizzes:
            first, second, third = element
            quiz_id.append(first)
            title.append(second)
            description.append(third)
        
        return {'quiz_id': [quiz_id], 'title': [title], 'description': [description]}

    except mysql.connector.Error as err:
        return {'error': str(err)}, 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def send_quiz_link(quiz_id, candidate_email):
    """
    /send-quiz
    tested with valid input
    """
    db = None
    cursor = None
    try:
        # Connect to the database
        db = DatabaseConnection()
        
        # Prepare and execute SQL query
        unique_link = _generate_random_link()

        query = "INSERT INTO Stats (Quiz_ID, Candidate_Email, Link_ID) VALUES (%s, %s, %s)"
        data = (int(quiz_id), str(candidate_email), str(unique_link))
        cursor = db.execute(query, data)
        db.commit()

        print(unique_link)
        return unique_link

    except mysql.connector.Error as err:
        return {'error': str(err)}, 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def quiz_results_query(employer_id, quiz_id):
    """
    /quiz-results
    Shows the results from the quiz_id
    """
    db = None
    cursor = None
    try:
        db = DatabaseConnection()
        query = "SELECT candidate_email, grade FROM stats WHERE quiz_id = %s ORDER BY grade DESC"
        data = (quiz_id,)

        cursor = db.execute(query, data)
        candidate_results = cursor.fetchall()
        # no candidates in DB currently pulling [] as of now
        candidate_emails = []
        grades=[]
        for email in candidate_results:
            candidate_emails.append(email[0])
        for grade in candidate_results:
            grades.append(grade[1])
        return {'message': 'success', 'candidate_email': candidate_emails, 'grades': grades}

    except mysql.connector.Error as err:
        return {'error': str(err)}, 500
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def submit_quiz_query(quiz_id, candidate_id, quiz_data):
    """
    /submit-quiz
    Handles the quiz answers and UPDATES the grade into Stats table
    """
    db = None
    cursor = None

    try:
        db = DatabaseConnection()
        answers = list(quiz_data.values())
        question_ids = _get_question_ids(db, quiz_id)
        is_correct_array = _find_correct_answers(db, question_ids, answers)

        grade = sum(is_correct_array) / len(is_correct_array)
        query = "UPDATE Stats SET grade = %s WHERE link_id = %s"
        data = (grade, candidate_id,)
        db.execute(query, data)
        db.commit()

        return {'message': "success, quiz completed and submitted by candidate"}, 200

    except mysql.connector.Error as err:
        return {'error': str(err)}, 500
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    
def _get_question_ids(db, quiz_id):
    # Prepare and execute SQL query to get the correct answers for the given question IDs
    #format_strings = ','.join(['%s'] * len(question_ids))
    cursor = db.execute("SELECT ID FROM questions WHERE quizID=%s", (quiz_id,))
    result = cursor.fetchall()
    cleaned_result = [item[0] for item in result]
    return cleaned_result

def _find_correct_answers(db, question_ids, answers):
    query = "SELECT is_correct FROM Answers WHERE QuestionID = %s AND answer= %s"
    results = []
    temp_results = []
    for i in range(len(question_ids)):
        if type(answers[i]) is list:
            for j in range(len(answers[i])):
                cursor = db.execute(query, (question_ids[i], answers[i][j],))
                is_correct = int(cursor.fetchone()[0])
                temp_results.append(is_correct)
            if sum(temp_results) / len(temp_results) == 1:
                results.append(1)
            else:
                results.append(0)
        elif answers[i] == "True" or answers[i] == "False":
            cursor = db.execute(query, (question_ids[i], "true-false",))
            is_correct = cursor.fetchone()[0]
            results.append(1 if is_correct == answers[i] else 0)
        else:
            cursor = db.execute(query, (question_ids[i], "free-form",))
            result_answer = cursor.fetchone()
            if not result_answer:
                cursor = db.execute(query, (question_ids[i], answers[i],))
                is_correct = int(cursor.fetchone()[0])
                results.append(is_correct)
            else:
                is_correct = result_answer[0]
                results.append(1 if is_correct == answers[i] else 0)
        
    return results

def show_quiz_query(quiz_id):
    """
    /show-quiz
    Shows all the questions and answers from a given quiz_id
    """
    try:
        db = DatabaseConnection()
    
        # Get quiz details
        quiz_details = _get_quiz_details(db, quiz_id)
        if not quiz_details:
            return jsonify({'error': 'Quiz not found!'}), 404
    
        # Get quiz questions
        quiz_questions = _get_quiz_questions(db, quiz_id)
        
        # Structure the response data
        questions = []
        for question in quiz_questions:
            question_id = question['question_id']
            question_text = question['question_text']
            question_type = question['question_type']
            
            # Get answers for each question
            answers_data = _get_question_answers(db, question_id)
            answers = [answer['answer_text'] for answer in answers_data]
            
            questions.append({
                'answers': answers,
                'question_text': question_text,
                'question_type': question_type
            })
    
        response_data = {
            'quiz_id': quiz_details['quiz_id'],
            'title': quiz_details['title'],
            'description': quiz_details['description'],
            'timer': quiz_details['timer'],
            'questions': questions
        }
    
        return jsonify(response_data), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        if db:
            db.close()

def _get_quiz_details(db, quiz_id):
    db.execute("SELECT * FROM Quiz WHERE quiz_id = %s", (quiz_id,))
    return db.fetchone()

def _get_quiz_questions(db, quiz_id):
    db.execute("SELECT * FROM Questions WHERE quiz_id = %s", (quiz_id,))
    return db.fetchall()

def _get_question_answers(db, question_id):
    db.execute("SELECT answer_text FROM Answers WHERE question_id = %s", (question_id,))
    return db.fetchall()

def delete_user(employer_id):
    """
    /delete-user
    tested with valid input
    """
    try:
        db = DatabaseConnection()
        query = "DELETE FROM employer WHERE ID = %s"
        data = (employer_id,)

        cursor = db.execute(query, data)

        # Get the last inserted ID
        return {'message': 'success, user deleted'}


    except mysql.connector.Error as err:
        return {'error': str(err)}, 500
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def _generate_random_link():
    """
    Creates a unique 10 digit alphanumeric string
    """
    length = 10
    link_id = ""

    for _ in range(length):
        rand_num = random.choice(
            list(range(48, 58)) +  # 0-9
            list(range(65, 91)) +  # A-Z
            list(range(97, 123))   # a-z
        )
        link_id += chr(rand_num)
        
    return link_id

def delete_user(employer_id):
    db = None
    cursor = None
    try:
        db = DatabaseConnection()
        query = "DELETE FROM Employer WHERE ID = %s"
        data = (employer_id,)
        
        cursor = db.execute(query, data)

        if cursor:
            # Commit the transaction
            db.connection.commit()

            if cursor.rowcount > 0:
                return {'message': 'success, user deleted'}
            else:
                return {'message': 'User not found'}

    except mysql.connector.Error as err:
        return {'error': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def update_user(employer_id, email=None, password=None):
    """
    /update-user

    Update user's email or password based on provided employer_id.
    Fails if the new email already exists or if no update parameters are provided.
    """
    db = None
    cursor = None
    try:
        if email is None and password is None:
            return {'error': 'No update parameters provided'}

        db = DatabaseConnection()

        # Retrieve current email and password
        query = "SELECT Email, Password FROM Employer WHERE ID = %s"
        cursor = db.execute(query, (employer_id,))
        current_email, current_password = cursor.fetchone()

        # Check if the new email is the same as the current email
        if email and email == current_email:
            return {'error': 'The new email must be different from the current email'}

        # Check if the new email is already taken by another user
        if email:
            query = "SELECT ID FROM Employer WHERE Email = %s"
            cursor = db.execute(query, (email,))
            result = cursor.fetchone()
            if result and result[0] != employer_id:
                return {'error': 'Email already exists'}

        # Check if the new password is the same as the current password
        if password and password == current_password:
            return {'error': 'The new password must be different from the current password'}

        # Construct dynamic query
        fields_to_update = []
        data = []

        if email:
            fields_to_update.append("Email = %s")
            data.append(email)

        if password:
            fields_to_update.append("Password = %s")
            data.append(password)

        update_clause = ", ".join(fields_to_update)
        query = f"UPDATE Employer SET {update_clause} WHERE ID = %s"
        data.append(employer_id)

        cursor = db.execute(query, data)
        db.commit()

        if email and password:
            return {'message': 'Success, email and password updated'}
        
        elif email:
            return {'message': 'Success, email updated'}
        
        elif password:
            return {'message': 'Success, password updated'}

    except mysql.connector.Error as err:
        return {'message': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def get_quiz_id_by_link(link_id):
  db = None
  cursor = None
  try:
      db = DatabaseConnection()
      query = "SELECT Quiz_ID FROM Stats WHERE Link_ID = %s"
      cursor = db.execute(query, (link_id,))
      result = cursor.fetchone()
      if result:
          return result[0]
      else:
          return None
  except mysql.connector.Error as err:
      return {'error': str(err)}
  finally:
      if cursor:
          cursor.close()
      if db:
          db.close()

def get_quiz_details_by_id(quiz_id):
    db = None
    cursor = None
    try:
        db = DatabaseConnection()
        # Get quiz details
        quiz_details = _get_quiz_details(db, quiz_id)
        if not quiz_details:
            return {'message': 'Quiz not found!'}, 404

        # Get quiz questions
        quiz_questions = _get_quiz_questions(db, quiz_id)
        # Structure the response data
        questions = []
        for question in quiz_questions:
            question_id = question[0]
            question_text = question[2]
            question_type = question[3]

            # Get answers for each question
            answers_data = _get_question_answers(db, question_id)
            answers = []
            for answer in answers_data:
                answers.append(answer[0])

            question_dict = {
                'question_text': question_text,
                'question_type': question_type,
                'answers': answers
            }

            questions.append(question_dict)
        
        response_data = {
            'employer_id': quiz_details[1],
            'quiz_id': quiz_details[0],
            'title': quiz_details[2],
            'description': quiz_details[3],
            'timer': quiz_details[4],
            'questions': questions
        }
        return response_data

    except mysql.connector.Error as err:
        return {'message': str(err)}, 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def _get_quiz_details(db, quiz_id):
    cursor = db.execute("SELECT * FROM Quiz WHERE ID = %s", (quiz_id,))
    return cursor.fetchone()

def _get_quiz_questions(db, quiz_id):
    cursor = db.execute("SELECT * FROM Questions WHERE QuizID = %s", (quiz_id,))
    return cursor.fetchall()

def _get_question_answers(db, question_id):
    cursor = db.execute("SELECT Answer FROM Answers WHERE QuestionID = %s", (question_id,))
    return cursor.fetchall()

def get_emails(candidate_id, quiz_id):
    db = None
    cursor = None
    try:
        db = DatabaseConnection()

        # Retrieve candidate_email from Stats table based on candidate_id
        query = "SELECT Candidate_Email FROM Stats WHERE Link_ID = %s"
        cursor = db.execute(query, (candidate_id,))
        result = cursor.fetchone()
        if not result:
            return {'error': 'No candidate found with the provided candidate_id'}
        
        candidate_email = result[0]

        # Retrieve employer_email from Quiz table based on quiz_id
        query = "SELECT Employer.Email FROM Employer JOIN Quiz ON Employer.ID = Quiz.EmployerID WHERE Quiz.ID = %s"
        cursor = db.execute(query, (quiz_id,))
        
        result = cursor.fetchone()
        if not result:
            return {'error': 'No employer found with the provided quiz_id'}
        
        employer_email = result[0]

        return employer_email, candidate_email

    except mysql.connector.Error as err:
        return {'error': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

