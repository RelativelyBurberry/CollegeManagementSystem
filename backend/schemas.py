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



#====================================================
# ADMIN SCHEMAS
# =====================================================
class AdminStudentCreate(BaseModel):
    name: str
    reg_no: str
    department_id: int
    email: EmailStr

class AdminFacultyCreate(BaseModel):
    name: str
    employee_id: str
    department_id: int
    email: EmailStr


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


    model_config = {
    "from_attributes": True
    }


class StudentDashboard(BaseModel):
    courses: int
    attendance_percentage: int
    pending_assignments: int
    days_to_exam: int


# =====================================================
# DEPARTMENT SCHEMAS
# =====================================================

class DepartmentBase(BaseModel):
    code: str
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


# =====================================================
# FACULTY SCHEMAS
# =====================================================

class FacultyBase(BaseModel):
    name: str
    employee_id: str
    department: str


class FacultyCreate(FacultyBase):
    pass


class FacultyResponse(BaseModel):
    id: int
    name: str
    employee_id: str
    user_id: int
    department: DepartmentResponse   

    model_config = {
        "from_attributes": True
    }


from typing import Optional

class NextClass(BaseModel):
    course: str
    time: str
    room: str
    
class FacultyDashboard(BaseModel):
    courses: int
    students: int
    pending_papers: int
    meetings_today: int
    classes_today: int
    next_class: Optional[NextClass]




# =====================================================
# COURSE SCHEMAS
# =====================================================

class CourseBase(BaseModel):
    course_code: str
    course_name: str
    credits: int
    semester: int
    department_id: int

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int

# =====================================================
# ENROLLMENT SCHEMAS
# =====================================================

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


# =====================================================
# FACULTY COURSE SCHEMAS
# =====================================================

class FacultyCourseCreate(BaseModel):
    faculty_id: int
    course_id: int


# =====================================================
# ATTENDANCE SCHEMAS
# =====================================================

class AttendanceSessionCreate(BaseModel):
    course_id: int
    date: str  # YYYY-MM-DD


class AttendanceRecordCreate(BaseModel):
    session_id: int
    student_id: int
    present: bool

class AttendanceSummary(BaseModel):
    subject: str
    attended: int
    total: int
    percentage: int


# =====================================================
# ASSIGNMENT SCHEMAS
# =====================================================

class AssignmentCreate(BaseModel):
    course_id: int
    title: str
    description: str | None = None
    due_date: str  # YYYY-MM-DD

class AssignmentSubmissionCreate(BaseModel):
    assignment_id: int
    submission_text: str
    submitted_at: str

class AssignmentGradeUpdate(BaseModel):
    marks: int



# =====================================================
# EXAM SCHEMAS
# =====================================================

class ExamCreate(BaseModel):
    course_id: int
    name: str
    max_marks: int
    exam_date: str

class ExamMarkCreate(BaseModel):
    exam_id: int
    student_id: int
    marks_obtained: int

class GradeCreate(BaseModel):
    course_id: int
    student_id: int
    grade: str


# =====================================================
# TIMETABLE SCHEMAS
# =====================================================

from datetime import time

class TimetableCreate(BaseModel):
    course_id: int
    faculty_id: int
    day_of_week: str
    start_time: time
    end_time: time
    room: str



# =====================================================
# TIMETABLE SCHEMAS
# =====================================================

class TimetableResponse(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time
    room: str | None
    subject: str
    faculty: str | None
    model_config = {
        "from_attributes": True
    }

#====================================================
# STUDENT SETTINGS SCHEMAS
# =====================================================

from pydantic import BaseModel, EmailStr
from typing import Optional


class StudentSettingsUpdate(BaseModel):
    email: Optional[EmailStr] = None
    new_password: Optional[str] = None





from pydantic import BaseModel, EmailStr

class FacultyUserCreate(BaseModel):
    email: EmailStr
