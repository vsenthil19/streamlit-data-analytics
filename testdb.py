from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access the DATABASE_URL environment variable
database_url = os.getenv('DATABASE_URL')

# Create an engine using the DATABASE_URL
engine = create_engine(database_url)

# Test the connection
with engine.connect() as connection:
    # Execute a simple SQL query to test the connection
    result = connection.execute("SELECT 'Connection Successful!'")
    
    # Print the result of the query
    for row in result:
        print(row)
