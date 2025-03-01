from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
import pandas as pd
from datetime import datetime
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

def create_db_engine(retries=3, delay=2):
    """Create database engine with retry logic"""
    for attempt in range(retries):
        try:
            # Disable connection pooling and set SSL mode to require
            engine = create_engine(
                DATABASE_URL,
                poolclass=NullPool,
                connect_args={
                    "sslmode": "require",
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