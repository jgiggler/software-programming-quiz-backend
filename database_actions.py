from database_connector import DatabaseConnection
import mysql.connector

def login_query(email, password):
    try:
        db = DatabaseConnection()
        query = "SELECT ID FROM Employer WHERE Email = %s AND Password = %s"
        data = (email, password)

        cursor = db.execute(query, data)
        result = cursor.fetchone()  # This will be a tuple (ID,) or None if no match is found

        return result

    except mysql.connector.Error as err:
        return {'error': str(err)}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def create_account_query(email, password):
  try:
      db = DatabaseConnection()
      query = "INSERT INTO Employer (Email, Password) VALUES (%s, %s)"
      data = (email, password)

      cursor = db.execute(query, data)

      # Get the last inserted ID
      employer_id = int(cursor.lastrowid)
      return {'message': 'success', 'employer_id': employer_id}

  except mysql.connector.Error as err:
      return {'error': str(err)}


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