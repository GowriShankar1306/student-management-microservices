from pydantic import BaseModel, EmailStr, Field, ConfigDict


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)
    department: str = Field(min_length=2, max_length=100)
    course_id: int | None = None


class StudentUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)
    department: str = Field(min_length=2, max_length=100)
    course_id: int | None = None


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    department: str
    course_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
