# software-programming-quiz-backend
CS 467 Capstone Project

Instructions to deploy the Flask App after you clone the GitHub Respository:

1. cd into "software-programming-quiz-backend"
2. run "python -m venv venv" to create a virtual environment
3. run "venv/Scripts/activate" to activate the virtual environment (note that this will have to be activated before deploying every time unless it's already active, but we'll most likely have the fronted deploy it automatically by including a script for it under "scripts" in the package.json file of the frontend. Aside from activation, everything else is only done once.)
4. run "pip install flask python-dotenv" (flask is self explanatory, python-dotenv reads key-value pairs from a .env file (.flaskenv in this case) and sets them as environment variables)
5. Now that everything is set up, you should be able to deploy the Flask App by running "flask run"