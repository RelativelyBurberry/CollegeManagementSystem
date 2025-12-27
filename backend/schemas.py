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


    model_config = {
    "from_attributes": True
    }


class FacultyDashboard(BaseModel):
    courses: int
    students: int
    pending_papers: int
    meetings_today: int


# =====================================================
# DEPARTMENT SCHEMAS
# =====================================================

class DepartmentBase(BaseModel):
    code: str
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int


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

class TimetableCreate(BaseModel):
    course_id: int
    day_of_week: str      # Monday, Tuesday, etc
    start_time: str       # HH:MM
    end_time: str         # HH:MM
    room: str | None = None


# =====================================================
# TIMETABLE SCHEMAS
# =====================================================

class TimetableResponse(BaseModel):
    day_of_week: str
    start_time: str
    end_time: str
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
