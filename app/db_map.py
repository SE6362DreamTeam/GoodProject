from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

# Define the metadata
metadata = MetaData()

# Define Declarative Base class
Base = declarative_base(metadata=metadata)

# Define URLs model using Declarative ORM
class URLs(Base):
    __tablename__ = "URLs"  # Explicitly set the table name

    # Define the columns
    url_id = Column(Integer, primary_key=True, autoincrement=True)
    search_term = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)

    # Define a relationship to the ScrapedData table
    scraped_data = relationship('ScrapedData', back_populates='url', cascade="all, delete-orphan")

class ScrapedData(Base):
    __tablename__ = 'ScrapedData'  # Explicitly set the table name

    # Define columns
    data_id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey('URLs.url_id', ondelete='CASCADE'), nullable=False)
    scraped_text = Column(Text, nullable=False)

    # Define a relationship to the URLs table
    url = relationship('URLs', back_populates='scraped_data')

# Define wrapper classes for accessing models and tables
class Classes:
    def __init__(self):
        self.Urls = URLs
        self.ScrapedData = ScrapedData

class Tables:
    def __init__(self):
        self.URLs = URLs.__table__
        self.ScrapedData = ScrapedData.__table__


class Map:
    def __init__(self):
        self.metadata = metadata
        self.classes = Classes()
        self.tables = Tables()
        self.base = Base
        self.engine = None

    # Connect to an engine and bind it to the metadata
    def connect(self, engine):
        self.engine = engine
        self.metadata.bind = engine
        self.metadata.create_all(engine)  # Ensure tables are created
