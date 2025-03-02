from sqlalchemy import create_engine

# Replace the DATABASE_URL with your actual database URL
DATABASE_URL = "postgresql://postgres:Jaysen%40db@localhost:5432/DataAnalyzer"

try:
    # Create an engine
    engine = create_engine(DATABASE_URL)

    # Connect to the database
    with engine.connect() as connection:
        print("Connected to the database successfully.")
except Exception as e:
    print(f"Failed to connect to the database: {e}")
