# Student Management System Using Microservices Architecture

## 1. Project Overview

The **Student Management System** is a backend application developed using Python, FastAPI, SQLite, and a microservices architecture. It provides REST APIs for user authentication, student management, course management, and student course enrollment.

The system consists of three independent microservices — Auth Service, Student Service, and Course Service — connected through a centralized API Gateway. The APIs are documented using Swagger UI and tested using Postman.

## 2. Technologies Used

- **Programming Language:** Python
- **Backend Framework:** FastAPI
- **Database:** SQLite
- **Architecture:** Microservices
- **Authentication:** JWT (JSON Web Token)
- **Password Security:** Password hashing
- **API Gateway:** FastAPI
- **API Testing:** Postman
- **API Documentation:** Swagger UI
- **Version Control:** Git and GitHub

## 3. Project Structure

```text
student-management/
├── api-gateway/
│   ├── main.py
│   └── requirements.txt
├── auth-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── database.py
│   └── requirements.txt
├── student-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── database.py
│   └── requirements.txt
├── course-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── database.py
│   └── requirements.txt
├── postman/
│   └── collection.json
├── screenshots/
└── README.md
```

## 4. System Architecture

### Auth Service
Responsible for user registration, login, JWT token generation, and retrieving the authenticated user's information.

### Student Service
Responsible for creating, retrieving, updating, and deleting student records.

### Course Service
Responsible for course management, student enrollment, and retrieving students enrolled in a particular course.

### API Gateway
Acts as the single entry point for client requests. It forwards requests to the appropriate microservice and returns service responses.

### Database
Each microservice maintains its own SQLite database to keep its data separate from the other services.

## 5. Service URLs

| Component | URL |
|---|---|
| API Gateway | `http://127.0.0.1:8000` |
| Auth Service | `http://127.0.0.1:8001` |
| Student Service | `http://127.0.0.1:8002` |
| Course Service | `http://127.0.0.1:8003` |

**Note:** Client and Postman requests should be sent through the API Gateway.

## 6. API Endpoints

All endpoints below are accessed through the API Gateway base URL: `http://127.0.0.1:8000`.

### Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate a user and obtain a JWT |
| GET | `/auth/me` | Retrieve the authenticated user's information |

### Student APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students` | Create a student |
| GET | `/students` | Retrieve all students |
| GET | `/students/{student_id}` | Retrieve a student by ID |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |

### Course APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/courses` | Create a course |
| GET | `/courses` | Retrieve all courses |
| GET | `/courses/{course_id}` | Retrieve a course by ID |
| PUT | `/courses/{course_id}` | Update a course |
| DELETE | `/courses/{course_id}` | Delete a course |

### Enrollment APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/enrollments` | Enroll a student in a course |
| GET | `/courses/{course_id}/students` | Retrieve students enrolled in a course |

## 7. Installation and Setup

### Prerequisites

- Python installed
- pip package manager
- Postman
- Git (for version control)

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
cd student-management
```

Replace `<your-github-repository-url>` with your actual GitHub repository URL.

### Step 2: Install Dependencies

Install the dependencies for each component using its respective requirements file.

For example, for the API Gateway:

```bash
cd api-gateway
pip install -r requirements.txt
```

Repeat for `auth-service`, `student-service`, and `course-service`.

### Step 3: Start the Microservices

Open separate terminal windows for the services and start each service from its respective directory.

Example for the API Gateway:

```bash
uvicorn main:app --reload --port 8000
```

For the Auth Service, Student Service, and Course Service, use the appropriate application module and port configured in each service.

**Important:** Start all three microservices before sending requests through the API Gateway. Use the correct startup commands for your actual project structure.

## 8. API Documentation

FastAPI provides interactive Swagger UI documentation for exploring and testing endpoints.

| Component | Swagger UI |
|---|---|
| API Gateway | `http://127.0.0.1:8000/docs` |
| Auth Service | `http://127.0.0.1:8001/docs` |
| Student Service | `http://127.0.0.1:8002/docs` |
| Course Service | `http://127.0.0.1:8003/docs` |

## 9. Authentication

The system uses JWT-based authentication for protected API endpoints.

1. Register a user through `/auth/register`.
2. Log in through `/auth/login`.
3. Copy the returned access token or configure Postman to save it automatically.
4. Use the token as a Bearer token when accessing protected endpoints.

Example authorization header:

```http
Authorization: Bearer <your_access_token>
```

Passwords are hashed before being stored in the database. Never commit real passwords, secret keys, or access tokens to the repository.

## 10. Testing with Postman

The Postman collection is available in the `postman/collection.json` file.

To test the application:

1. Start all microservices and the API Gateway.
2. Import `collection.json` into Postman.
3. Register a user and log in.
4. Obtain and use the JWT access token.
5. Test student CRUD operations.
6. Test course CRUD operations.
7. Test student enrollment and retrieving students by course.
8. Review the responses and status codes.

Screenshots of API testing results are stored in the `screenshots/` directory.

## 11. Features

- User registration and login
- JWT-based authentication
- Secure password hashing
- Student CRUD operations
- Course CRUD operations
- Student course enrollment
- Centralized API Gateway
- Independent microservices
- Separate SQLite databases
- Interactive Swagger UI documentation
- Postman API testing

## 12. Future Enhancements

- React-based frontend
- Role-based access control
- Improved logging and monitoring
- Docker-based deployment
- Automated unit and integration testing

## 13. Conclusion

The Student Management System demonstrates how to develop a backend application using FastAPI and a microservices architecture. It separates authentication, student management, and course management into independent services and uses an API Gateway to centralize request routing. SQLite provides persistent storage, while JWT authentication and Postman testing support secure API access and functional verification.

