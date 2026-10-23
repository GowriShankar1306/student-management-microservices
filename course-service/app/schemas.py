from pydantic import BaseModel, Field, ConfigDict

class CourseCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    duration: str = Field(min_length=1, max_length=50)

class CourseUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    duration: str = Field(min_length=1, max_length=50)

class CourseResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    duration: str

    model_config = ConfigDict(from_attributes=True)


class EnrollmentCreate(BaseModel):
    student_id: int = Field(gt=0)
    course_id: int = Field(gt=0)


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int

    model_config = ConfigDict(from_attributes=True)


class EnrolledStudentResponse(BaseModel):
    student_id: int
    name: str
    email: str
    phone: str
    department: str
