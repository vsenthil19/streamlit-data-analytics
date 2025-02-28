from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import pandas as pd
from datetime import datetime

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create declarative base
Base = declarative_base()

# Create Session class
Session = sessionmaker(bind=engine)

class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    data = Column(String)  # Store CSV data as string

    @classmethod
    def from_pandas(cls, df, name):
        """Create a Dataset instance from a pandas DataFrame"""
        return cls(
            name=name,
            data=df.to_csv(index=False)
        )

    def to_pandas(self):
        """Convert stored data back to pandas DataFrame"""
        return pd.read_csv(pd.StringIO(self.data))

def init_db():
    """Initialize the database tables"""
    inspector = inspect(engine)
    # Only create tables if they don't exist
    if not inspector.has_table('datasets'):
        Base.metadata.create_all(engine)

def get_session():
    """Get a new database session"""
    return Session()