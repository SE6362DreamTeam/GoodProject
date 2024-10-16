from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, Text, Index
from sqlalchemy.orm import declarative_base, relationship

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

# Define ScrapedData model using Declarative ORM
class ScrapedData(Base):
    __tablename__ = 'ScrapedData'  # Explicitly set the table name

    # Define columns
    data_id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey('URLs.url_id', ondelete='CASCADE'), nullable=False)
    scraped_text = Column(Text, nullable=False)

    # Define a relationship to the URLs table
    url = relationship('URLs', back_populates='scraped_data')

    # Define a relationship to the AlphabetizedData table
    alphabetized_data = relationship('AlphabetizedData', back_populates='scraped_data', cascade="all, delete-orphan")

# Define AlphabetizedData model
class AlphabetizedData(Base):
    __tablename__ = 'AlphabetizedData'  # Explicitly set the table name

    # Define columns
    alpha_id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey('URLs.url_id', ondelete='CASCADE'), nullable=False)
    data_id = Column(Integer, ForeignKey('ScrapedData.data_id', ondelete='CASCADE'), nullable=False)
    text_line = Column(Text, nullable=False)
    mfa = Column(Integer, default=0)

    # Define index for the text_line column
    __table_args__ = (Index('idx_text_line', 'text_line', mysql_length=255),)

    # Define relationships
    scraped_data = relationship('ScrapedData', back_populates='alphabetized_data')

# Update Classes wrapper to include AlphabetizedData
class Classes:
    def __init__(self):
        self.Urls = URLs
        self.ScrapedData = ScrapedData
        self.AlphabetizedData = AlphabetizedData

# Update Tables wrapper to include AlphabetizedData
class Tables:
    def __init__(self):
        self.URLs = URLs.__table__
        self.ScrapedData = ScrapedData.__table__
        self.AlphabetizedData = AlphabetizedData.__table__

# Update Map to handle AlphabetizedData table creation
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
