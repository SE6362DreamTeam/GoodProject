import csv
import os

from sqlalchemy import MetaData

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL, PrimaryKeyConstraint
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import SQLAlchemy
from app.db_map import Map, Base
import logging

db = SQLAlchemy()
map = Map()


def init_db(app):

    try:
        # Build the database URI using the environment variables
        FLASK_SQLALCHEMY_DATABASE_URI = (
            f"{os.getenv('DB_FLAVOR')}://"
            f"{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )

        # Configure the Flask app for SQLAlchemy
        app.config['SQLALCHEMY_DATABASE_URI'] = FLASK_SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Or False, to avoid warnings
        app.config['SQLALCHEMY_ECHO'] = True  # Log all SQL statements

        # Initialize the SQLAlchemy object with the app
        db.init_app(app)

        logging.info("Database connected successfully.")
        return db

    except Exception as e:
        logging.error("Failed to connect to the database.", exc_info=True)
        raise e