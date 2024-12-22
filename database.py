from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve credentials from environment variables
username = os.getenv("username")
password = os.getenv("password")
database_name = os.getenv("db_name")

# Create the engine
engine = create_engine(
    f"postgresql://{username}:{password}@localhost:5432/{database_name}", echo=True
)

Base = declarative_base()
Session = sessionmaker()
