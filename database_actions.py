from database_connector import DatabaseConnection
import mysql.connector
from random import randint

def login_query(email, password):
    cursor = None
    db = None
    try:
        db = DatabaseConnection()
        query = "SELECT ID FROM Employer WHERE Email = %s AND Password = %s"
        data = (email, password)

        cursor = db.execute(query, data)
        if cursor:
            result = cursor.fetchone()  # This will be a tuple (ID,) or None if no match is found
            return result

    except mysql.connector.Error as err:
        return {'error': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    return None


def create_account_query(email, password):
    db = None
    cursor = None
    try:
        db = DatabaseConnection()
        query = "INSERT INTO Employer (Email, Password) VALUES (%s, %s)"
        data = (email, password)
        
        cursor = db.execute(query, data)

        if cursor:
            # Commit the transaction
            db.connection.commit()

            # Get the last inserted ID
            employer_id = int(cursor.lastrowid)
            return {'message': 'success', 'employer_id': employer_id}
        else:
            return {'message': 'Username already in use'}

    except mysql.connector.Error as err:
        return {'error': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    

def create_quiz(data):
  try:
      db = DatabaseConnection()

      cursor = db.connection.cursor()

      employer_id = data.get('employer_id')
      quiz_title = data.get("title")
      quiz_description = data.get("description")

      # Insert into Quiz table
      quiz_query = "INSERT INTO Quiz (EmployerID, Title, QuizDescription) VALUES (%s, %s, %s)"
      cursor.execute(quiz_query, (employer_id, quiz_title, quiz_description))
      quiz_id = cursor.lastrowid

      questions = data.get('questions')
      for question in questions:
          question_title = question.get('question_text')
          question_type = question.get('question_type')
          answers = question.get('answers')
          correct_answer_index = question.get('is_correct')

          # Insert question into Questions table
          question_query = "INSERT INTO Questions (QuizID, Question, QuestionType) VALUES (%s, %s, %s)"
          cursor.execute(question_query, (quiz_id, question_title, question_type))
          question_id = cursor.lastrowid

          # Insert answers into Answers table
          answer_query = "INSERT INTO Answers (QuestionID, Answer, is_correct) VALUES (%s, %s, %s)"
          for index, answer in enumerate(answers):
              is_correct = index in correct_answer_index
              cursor.execute(answer_query, (question_id, answer, is_correct))

      # Commit the transaction
      db.connection.commit()

      return {'message': 'success, quiz created!', 'quiz_id': quiz_id}

  except mysql.connector.Error as err:
      return {'error': str(err)}

  finally:
      if cursor:
          cursor.close()
      if db:
          db.close()


def delete_quiz(employer_id, quiz_id):
  try:
      db = DatabaseConnection()
      query = "DELETE FROM Quiz WHERE EmployerID = %s AND ID = %s"
      data = (employer_id, quiz_id)

      cursor = db.execute(query, data)
      db.connection.commit()

      if cursor.rowcount == 0:
          return {'error': 'Quiz not found or you do not have permission to delete it'}

      return {'message': 'success, quiz was deleted'}

  except mysql.connector.Error as err:
        return {'error': str(err)}

  finally:
      if cursor:
          cursor.close()
      if db:
          db.close()

def user_quiz(employer_id):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Prepare and execute SQL query
        query = """
        SELECT Quiz.quiz_id AS quiz_id, Quiz.title, Quiz.description
        FROM Quiz
        JOIN Employer ON Quiz.EmployerID = Employer.employer_id
        WHERE employer.employer_id = %s
        """
        cursor.execute(query, (employer_id,))
        
        # Fetch all results
        quizzes = cursor.fetchall()
        
        return {'quizzes': quizzes}, 200

    except mysql.connector.Error as err:
        return {'error': str(err)}, 500

    finally:
        cursor.close()
        conn.close()

def send_quiz_link(employer_id, quiz_id, candidate_email):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Prepare and execute SQL query
        unique_link = _generate_random_link()
        return_link = "software-quiz.com/" + unique_link

        quiz_query = "INSERT INTO Stats (candidate_email, link_id, quiz_id) VALUES (%s, %s, %s)"
        cursor.execute(quiz_query, (candidate_email, unique_link, quiz_id))
        
        return {'message': "success, here is the link to the quiz",
                "link": return_link}, 200

    except mysql.connector.Error as err:
        return {'error': str(err)}, 500

    finally:
        cursor.close()
        conn.close()

def _generate_random_link():
    # Creates a unique 10 digit alphanumeric string
    length = 10
    link_id = ""

    for i in range(length):
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