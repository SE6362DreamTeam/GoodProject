import threading

from flask import Flask

from app.background_tasks import check_urls_periodically
from app.db import db, init_db  # SQLAlchemy instance
from dotenv import load_dotenv
import os
from app.db_map import Base, Map  # Assuming Base is your declarative base class

def create_app():
    # Load environment variables from .env file
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
    init_db(app)

    # Create database tables if they don't exist
    with app.app_context():
        Base.metadata.create_all(db.engine)

    # Register the routes
    from app import routes
    routes.init_app(app)

    # Start background tasks
    threading.Thread(target=check_urls_periodically, args=(app,), daemon=True).start()

    return app
