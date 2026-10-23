import os
import httpx

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Course, Enrollment
from app.schemas import CourseCreate, CourseUpdate, CourseResponse, EnrollmentCreate, EnrollmentResponse, EnrolledStudentResponse


app = FastAPI(title="Course Service")

Base.metadata.create_all(bind=engine)

security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise RuntimeError("Set the JWT_SECRET_KEY environment variable")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user_id


STUDENT_SERVICE_URL = os.getenv(
    "STUDENT_SERVICE_URL",
    "http://127.0.0.1:8002"
)


def get_student(student_id: int, token: str) -> dict:
    url = f"{STUDENT_SERVICE_URL}/students/{student_id}"

    try:
        response = httpx.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Student Service is unavailable"
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if response.status_code in (401, 403):
        raise HTTPException(
            status_code=response.status_code,
            detail="Student Service rejected the authentication token"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to retrieve student details"
        )

    return response.json()



@app.get("/")
def home():
    return {"message": "Course Service is running"}


@app.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    course = Course(
        name=data.name,
        description=data.description,
        duration=data.duration
    )

    db.add(course)

    try:
        db.commit()
        db.refresh(course)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A course with this name already exists"
        )

    return course


@app.get("/courses", response_model=list[CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(Course).all()


@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return course


@app.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    data: CourseUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    course.name = data.name
    course.description = data.description
    course.duration = data.duration

    try:
        db.commit()
        db.refresh(course)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A course with this name already exists"
        )

    return course


@app.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    db.delete(course)
    db.commit()

    return {"message": "Course deleted successfully"}


@app.post(
    "/enrollments",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def enroll_student(
    data: EnrollmentCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    course = db.query(Course).filter(
        Course.id == data.course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    get_student(data.student_id, credentials.credentials)

    existing = db.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student is already enrolled in this course"
        )

    enrollment = Enrollment(
        student_id=data.student_id,
        course_id=data.course_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment


@app.get(
    "/courses/{course_id}/students",
    response_model=list[EnrolledStudentResponse]
)
def get_enrolled_students(
    course_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    enrollments = db.query(Enrollment).filter(
        Enrollment.course_id == course_id
    ).all()

    students = []

    for enrollment in enrollments:
        try:
            student = get_student(
                enrollment.student_id,
                credentials.credentials
            )
        except HTTPException as exc:
            if exc.status_code == status.HTTP_404_NOT_FOUND:
                continue
            raise

        students.append({
            "student_id": student["id"],
            "name": student["name"],
            "email": student["email"],
            "phone": student["phone"],
            "department": student["department"]
        })

    return students
