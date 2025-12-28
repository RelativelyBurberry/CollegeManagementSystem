from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import AssignmentSubmission, Faculty, User, Course, FacultyCourse,Assignment, Enrollment,Timetable
from auth import get_current_user,  get_current_faculty

from schemas import FacultyDashboard,FacultyResponse

from datetime import datetime
from sqlalchemy import and_


from sqlalchemy import func
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
@router.get("/me", response_model=FacultyResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    faculty = (
        db.query(Faculty)
        .filter(Faculty.user_id == current_user.id)
        .first()
    )

    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty profile not found")

    return faculty


@router.get("/papers-summary")
def papers_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    faculty = db.query(Faculty).filter(
        Faculty.user_id == current_user.id
    ).first()

    rows = (
        db.query(
            Course.course_code,
            Assignment.title,
            func.count(AssignmentSubmission.id)
        )
        .join(Assignment, Assignment.course_id == Course.id)
        .join(AssignmentSubmission, AssignmentSubmission.assignment_id == Assignment.id)
        .join(FacultyCourse, FacultyCourse.course_id == Course.id)
        .filter(
            FacultyCourse.faculty_id == faculty.id,
            AssignmentSubmission.marks == None
        )
        .group_by(Course.course_code, Assignment.title)
        .all()
    )

    return [
        {
            "course": r[0],
            "title": r[1],
            "pending": r[2]
        }
        for r in rows
    ]

@router.get("/dashboard", response_model=FacultyDashboard)
def faculty_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
    ):
        faculty = db.query(Faculty).filter(
            Faculty.user_id == current_user.id
        ).first()

        # courses count
        courses_count = db.query(FacultyCourse).filter(
            FacultyCourse.faculty_id == faculty.id
        ).count()

        # students count (DISTINCT students across all courses)
        students_count = (
            db.query(func.count(func.distinct(Enrollment.student_id)))
            .join(FacultyCourse, FacultyCourse.course_id == Enrollment.course_id)
            .filter(FacultyCourse.faculty_id == faculty.id)
            .scalar()
        )

        pending_papers = (
            db.query(func.count(AssignmentSubmission.id))
            .join(Assignment, Assignment.id == AssignmentSubmission.assignment_id)
            .join(FacultyCourse, FacultyCourse.course_id == Assignment.course_id)
            .filter(
                FacultyCourse.faculty_id == faculty.id,
                AssignmentSubmission.marks == None
            )
            .scalar()
        )


        # meetings today (stub for now)
        meetings_today = 2

        now = datetime.now()
        today = now.strftime("%A")  # e.g. "Monday"
        current_time = now.time()

        classes_today = (
        db.query(Timetable)
        .join(FacultyCourse, FacultyCourse.course_id == Timetable.course_id)
        .filter(
                FacultyCourse.faculty_id == faculty.id,
                Timetable.day_of_week == today
            ).count()
        )

        next_class = (
            db.query(
                Course.course_name,
                Timetable.start_time,
                Timetable.room
            )
            .join(FacultyCourse, FacultyCourse.course_id == Course.id)
            .join(Timetable, Timetable.course_id == Course.id)
            .filter(
                FacultyCourse.faculty_id == faculty.id,
                Timetable.day_of_week == today,
                Timetable.start_time > current_time
            )
            .order_by(Timetable.start_time)
            .first()
        )

        next_class_info = None

        if next_class:
            next_class_info = {
                "course": next_class.course_name,
                "time": next_class.start_time.strftime("%I:%M %p"),
                "room": next_class.room
            }

        


        return {
            "courses": courses_count or 0,
            "students": students_count or 0,
            "pending_papers": pending_papers or 0,
            "meetings_today": meetings_today or 0,
            "classes_today": classes_today or 0,
            "next_class": next_class_info
        }


    



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


@router.get("/course/{course_id}/students")
def get_students_for_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    faculty = db.query(Faculty).filter(
        Faculty.user_id == current_user.id
    ).first()

    teaches = db.query(FacultyCourse).filter(
        FacultyCourse.faculty_id == faculty.id,
        FacultyCourse.course_id == course_id
    ).first()

    if not teaches:
        raise HTTPException(status_code=403, detail="Not assigned to this course")

    students = (
        db.query(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .filter(Enrollment.course_id == course_id)
        .all()
    )

    return [
        {
            "id": s.id,
            "name": s.name,
            "reg_no": s.reg_no
        }
        for s in students
    ]


@router.get("/students-summary")
def students_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_faculty)
):
    faculty = db.query(Faculty).filter(
        Faculty.user_id == current_user.id
    ).first()

    rows = (
        db.query(
            Course.course_name,
            Course.course_code,
            func.count(Enrollment.student_id)
        )
        .join(FacultyCourse, FacultyCourse.course_id == Course.id)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .filter(FacultyCourse.faculty_id == faculty.id)
        .group_by(Course.id)
        .all()
    )

    return [
        {
            "course": f"{r.course_code}: {r.course_name}",
            "students": r[2]
        }
        for r in rows
    ]


