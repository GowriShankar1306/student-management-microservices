from fastapi import FastAPI, Request, Response, Depends
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
import httpx

from pydantic import BaseModel


app = FastAPI(title="Student Management API Gateway")

security = HTTPBearer()

AUTH_SERVICE_URL = "http://127.0.0.1:8001"
STUDENT_SERVICE_URL = "http://127.0.0.1:8002"
COURSE_SERVICE_URL = "http://127.0.0.1:8003"

class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class StudentRequest(BaseModel):
    name: str
    email: str
    phone: str
    department: str
    course_id: int | None = None

class StudentUpdateRequest(BaseModel):
    name: str
    email: str
    phone: str
    department: str
    course_id: int | None = None


class CourseRequest(BaseModel):
    name: str
    description: str
    duration: str

class CourseUpdateRequest(BaseModel):
    name: str
    description: str
    duration: str

class EnrollmentRequest(BaseModel):
    student_id: int
    course_id: int

@app.get("/")
def home():
    return {"message": "Student Management API Gateway is running"}


@app.get("/health")
def health():
    return {
        "gateway": "running",
        "auth_service": AUTH_SERVICE_URL,
        "student_service": STUDENT_SERVICE_URL,
        "course_service": COURSE_SERVICE_URL
    }


async def forward_request(
    request: Request,
    base_url: str,
    path: str,
    json_data: dict | None = None
):
    url = f"{base_url}/{path}"

    if request and request.url.query:
        url = f"{url}?{request.url.query}"

    headers = {}

    if request:
        headers = {
            key: value
            for key, value in request.headers.items()
            if key.lower() not in {
                "host",
                "content-length",
                "connection"
            }
        }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if json_data is not None:
                upstream = await client.request(
                    method=request.method,
                    url=url,
                    json=json_data,
                    headers=headers
                )
            else:
                body = await request.body()
                upstream = await client.request(
                    method=request.method,
                    url=url,
                    content=body,
                    headers=headers
                )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": "Requested service is unavailable"}
        )

    excluded_headers = {
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection"
    }

    response_headers = {
        key: value
        for key, value in upstream.headers.items()
        if key.lower() not in excluded_headers
    }

    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=response_headers,
        media_type=upstream.headers.get("content-type")
    )

@app.post("/auth/login")
async def login_gateway(data: LoginRequest):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream = await client.post(
                f"{AUTH_SERVICE_URL}/auth/login",
                json=data.model_dump()
            )

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type")
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": "Authentication Service is unavailable"}
        )


@app.post("/auth/register")
async def register_gateway(data: RegisterRequest):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream = await client.post(
                f"{AUTH_SERVICE_URL}/auth/register",
                json=data.model_dump()
            )

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type")
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": "Authentication Service is unavailable"}
        )

@app.get("/auth/me")
async def get_current_user(
    credentials=Depends(security)
):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream = await client.get(
                f"{AUTH_SERVICE_URL}/auth/me",
                headers={
                    "Authorization": f"Bearer {credentials.credentials}"
                }
            )

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type")
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": "Authentication Service is unavailable"}
        )

# Student 

@app.post("/students")
async def create_student(data: StudentRequest, request: Request, credentials=Depends(security)):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream = await client.post(
                f"{STUDENT_SERVICE_URL}/students",
                json=data.model_dump(),
                headers={
                    "Authorization": f"Bearer {credentials.credentials}"
                }
            )

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type")
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": "Student Service is unavailable"}
        )
    

@app.get("/students")
async def get_students(
    credentials=Depends(security)
):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream = await client.get(
                f"{STUDENT_SERVICE_URL}/students",
                headers={
                    "Authorization": f"Bearer {credentials.credentials}"
                }
            )

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type")
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": "Student Service is unavailable"}
        )

@app.put("/students/{student_id}")
async def update_student(
    student_id: int,
    data: StudentUpdateRequest,
    credentials=Depends(security)
):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream = await client.put(
                f"{STUDENT_SERVICE_URL}/students/{student_id}",
                json=data.model_dump(),
                headers={
                    "Authorization": f"Bearer {credentials.credentials}"
                }
            )

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type")
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": "Student Service is unavailable"}
        )


@app.get("/students/{student_id}")
async def get_student(
    student_id: int,
    credentials=Depends(security)
):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream = await client.get(
                f"{STUDENT_SERVICE_URL}/students/{student_id}",
                headers={
                    "Authorization": f"Bearer {credentials.credentials}"
                }
            )

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type")
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": "Student Service is unavailable"}
        )


@app.delete("/students/{student_id}")
async def delete_student(
    student_id: int,
    credentials=Depends(security)
):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream = await client.delete(
                f"{STUDENT_SERVICE_URL}/students/{student_id}",
                headers={
                    "Authorization": f"Bearer {credentials.credentials}"
                }
            )

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type")
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": "Student Service is unavailable"}
        )

# Courses

@app.get("/courses")
async def get_courses(
    request: Request,
    credentials=Depends(security)
):
    return await forward_request(
        request,
        COURSE_SERVICE_URL,
        "courses"
    )


@app.post("/courses")
async def create_course(
    data: CourseRequest,
    request: Request,
    credentials=Depends(security)
):
    return await forward_request(
        request,
        COURSE_SERVICE_URL,
        "courses",
        json_data=data.model_dump()
    )


@app.get("/courses/{course_id}")
async def get_course(
    course_id: int,
    request: Request,
    credentials=Depends(security)
):
    return await forward_request(
        request,
        COURSE_SERVICE_URL,
        f"courses/{course_id}"
    )


@app.put("/courses/{course_id}")
async def update_course(
    course_id: int,
    data: CourseUpdateRequest,
    credentials=Depends(security)
):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            upstream = await client.put(
                f"{COURSE_SERVICE_URL}/courses/{course_id}",
                json=data.model_dump(),
                headers={
                    "Authorization": f"Bearer {credentials.credentials}"
                }
            )

        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            media_type=upstream.headers.get("content-type")
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": "Course Service is unavailable"}
        )

@app.delete("/courses/{course_id}")
async def delete_course(
    course_id: int,
    request: Request,
    credentials=Depends(security)
):
    return await forward_request(
        request,
        COURSE_SERVICE_URL,
        f"courses/{course_id}"
    )


@app.get("/courses/{course_id}/students")
async def get_enrolled_students(
    course_id: int,
    request: Request,
    credentials=Depends(security)
):
    return await forward_request(
        request,
        COURSE_SERVICE_URL,
        f"courses/{course_id}/students"
    )


@app.post("/enrollments")
async def create_enrollment(
    data: EnrollmentRequest,
    request: Request,
    credentials=Depends(security)
):
    return await forward_request(
        request,
        COURSE_SERVICE_URL,
        "enrollments",
        json_data=data.model_dump()
    )
