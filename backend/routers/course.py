from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Course

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.get("/department/{department_id}")
def get_courses_by_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Course).filter(
        Course.department_id == department_id
    ).all()
