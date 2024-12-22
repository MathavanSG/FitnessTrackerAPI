from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# User table definition
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(Text, nullable=True)
    workout_routines = relationship("WorkoutRoutine", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"


# WorkoutRoutine table definition
class WorkoutRoutine(Base):
    __tablename__ = "workout_routine"
    routine_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), index=True
    )  # Foreign key to User table
    date = Column(Date, nullable=True)
    routine_details = Column(Text, nullable=True)
    user = relationship(
        "User", back_populates="workout_routines"
    )  # Back reference to User table

    def __repr__(self):
        return f"WorkoutRoutine(routine_id={self.routine_id}, user_id={self.user_id}, date={self.date})"
