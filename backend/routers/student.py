from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from database import get_db
from models import Student, User
from auth import decode_access_token

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# =====================================================
# HELPER → GET CURRENT USER FROM JWT
# =====================================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    user = db.query(User).filter(User.email == payload["sub"]).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# =====================================================
# CREATE STUDENT PROFILE (ADMIN ONLY)
# =====================================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_student(
    name: str,
    reg_no: str,
    department: str,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create students")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != "student":
        raise HTTPException(status_code=400, detail="Invalid student user")

    existing = db.query(Student).filter(Student.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student profile already exists")

    student = Student(
        name=name,
        reg_no=reg_no,
        department=department,
        user_id=user_id
    )

    db.add(student)
    db.commit()
    db.refresh(student)
    return student


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
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students allowed")

    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    return student


# =====================================================
# UPDATE STUDENT (ADMIN ONLY)
# =====================================================
@router.put("/{student_id}")
def update_student(
    student_id: int,
    name: str | None = None,
    department: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update students")

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if name:
        student.name = name
    if department:
        student.department = department

    db.commit()
    db.refresh(student)
    return student


# =====================================================
# DELETE STUDENT (ADMIN ONLY)
# =====================================================
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete students")

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
