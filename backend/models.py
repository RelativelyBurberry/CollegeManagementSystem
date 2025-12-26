# models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

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

    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="students")

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

    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="faculty")

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="faculty")

# =====================================================
# DEPARTMENT MODEL
# =====================================================

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)   # CSE, ECE
    name = Column(String, nullable=False)                # Computer Science

    students = relationship("Student", back_populates="department")
    faculty = relationship("Faculty", back_populates="department")
    courses = relationship("Course", back_populates="department")

# =====================================================
# COURSE MODEL
# =====================================================

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, nullable=False)  # CS101
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="courses")

# =====================================================
# FACULTY ↔ COURSE (ASSIGNMENT)
# =====================================================

class FacultyCourse(Base):
    __tablename__ = "faculty_courses"

    id = Column(Integer, primary_key=True, index=True)

    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    __table_args__ = (
        UniqueConstraint("faculty_id", "course_id", name="uq_faculty_course"),
    )


# =====================================================
# STUDENT ↔ COURSE (ENROLLMENT)
# =====================================================

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course"),
    )

# =====================================================
# ATTENDANCE SESSION
# =====================================================

class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False)

    date = Column(String, nullable=False)  # YYYY-MM-DD

# =====================================================
# ATTENDANCE RECORD
# =====================================================

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("attendance_sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    present = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint("session_id", "student_id", name="uq_session_student"),
    )


# =====================================================
# ASSIGNMENT
# =====================================================

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(String, nullable=False)  # YYYY-MM-DD


# =====================================================
# ASSIGNMENT SUBMISSION
# =====================================================

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"

    id = Column(Integer, primary_key=True, index=True)

    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    submission_text = Column(String, nullable=True)
    submitted_at = Column(String, nullable=False)

    marks = Column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint("assignment_id", "student_id", name="uq_assignment_student"),
    )


# =====================================================
# EXAM
# =====================================================

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False)

    name = Column(String, nullable=False)   # Midterm / Endsem
    max_marks = Column(Integer, nullable=False)
    exam_date = Column(String, nullable=False)


# =====================================================
# EXAM MARKS
# =====================================================

class ExamMark(Base):
    __tablename__ = "exam_marks"

    id = Column(Integer, primary_key=True, index=True)

    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    marks_obtained = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("exam_id", "student_id", name="uq_exam_student"),
    )


# =====================================================
# FINAL GRADE
# =====================================================

class FinalGrade(Base):
    __tablename__ = "final_grades"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    grade = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("course_id", "student_id", name="uq_course_grade"),
    )


# =====================================================
# TIMETABLE
# =====================================================

class Timetable(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    day_of_week = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    room = Column(String, nullable=True)

    course = relationship("Course")
