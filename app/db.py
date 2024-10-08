import csv
import os

from sqlalchemy import MetaData

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL, PrimaryKeyConstraint
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import SQLAlchemy
from app.db_map import Map, Base
import logging
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()
map = Map()


def init_db(app):
    try:
        # Initialize the SQLAlchemy object with the app
        db.init_app(app)

        logging.info("Database connected successfully.")
        return db

    except Exception as e:
        logging.error("Failed to connect to the database.", exc_info=True)
        raise e


def get_engine():
    # Get the engine from db
    engine = db.engine

    # Create a session factory using the engine
    Session = sessionmaker(bind=engine)

    # Return a new session object
    return Session()