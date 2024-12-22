# My Fitness Tracker API

## Overview
**My Fitness Tracker API** is a RESTful API designed to help users track their fitness routines and workout progress. The API is built with **FastAPI** and provides a variety of endpoints to manage user authentication and workout routines.

### Features:
- User authentication with JWT tokens.
- CRUD operations for workout routines.
- Secure endpoints with built-in Swagger UI for easy testing.
- JWT `Authorize` button in Swagger UI for seamless integration without relying on external tools.

### OpenAPI Specifications:
- **Version**: 1.0
- **Specification**: OAS 3.1
- **OpenAPI JSON**: `/openapi.json`

### Base URL:
- The API is hosted locally or on a server, with all endpoints relative to the base URL.

---

## Endpoints

### **Authentication (auth)**

#### **GET** `/auth/`
Returns a welcome message after successful authentication.

#### **POST** `/auth/signup`
Allows new users to register by providing a username, email, and password.

#### **POST** `/auth/login`
Authenticates the user and returns JWT access and refresh tokens.

#### **GET** `/auth/refresh`
Generates a new access token using a valid refresh token.

---

### **Workout Routines (workout_routines)**

#### **GET** `/workout_routines/`
Returns a welcome message for the fitness tracker.

#### **POST** `/workout_routines/createworkout`
Creates a new workout routine for the authenticated user.

#### **GET** `/workout_routines/showallworkouts`
Retrieves all workout routines for the authenticated user.

#### **GET** `/workout_routines/showallworkouts/{routine_id}`
Fetches details of a specific workout routine by its ID.

#### **PUT** `/workout_routines/updateworkouts/{routine_id}`
Updates the details of a specific workout routine.

#### **GET** `/workout_routines/filterworkoutsbydate`
Filters workout routines for the authenticated user by a specific date.

#### **PATCH** `/workout_routines/update_workout_details/{routine_id}`
Partially updates workout details for a specific routine.

#### **DELETE** `/workout_routines/delete_routine/{routine_id}`
Deletes a specific workout routine for the authenticated user.

---

## Built-in Swagger UI JWT Authorization

The API integrates a **JWT `Authorize` button** directly into the Swagger UI. This feature enhances the user experience by:
- Allowing users to input their Bearer tokens directly in the Swagger interface.
- Automatically including the token in requests to secured endpoints.
- Eliminating the need for external tools like Postman for testing.

### How to Use:
1. Click the `Authorize` button in the Swagger UI.
2. Enter your Bearer token in the format: `Bearer <JWT>`.
3. Test secured endpoints directly in the Swagger interface.

---

## Example Application
Here is a simple example of how you can use the API:

### 1. Signup
```bash
curl -X POST "http://<base_url>/auth/signup" \
-H "Content-Type: application/json" \
-d '{
    "username": "john_doe",
    "email": "john@example.com",
    "hashed_password": "password123"
}'
```

### 2. Login
```bash
curl -X POST "http://<base_url>/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "username": "john_doe",
    "hashed_password": "password123"
}'
```
Response:
```json
{
    "access": "<JWT_ACCESS_TOKEN>",
    "refresh": "<JWT_REFRESH_TOKEN>"
}
```

### 3. Create a Workout Routine
```bash
curl -X POST "http://<base_url>/workout_routines/createworkout" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <JWT_ACCESS_TOKEN>" \
-d '{
    "date": "2024-01-01",
    "routine_details": "Chest and Back Workout"
}'
```

### 4. Get All Workouts
```bash
curl -X GET "http://<base_url>/workout_routines/showallworkouts" \
-H "Authorization: Bearer <JWT_ACCESS_TOKEN>"
```

---

## Getting Started

### Prerequisites
- Python 3.9 or higher
- FastAPI
- A database (e.g., SQLite, PostgreSQL)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your_github_username>/fitness-tracker-api.git
   cd fitness-tracker-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start PostgreSQL with Docker Compose:
   ```bash
   docker-compose up -d
   ```

   **`docker-compose.yml`**:
   ```yaml
   version: "3.8"
   services:
     db:
       image: postgres:latest
       container_name: my_postgres_container
       environment:
         POSTGRES_USER: your_username
         POSTGRES_PASSWORD: your_password
         POSTGRES_DB: your_dbname
       ports:
         - "5432:5432"
       volumes:
         - ./data:/var/lib/postgresql/data
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

5. Access the API documentation:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
