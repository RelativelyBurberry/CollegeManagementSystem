from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Student, User
from auth import get_current_user, get_current_student
from schemas import StudentDashboard



router = APIRouter(
    prefix="/students",
    tags=["Students"]
)



# =====================================================
# GET ALL STUDENTS (ADMIN / FACULTY)
# =====================================================
@router.get("/")
def get_all_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "faculty"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    return db.query(Student).all()


# =====================================================
# GET OWN STUDENT PROFILE (STUDENT)
# =====================================================
@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
    ):
        student = db.query(Student).filter(
            Student.user_id == current_user.id
        ).first()

        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")

        return student


@router.get("/dashboard", response_model=StudentDashboard)
def student_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    # TEMP values (we’ll replace with real logic later)
    return {
        "courses": 5,
        "attendance_percentage": 92,
        "pending_assignments": 3,
        "days_to_exam": 14
    }
