from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from models import User, WorkoutRoutine
from schemas import WorkoutRoutineModel, UpdateWorkoutRoutineDetails
from database import Session, engine
from fastapi.encoders import jsonable_encoder
from datetime import datetime

workout_routine_router = APIRouter()

session = Session(bind=engine)


@workout_routine_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    """
    ### A sample implementation of the authorization and page redirect

    Returns:
        A JSON message greeting the Bodybuilder and asking about achievements.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    return {"message": "Hello, Bodybuilder!, What was your acheivement ;-)"}


@workout_routine_router.post("/createworkout", status_code=status.HTTP_201_CREATED)
async def create_workout_routine(
    workout_routine: WorkoutRoutineModel, Authorize: AuthJWT = Depends()
):
    """
    ### Create Workout Routines

    Creates a new workout routine for the authenticated user.

    Args:
        workout_routine (WorkoutRoutineModel): The workout routine data.
            Examples:
                {
                "routine_id": 1,
                "user_id": 123,
                "date": "2024-12-01",
                "routine_details": "Morning yoga and cardio workout",
            }

    Returns:
        JSON object containing the newly created workout routine details.
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter_by(username=current_user).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    new_workout_routine = WorkoutRoutine(
        date=workout_routine.date,
        routine_details=workout_routine.routine_details,
        user_id=user.id,
    )

    session.add(new_workout_routine)
    session.commit()

    response = {
        "Date": new_workout_routine.date,
        "Routine": new_workout_routine.routine_details,
        "Routine_id": new_workout_routine.routine_id,
        "User_id": new_workout_routine.user_id,
    }

    return jsonable_encoder(response)


@workout_routine_router.get("/showallworkouts", status_code=status.HTTP_201_CREATED)
async def show_all_workouts(Authorize: AuthJWT = Depends()):
    """
    ### Show All Workouts

    Retrieves all workout routines for the current authenticated user.

    Returns:
        A JSON-encoded list of workout routines for the authenticated user.
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter_by(username=current_user).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    workout_routines = session.query(WorkoutRoutine).filter_by(user_id=user.id).all()

    return jsonable_encoder(workout_routines)


@workout_routine_router.get(
    "/showallworkouts/{routine_id}", status_code=status.HTTP_201_CREATED
)
async def show_all_workouts(routine_id: int, Authorize: AuthJWT = Depends()):
    """
    ### Show Workouts by Routine ID

    Retrieves a specific workout routine by its routine ID for the authenticated user.

    Args:
        routine_id (int): The ID of the workout routine to retrieve.

    Returns:
        A JSON-encoded dictionary of the requested workout routine.

    Raises:
        HTTPException: 401 if token is invalid or missing,
                       404 if user or routine not found.
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter_by(username=current_user).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    workout_routine = (
        session.query(WorkoutRoutine)
        .filter(WorkoutRoutine.routine_id == routine_id)
        .first()
    )

    if workout_routine:
        return jsonable_encoder(workout_routine)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Workout routine not found"
    )


@workout_routine_router.put(
    "/updateworkouts/{routine_id}", status_code=status.HTTP_200_OK
)
async def update_workout_routine(
    routine_id: int,
    workout_routine: WorkoutRoutineModel,
    Authorize: AuthJWT = Depends(),
):
    """
    ### Update Workout Routine

    Updates a specific workout routine by its routine ID with the provided new data.

    Args:
        routine_id (int): The ID of the workout routine to update.
        workout_routine (WorkoutRoutineModel): The new workout routine details.
            Example:
                {
                "routine_id": 1,
                "user_id": 123,
                "date": "2024-12-01",
                "routine_details": "Morning yoga and cardio workout",
            }


    Returns:
        A JSON-encoded dictionary of the updated workout routine.

    Raises:
        HTTPException: 401 if token is invalid or missing.
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )

    workout_routine_to_update = (
        session.query(WorkoutRoutine)
        .filter(WorkoutRoutine.routine_id == routine_id)
        .first()
    )

    if workout_routine_to_update:
        workout_routine_to_update.date = workout_routine.date
        workout_routine_to_update.routine_details = workout_routine.routine_details
        session.commit()
    return jsonable_encoder(workout_routine_to_update)


@workout_routine_router.get("/filterworkoutsbydate", status_code=status.HTTP_200_OK)
async def filter_workouts_by_date(date: str, Authorize: AuthJWT = Depends()):
    """
    ### Filter Workouts by Date

    Filter workout routines by date for the current authenticated user.

    Args:
        date (str): Date in YYYY-MM-DD format (query parameter).

    Returns:
        A list of workout routines for the specified date.

    Raises:
        HTTPException: 400 if the date is invalid format,
                       401 if token is invalid or missing,
                       404 if no routines are found on that date or user not found.
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )

    try:
        filter_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD.",
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter_by(username=current_user).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    workout_routines = (
        session.query(WorkoutRoutine)
        .filter(WorkoutRoutine.user_id == user.id, WorkoutRoutine.date == filter_date)
        .all()
    )

    if not workout_routines:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No workout routines found for date {filter_date}.",
        )

    return jsonable_encoder(workout_routines)


@workout_routine_router.patch(
    "/update_workout_details/{routine_id}", status_code=status.HTTP_200_OK
)
async def update_workout_details(
    routine_id: int,
    update_details: UpdateWorkoutRoutineDetails,
    Authorize: AuthJWT = Depends(),
):
    """
    ### Partially Update Workout Details

    Partially updates the routine details for a given workout routine (by its ID).

    Args:
        routine_id (int): The ID of the workout routine to update.
        update_details (UpdateWorkoutRoutineDetails): Partial data to update the routine.
            Example:
                {
                "routine_id": 1,
                "user_id": 123,
                "date": "2024-12-01",
                "routine_details": "Morning yoga and cardio workout",
            }


    Returns:
        A JSON-encoded dictionary of the updated workout routine fields.

    Raises:
        HTTPException: 401 if token is invalid or missing,
                       403 if the user is not authorized to update the routine,
                       404 if the workout routine is not found.
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )

    username = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == username).first()

    workout_routine_to_be_updated = (
        session.query(WorkoutRoutine)
        .filter(WorkoutRoutine.routine_id == routine_id)
        .first()
    )

    if not workout_routine_to_be_updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workout routine not found"
        )
    if workout_routine_to_be_updated.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to update this routine",
        )
    workout_routine_to_be_updated.routine_details = update_details.routine_details
    session.commit()
    response_dict = {
        "routine_id": workout_routine_to_be_updated.routine_id,
        "user_id": workout_routine_to_be_updated.user_id,
        "date": workout_routine_to_be_updated.date,
        "routine_details": workout_routine_to_be_updated.routine_details,
    }
    return jsonable_encoder(response_dict)


@workout_routine_router.delete(
    "/delete_routine/{routine_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_workout_routine(routine_id: int, Authorize: AuthJWT = Depends()):
    """
    ### Delete Workout Routine

    Deletes the specified workout routine by its routine ID for the authenticated user.

    Args:
        routine_id (int): The ID of the workout routine to delete.


    Returns:
        A success message confirming deletion of the specified workout routine.

    Raises:
        HTTPException: 401 if token is invalid or missing.
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )

    username = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == username).first()

    workout_routine_to_be_deleted = (
        session.query(WorkoutRoutine)
        .filter(WorkoutRoutine.routine_id == routine_id)
        .first()
    )
    session.delete(workout_routine_to_be_deleted)
    session.commit()
    return {"message": "Workout routine deleted successfully"}
