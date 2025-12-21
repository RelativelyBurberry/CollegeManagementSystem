# models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

# =====================================================
# USER MODEL (AUTH BASE)
# =====================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) #index is for faster search, db creates an index on this column and searches only that index
    '''SELECT * FROM users WHERE email = 'abc@gmail.com';
    Instead of scanning whole table, it scans only the index which is much faster
    Use index=True for:
    email
    username
    foreign keys
    anything used in WHERE'''
    email = Column(String, unique=True, index=True, nullable=False) #cannot be empty (nullable = False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "student" | "faculty" | "admin"
    is_active = Column(Boolean, default=True)

    # one-to-one relationships , ONE user account linked to EITHER one student profile OR one faculty profile
    student = relationship("Student", back_populates="user", uselist=False) #back_populates tells SQLAlchemy that two relationship fields are the two ends of the same connection.
    faculty = relationship("Faculty", back_populates="user", uselist=False)

# =====================================================
# STUDENT MODEL
# =====================================================

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    reg_no = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="student")

# =====================================================
# FACULTY MODEL
# =====================================================

class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    employee_id = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="faculty")
