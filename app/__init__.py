from flask import Flask
from app.db import db  # SQLAlchemy instance
from dotenv import load_dotenv
import os

def create_app():
    """Application factory function"""
    # Load environment variables from the .env file
    load_dotenv()

    # Initialize the Flask app
    app = Flask(__name__)

    # Set app configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"{os.getenv('DB_FLAVOR')}://"
        f"{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Register the routes
    from app import routes
    routes.init_app(app)

    return app
