from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User, Student, Faculty
from schemas import (
    StudentCreate,
   
    FacultyCreate
)
from auth import get_current_user, hash_password


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


'''@router.get("/ping")
def admin_ping():
    return {"msg": "admin alive"}'''

def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# =====================================================
# CREATE STUDENT (ADMIN ONLY)
@router.post("/students", status_code=201)
def create_student(
    student: StudentCreate,
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != "student":
        raise HTTPException(status_code=400, detail="Invalid student user")

    existing = db.query(Student).filter(Student.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student profile already exists")

    student_profile = Student(
        name=student.name,
        reg_no=student.reg_no,
        department=student.department,
        user_id=user_id
    )

    db.add(student_profile)
    db.commit()
    db.refresh(student_profile)

    return student_profile

@router.post("/faculty", status_code=201)
def create_faculty(
    faculty: FacultyCreate,
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    # 1. Validate user
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != "faculty":
        raise HTTPException(
            status_code=400,
            detail="Invalid faculty user"
        )

    # 2. Prevent duplicate faculty profile
    existing = db.query(Faculty).filter(Faculty.user_id == user_id).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Faculty profile already exists"
        )

    # 3. Create faculty profile
    faculty_profile = Faculty(
        name=faculty.name,
        employee_id=faculty.employee_id,
        department=faculty.department,
        user_id=user_id
    )

    db.add(faculty_profile)
    db.commit()
    db.refresh(faculty_profile)

    return faculty_profile


@router.put("/students/{student_id}")
def update_student(
    student_id: int,
    name: str | None = None,
    department: str | None = None,
    reg_no: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if name is not None:
        student.name = name
    if department is not None:
        student.department = department
    if reg_no is not None:
        student.reg_no = reg_no

    db.commit()
    db.refresh(student)
    return student

@router.delete("/students/{student_id}", status_code=204)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

@router.put("/faculty/{faculty_id}")
def update_faculty(
    faculty_id: int,
    name: str | None = None,
    department: str | None = None,
    employee_id: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    if name is not None:
        faculty.name = name
    if department is not None:
        faculty.department = department
    if employee_id is not None:
        faculty.employee_id = employee_id

    db.commit()
    db.refresh(faculty)
    return faculty

@router.delete("/faculty/{faculty_id}", status_code=204)
def delete_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    db.delete(faculty)
    db.commit()
