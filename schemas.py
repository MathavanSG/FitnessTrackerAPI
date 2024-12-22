from pydantic import BaseModel
from typing import Optional
from datetime import date


class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    hashed_password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "Maddy",
                "email": "Maddy@example.com",
                "hashed_password": "example_hashed_password",
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "5c0e9980bed3b64ce7735db110951df414e399e3bc7993c071ae5148cd6e783c"
    )


class LoginModel(BaseModel):
    username: str
    hashed_password: str


class WorkoutRoutineModel(BaseModel):
    routine_id: Optional[int] = None
    user_id: Optional[int] = None  # Optional because it's set automatically
    date: date
    routine_details: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "routine_id": 1,
                "user_id": 123,
                "date": "2024-12-01",
                "routine_details": "Morning yoga and cardio workout",
            }
        }


class UpdateWorkoutRoutineDetails(BaseModel):
    routine_details: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "routine_details": "Morning yoga and cardio workout",
            }
        }
