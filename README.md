# Software Programming Quiz Backend

This is part of a Summer 2024 Oregon State University CS 467 Capstone Project. Here is a link to the [frontend](https://github.com/jgiggler/software-programming-quiz-frontend) part of the project.

## Deployment Instructions

1. Git clone this repository and verify that the active working directory is "software-programming-quiz-backend" in your terminal. If it is not, cd into it.

2. (Optional but recommended for package management) Create a virtual environment with `python -m venv venv`.

3. On Windows, activate the virtual environment with `venv/Scripts/activate`. Remember to do this every time you close and reopen the program otherwise you'll run into the issue of missing/uninstalled packages. 

4. Run `pip install flask python-dotenv mysql-connector-python flask_cors` to install required packages. Flask is a Python web application framework, Python Dotenv reads key-value pairs from a .env file (.env in this case) and sets them as environment variables, MySQL Connector/Python is a driver for communicating with MySQL servers, and Flask-CORS is a Flask extension for handling Cross Origin Resource Sharing (CORS). 

5. Create a database in MySqlDB. Once you have made an account and created your database, you will need to run the code in database_setup.sql to set up your relational database. (If you are our grader, then you will have access to our database when we share our .env file with you. Simply replace the example.env with the .env that we give you and you can skip to step 7).

6. Rename the example.env file to simply ".env" and fill in all of the blanks with your own information. 
    - 'user' is your MySqlDB username
    - 'password' is your MySqlDB password
    - 'host' is the url where the database is hosted on MySqlDB
    - 'smtp_server' is the email service that you will be using for the emailing functionality. (Our implementation uses a dedicated gmail account for it. You can use any email service just make sure you enable SMTP permissions on your account)
    - 'smtp_port' (587 by default, but can be changed if need be)
    - 'smtp_user' is the email username that you will be using. 
    - 'smtp_password' is the password generated when you enable SMTP permission.

7. Deploy the Flask App with `python app.py`. By default, it will run on port 4546, but you can change that at the bottom of app.py.

8. Deploy the frontend (link at the top) and you should be set!
