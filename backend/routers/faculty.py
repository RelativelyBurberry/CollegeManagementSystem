from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Faculty, User, Course, FacultyCourse
from auth import get_current_user,  get_current_faculty

from schemas import FacultyDashboard


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

@router.get("/dashboard", response_model=FacultyDashboard)
def faculty_dashboard(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_faculty)
    ):
    # TEMP stub data (same idea as student)
    return {
        "courses": 4,
        "students": 120,
        "pending_papers": 8,
        "meetings_today": 2
    }
    model_config = {"from_attributes": True}


@router.get("/my-courses")
def get_my_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    faculty = db.query(Faculty).filter(
        Faculty.user_id == current_user.id
    ).first()

    courses = (
        db.query(Course)
        .join(FacultyCourse, FacultyCourse.course_id == Course.id)
        .filter(FacultyCourse.faculty_id == faculty.id)
        .all()
    )

    return courses


from models import (
    Faculty,
    Course,
    FacultyCourse,
    Enrollment,
    AttendanceSession,
    AttendanceRecord,
    Student,
)
from schemas import AttendanceSessionCreate, AttendanceRecordCreate


@router.post("/attendance/session", status_code=201)
def create_attendance_session(
    data: AttendanceSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    faculty = db.query(Faculty).filter(
        Faculty.user_id == current_user.id
    ).first()

    # verify faculty teaches this course
    teaches = db.query(FacultyCourse).filter(
        FacultyCourse.faculty_id == faculty.id,
        FacultyCourse.course_id == data.course_id
    ).first()

    if not teaches:
        raise HTTPException(status_code=403, detail="Not assigned to this course")

    session = AttendanceSession(
        course_id=data.course_id,
        faculty_id=faculty.id,
        date=data.date
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session

@router.post("/attendance/mark", status_code=201)
def mark_attendance(
    data: AttendanceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    record = AttendanceRecord(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


from models import (
    Faculty,
    Course,
    FacultyCourse,
    Assignment,
    AssignmentSubmission,
    Enrollment,
    Student
)
from schemas import (
    AssignmentCreate,
    AssignmentGradeUpdate
)

@router.post("/assignments", status_code=201)
def create_assignment(
    data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    faculty = db.query(Faculty).filter(
        Faculty.user_id == current_user.id
    ).first()

    teaches = db.query(FacultyCourse).filter(
        FacultyCourse.faculty_id == faculty.id,
        FacultyCourse.course_id == data.course_id
    ).first()

    if not teaches:
        raise HTTPException(status_code=403, detail="Not assigned to this course")

    assignment = Assignment(
        course_id=data.course_id,
        faculty_id=faculty.id,
        title=data.title,
        description=data.description,
        due_date=data.due_date
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment

@router.get("/assignments/{assignment_id}/submissions")
def get_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    return db.query(AssignmentSubmission).filter(
        AssignmentSubmission.assignment_id == assignment_id
    ).all()


@router.put("/submissions/{submission_id}/grade")
def grade_submission(
    submission_id: int,
    data: AssignmentGradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    submission = db.query(AssignmentSubmission).filter(
        AssignmentSubmission.id == submission_id
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    submission.marks = data.marks
    db.commit()
    db.refresh(submission)

    return submission


from models import Exam, ExamMark, FinalGrade
from schemas import ExamCreate, ExamMarkCreate, GradeCreate

@router.post("/exams", status_code=201)
def create_exam(
    data: ExamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    faculty = db.query(Faculty).filter(
        Faculty.user_id == current_user.id
    ).first()

    exam = Exam(
        course_id=data.course_id,
        faculty_id=faculty.id,
        name=data.name,
        max_marks=data.max_marks,
        exam_date=data.exam_date
    )

    db.add(exam)
    db.commit()
    db.refresh(exam)

    return exam


@router.post("/exam-marks", status_code=201)
def upload_exam_marks(
    data: ExamMarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    marks = ExamMark(**data.dict())
    db.add(marks)
    db.commit()
    db.refresh(marks)

    return marks


@router.post("/final-grade", status_code=201)
def assign_final_grade(
    data: GradeCreate,
    db: Session = Depends(get_db),
        current_user: User = Depends(get_current_faculty)
    ):
    grade = FinalGrade(**data.dict())
    db.add(grade)
    db.commit()
    db.refresh(grade)

    return grade


from schemas import TimetableCreate
from models import Timetable

@router.post("/timetable", status_code=201)
def create_timetable_entry(
    data: TimetableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "faculty"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    entry = Timetable(**data.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


