from database_connector import DatabaseConnection
import mysql.connector
import random
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

def create_quiz_query(employer_id, quiz_title, quiz_description):
    """
    /create-quiz
    tested with valid input
    """
    db = None
    cursor = None
    try:
        db = DatabaseConnection()
        # Insert into Quiz table
        query = "INSERT INTO Quiz (EmployerID, Title, QuizDescription) VALUES (%s, %s, %s)"
        data = (employer_id, quiz_title, quiz_description)
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
    TODO
    question_query = "INSERT INTO Questions (QuizID, Question, QuestionType) VALUES (%s, %s, %s)"
    cursor.execute(question_query, (quiz_id, question_title, question_type))
    question_id = cursor.lastrowid
    """
    return

def create_answer_query(QuestionID, Answer, is_correct):
    """
    /create-quiz
    answer_query = "INSERT INTO Answers (QuestionID, Answer, is_correct) VALUES (%s, %s, %s)"
    for index, answer in enumerate(answers):
        is_correct = index in correct_answer_index
        cursor.execute(answer_query, (question_id, answer, is_correct))
    TODO
    """
    return

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
        SELECT * FROM quiz WHERE EmployerID = %s
        """
        data = (employer_id,)
        cursor = db.execute(query, data)

        # Fetch all results
        quizzes = cursor.fetchall()
        return {'quizzes': quizzes}, 200

    except mysql.connector.Error as err:
        return {'error': str(err)}, 500

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def send_quiz_link(candidate_email, quiz_id, grade):
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
        return_link = "software-quiz.com/" + unique_link

        query = "INSERT INTO Stats (candidate_email, Link_ID, Quiz_ID, grade) VALUES (%s, %s, %s, %s)"
        data = (candidate_email, return_link, quiz_id, grade)
        db.execute(query, data)
        db.commit()

        return {'message': "success, here is the link to the quiz",
                "link": return_link}, 200

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
        query = "SELECT candidate_email, grade FROM stats WHERE quiz_id = %s"
        data = (quiz_id,)

        cursor = db.execute(query, data)


        return {'message': 'success'}

    except mysql.connector.Error as err:
        return {'error': str(err)}, 500
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

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