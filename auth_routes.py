from fastapi import APIRouter, status, HTTPException, Depends
from database import Session, engine
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

# Create the API router for authentication routes
auth_router = APIRouter()

session = Session(bind=engine)


@auth_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    """
    ### Hello Endpoint

    Verifies the JWT token and greets the user.

    Args:
        Authorize (AuthJWT): Dependency for JWT-based authorization.

    Returns:
        A JSON message greeting the user.

    Raises:
        HTTPException: 401 if the token is invalid or missing.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return {"message": "Hello, Bodybuilder!"}


@auth_router.post("/signup", status_code=status.HTTP_200_OK)
async def signup(user: SignUpModel):
    """
    ### Signup Endpoint

    Registers a new user by saving their details in the database.

    Args:
        user (SignUpModel): A Pydantic model containing `username`, `email`, and `hashed_password`.
            Example:
                {
                "username": "Maddy",
                "email": "Maddy@example.com",
                "hashed_password": "example_hashed_password",
            }

    Returns:
        A JSON object representing the newly created user.

    Raises:
        HTTPException: 400 if the email or username already exists.
    """
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists",
        )

    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the username already exists",
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=generate_password_hash(user.hashed_password),
    )

    session.add(new_user)
    session.commit()

    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    """
    ### Login Endpoint

    Authenticates the user by verifying the username and password, and returns access and refresh tokens.

    Args:
        user (LoginModel): A Pydantic model containing `username` and `hashed_password`.
            Example:
                {
                "username": "Maddy",
                "hashed_password": "example_hashed_password",
            }
        Authorize (AuthJWT): Dependency for JWT-based token creation.

    Returns:
        A JSON object containing `access` and `refresh` tokens.

    Raises:
        HTTPException: 400 if the username or password is invalid.
    """
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.hashed_password, user.hashed_password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response = {"access": access_token, "refresh": refresh_token}

        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password"
    )


@auth_router.get("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    """
    ### Refresh Token Endpoint

    Generates a new access token using a valid refresh token.

    Args:
        Authorize (AuthJWT): Dependency for JWT-based token operations.

    Returns:
        A JSON object containing the new access token.

    Raises:
        HTTPException: 401 if the refresh token is invalid or missing.
    """
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide a valid refresh token",
        )

    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=Authorize.get_jwt_subject())

    return jsonable_encoder({"access": access_token})
