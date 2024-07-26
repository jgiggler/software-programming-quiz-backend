# Software Programming Quiz Backend

This is part of a Summer 2024 Oregon State University CS 467 Capstone Project. Here is a link to the [frontend](https://github.com/jgiggler/software-programming-quiz-frontend) part of the project. For further information on Flask, refer to the following [source](https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project) to get a starter Flask backend to work with a React frontend.

## Deployment Instructions

1. Verify that the active working directory is "software-programming-quiz-backend". If it is not, cd into it.
2. Create a virtual environment with `python -m venv venv`.
3. Activate the virtual environment with `venv/Scripts/activate`. The virtual environment must be actived during each deployment. This will be handled automatically by a script under "scripts" in the package.json file of the frontend.
4. Run `pip install flask python-dotenv mysql-connector-python flask_cors` to install required packages. Flask is a Python web application framework, Python Dotenv reads key-value pairs from a .env file (.env in this case) and sets them as environment variables, MySQL Connector/Python is a driver for communicating with MySQL servers, and Flask-CORS is a Flask extension for handeling Cross Origin Resource Sharing (CORS). 
5. Create a global environment variable with the MySQL server password `export password=replace_with_password`. This is retrieved in database_connector.py with `os.environ.get('password')`.
6. Deploy the Flask App with `flask run`.
