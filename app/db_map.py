from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, MetaData, Index
from sqlalchemy.orm import declarative_base, relationship

# Define metadata and base class for declarative base
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Define URLs model
class URLs(Base):
    __tablename__ = "URLs"

    url_id = Column(Integer, primary_key=True, autoincrement=True)
    search_term = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)

    # Relationship to ScrapedData
    scraped_data = relationship('ScrapedData', back_populates='url', cascade="all, delete-orphan")

# Define ScrapedData model
class ScrapedData(Base):
    __tablename__ = 'ScrapedData'

    data_id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey('URLs.url_id', ondelete='CASCADE'), nullable=False)
    scraped_text = Column(Text, nullable=False)

    # Relationship to URLs
    url = relationship('URLs', back_populates='scraped_data')

    # Relationship to AlphabetizedData
    alphabetized_data = relationship('AlphabetizedData', back_populates='scraped_data', cascade="all, delete-orphan")

# Define AlphabetizedData model
class AlphabetizedData(Base):
    __tablename__ = 'AlphabetizedData'

    alpha_id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey('URLs.url_id', ondelete='CASCADE'), nullable=False)
    data_id = Column(Integer, ForeignKey('ScrapedData.data_id', ondelete='CASCADE'), nullable=False)
    text_line = Column(Text, nullable=False)
    mfa = Column(Integer, default=0)

    # Index for faster searching on text_line
    __table_args__ = (Index('idx_text_line', 'text_line', mysql_length=255),)

    # Relationships
    scraped_data = relationship('ScrapedData', back_populates='alphabetized_data')

# Define PreviousSearches model
class PreviousSearches(Base):
    __tablename__ = 'PreviousSearches'

    search_id = Column(Integer, primary_key=True, autoincrement=True)
    search_term = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)  # Use DateTime for correct timestamp format

# Wrappers to help organize classes and tables for easy access
class Classes:
    def __init__(self):
        self.URLs = URLs
        self.ScrapedData = ScrapedData
        self.AlphabetizedData = AlphabetizedData
        self.PreviousSearches = PreviousSearches

class Tables:
    def __init__(self):
        self.URLs = URLs.__table__
        self.ScrapedData = ScrapedData.__table__
        self.AlphabetizedData = AlphabetizedData.__table__
        self.PreviousSearches = PreviousSearches.__table__

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
        self.metadata.create_all(engine)  # Ensure all tables are created
