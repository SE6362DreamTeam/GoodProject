from flask import Flask

from app import *  # This ensures all routes in routes.py are registered
from db_credentials import DB_PASSWORD

# Initialize the Flask app
app = Flask(__name__)

# Set secret key for forms, sessions, CSRF protection, etc.
app.config['user'] = 'The Search'

# Import your routes from the routes.py file


if __name__ == '__main__':
    # Run the application
    app.run(debug=True)
