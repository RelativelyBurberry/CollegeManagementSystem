# routers/student.py

from fastapi import APIRouter

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)
