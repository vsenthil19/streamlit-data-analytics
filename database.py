from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create SQLAlchemy engine
try:
    engine = create_engine(DATABASE_URL)
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Error creating database engine: {str(e)}")
    raise

# Create declarative base
Base = declarative_base()

# Create Session class
Session = sessionmaker(bind=engine)

class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    data = Column(String, nullable=False)  # Store CSV data as string

    @classmethod
    def from_pandas(cls, df, name):
        """Create a Dataset instance from a pandas DataFrame"""
        try:
            return cls(
                name=name,
                data=df.to_csv(index=False)
            )
        except Exception as e:
            logger.error(f"Error creating Dataset from DataFrame: {str(e)}")
            raise

    def to_pandas(self):
        """Convert stored data back to pandas DataFrame"""
        try:
            return pd.read_csv(pd.StringIO(self.data))
        except Exception as e:
            logger.error(f"Error converting data to DataFrame: {str(e)}")
            raise

def init_db():
    """Initialize the database tables"""
    try:
        inspector = inspect(engine)
        if not inspector.has_table('datasets'):
            logger.info("Creating datasets table")
            Base.metadata.create_all(engine)
            logger.info("Datasets table created successfully")
        else:
            logger.info("Datasets table already exists")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def get_session():
    """Get a new database session"""
    return Session()