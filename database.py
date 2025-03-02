from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import logging
import time
from io import StringIO
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to load environment variables from .env file, but don't fail if it doesn't exist
logger.info("Current working directory: %s", os.getcwd())
try:
    load_dotenv()
    logger.info("Loaded environment variables from .env file")
except Exception as e:
    logger.info("No .env file found, using system environment variables")

# Get database URL from environment
logger.info("Attempting to load DATABASE_URL from environment...")
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set")
    logger.info("Available environment variables: %s", list(os.environ.keys()))
    raise ValueError("DATABASE_URL environment variable is not set")
else:
    # Log a sanitized version of the URL (hide password)
    sanitized_url = DATABASE_URL.replace('//', '//***:***@')
    logger.info("Database URL found: %s", sanitized_url)

def create_db_engine(retries=3, delay=2):
    """Create database engine with retry logic"""
    for attempt in range(retries):
        try:
            logger.info(f"Attempt {attempt + 1} to create database engine")
            engine = create_engine(
                DATABASE_URL,
                poolclass=NullPool,
                connect_args={
                    "connect_timeout": 30
                }
            )
            # Test the connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
            logger.info("Database engine created successfully")
            return engine
        except Exception as e:
            if attempt == retries - 1:
                logger.error(f"Failed to create database engine after {retries} attempts: {str(e)}")
                raise
            logger.warning(f"Database connection attempt {attempt + 1} failed: {str(e)}")
            time.sleep(delay)

# Create engine with retry logic
engine = create_db_engine()

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
            return pd.read_csv(StringIO(self.data))
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