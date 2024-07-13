from flask import Flask


# Configuration

app = Flask(__name__)


# Routes 
# Mostly just placeholders based on the specs until the database communication is implemented

@app.route("/login", methods=["GET", "POST"])
def login():
    return 

@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    return 

@app.route("/create-quiz", methods=["GET", "POST"])
def create_quiz():
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
