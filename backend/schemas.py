# schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# =====================================================
# USER SCHEMAS (AUTH)
# =====================================================

class UserBase(BaseModel):
    email: EmailStr
    role: str  # student | faculty | admin


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


# =====================================================
# STUDENT SCHEMAS
# =====================================================

class StudentBase(BaseModel):
    name: str
    reg_no: str
    department: str


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# =====================================================
# FACULTY SCHEMAS
# =====================================================

class FacultyBase(BaseModel):
    name: str
    employee_id: str
    department: str


class FacultyCreate(FacultyBase):
    pass


class FacultyResponse(FacultyBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
