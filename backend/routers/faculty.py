from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from database import get_db
from models import Faculty, User
from auth import decode_access_token

router = APIRouter(
    prefix="/faculty",
    tags=["Faculty"]
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
# CREATE FACULTY PROFILE (ADMIN ONLY)
# =====================================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_faculty(
    name: str,
    employee_id: str,
    department: str,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create faculty")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != "faculty":
        raise HTTPException(status_code=400, detail="Invalid faculty user")

    existing = db.query(Faculty).filter(Faculty.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Faculty profile already exists")

    faculty = Faculty(
        name=name,
        employee_id=employee_id,
        department=department,
        user_id=user_id
    )

    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return faculty


# =====================================================
# GET ALL FACULTY (ADMIN ONLY)
# =====================================================
@router.get("/")
def get_all_faculty(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return db.query(Faculty).all()


# =====================================================
# GET OWN FACULTY PROFILE (FACULTY)
# =====================================================
@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "faculty":
        raise HTTPException(status_code=403, detail="Only faculty allowed")

    faculty = db.query(Faculty).filter(Faculty.user_id == current_user.id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty profile not found")

    return faculty


# =====================================================
# UPDATE FACULTY (ADMIN ONLY)
# =====================================================
@router.put("/{faculty_id}")
def update_faculty(
    faculty_id: int,
    name: str | None = None,
    department: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update faculty")

    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    if name:
        faculty.name = name
    if department:
        faculty.department = department

    db.commit()
    db.refresh(faculty)
    return faculty


# =====================================================
# DELETE FACULTY (ADMIN ONLY)
# =====================================================
@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete faculty")

    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    db.delete(faculty)
    db.commit()
