from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access the DATABASE_URL environment variable
database_url = os.getenv('DATABASE_URL')
print(f'DATABASE_URL: {database_url}')
