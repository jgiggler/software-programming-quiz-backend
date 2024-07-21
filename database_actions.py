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