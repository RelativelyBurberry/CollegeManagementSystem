from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Faculty, User
from auth import get_current_user,  get_current_faculty


router = APIRouter(
    prefix="/faculty",
    tags=["Faculty"]
)



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
    current_user: User = Depends(get_current_faculty)
    ):
        faculty = db.query(Faculty).filter(
            Faculty.user_id == current_user.id
        ).first()

        if not faculty:
            raise HTTPException(status_code=404, detail="Faculty profile not found")

        return faculty
