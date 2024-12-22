from database import engine, Base
from models import User, WorkoutRoutine

# Debug: Check registered tables
print("Registered tables:", Base.metadata.tables.keys())

# Create tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
