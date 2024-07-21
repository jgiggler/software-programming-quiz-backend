from database_connector import connect

def login_query(email, password):
  try:
      conn = connect()
      cursor = conn.cursor()

      # Fetch the employer ID where email and password match
      query = "SELECT ID FROM Employer WHERE Email = %s AND Password = %s"
      cursor.execute(query, (email, password))

      result = cursor.fetchone()  # This will be a tuple (ID,) or None if no match is found

      return result

  except mysql.connector.Error as err:
      return {'error': str(err)}

  finally:
      cursor.close()
      conn.close()


def create_account_query(email, password):
    try:
        conn = connect()
        cursor = conn.cursor()
        
        # Prepare and execute SQL query
        query = "INSERT INTO employer (email, password) VALUES (%s, %s)"
        cursor.execute(query, (email, password))
        
        # Commit the transaction
        conn.commit()

        # Get the last inserted ID
        employer_id = int(cursor.lastrowid)
        return {'message': 'success', 'employer_id': employer_id}

    except mysql.connector.Error as err:
        return {'error': str(err)}

    finally:
        cursor.close()
        conn.close()


def create_quiz(data):
  try:
      conn = connect()
      cursor = conn.cursor()

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
      conn.commit()

      return {'message': 'success, quiz created!', 'quiz_id': quiz_id}

  except mysql.connector.Error as err:
      return {'error': str(err)}

  finally:
      cursor.close()
      conn.close()


def delete_quiz(employer_id, quiz_id):
  try:
      conn = connect()
      cursor = conn.cursor()

      delete_query = "DELETE FROM Quiz WHERE EmployerID = %s AND ID = %s"
      cursor.execute(delete_query, (employer_id, quiz_id))
      conn.commit()

      if cursor.rowcount == 0:
          return {'error': 'Quiz not found or you do not have permission to delete it'}

      return {'message': 'success, quiz was deleted'}

  except mysql.connector.Error as err:
      return {'error': str(err)}

  finally:
      cursor.close()
      conn.close()