from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Student, User, Course, Enrollment
from auth import get_current_user, get_current_student
from schemas import StudentDashboard



router = APIRouter(
    prefix="/students",
    tags=["Students"]
)



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
    current_user: User = Depends(get_current_student)
    ):
        student = db.query(Student).filter(
            Student.user_id == current_user.id
        ).first()

        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")

        return {
        "name": student.name,
        "department": student.department.name if student.department else None
    }


@router.get("/dashboard", response_model=StudentDashboard)
def student_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    # get student profile
    student = db.query(Student).filter(
        Student.user_id == current_user.id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # REAL course count from enrollments
    total_courses = db.query(Enrollment).filter(
        Enrollment.student_id == student.id
    ).count()

    # TEMP until attendance / assignments tables exist
    attendance_percentage = 0
    pending_assignments = 0
    days_to_exam = 14

    return {
        "courses": total_courses,
        "attendance_percentage": attendance_percentage,
        "pending_assignments": pending_assignments,
        "days_to_exam": days_to_exam
    }


@router.get("/my-courses")
def get_my_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    student = db.query(Student).filter(
        Student.user_id == current_user.id
    ).first()

    courses = (
        db.query(Course)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .filter(Enrollment.student_id == student.id)
        .all()
    )

    return courses


from models import AttendanceSession, AttendanceRecord

@router.get("/attendance/{course_id}")
def get_attendance_percentage(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    student = db.query(Student).filter(
        Student.user_id == current_user.id
    ).first()

    total = (
        db.query(AttendanceRecord)
        .join(AttendanceSession)
        .filter(
            AttendanceSession.course_id == course_id,
            AttendanceRecord.student_id == student.id
        )
        .count()
    )

    present = (
        db.query(AttendanceRecord)
        .join(AttendanceSession)
        .filter(
            AttendanceSession.course_id == course_id,
            AttendanceRecord.student_id == student.id,
            AttendanceRecord.present == True
        )
        .count()
    )

    percentage = (present / total * 100) if total > 0 else 0

    return {
        "course_id": course_id,
        "attendance_percentage": round(percentage, 2)
    }


from models import Assignment, AssignmentSubmission, Enrollment
from schemas import AssignmentSubmissionCreate


@router.get("/assignments/{course_id}")
def get_assignments(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    return db.query(Assignment).filter(
        Assignment.course_id == course_id
    ).all()

@router.post("/assignments/submit", status_code=201)
def submit_assignment(
    data: AssignmentSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    student = db.query(Student).filter(
        Student.user_id == current_user.id
    ).first()

    submission = AssignmentSubmission(
        assignment_id=data.assignment_id,
        student_id=student.id,
        submission_text=data.submission_text,
        submitted_at=data.submitted_at
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission


from models import Exam, ExamMark, FinalGrade

@router.get("/exam-marks/{course_id}")
def get_exam_marks(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    student = db.query(Student).filter(
        Student.user_id == current_user.id
    ).first()

    return (
        db.query(ExamMark)
        .join(Exam)
        .filter(
            Exam.course_id == course_id,
            ExamMark.student_id == student.id
        )
        .all()
    )


@router.get("/final-grade/{course_id}")
def get_final_grade(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    student = db.query(Student).filter(
        Student.user_id == current_user.id
    ).first()

    return db.query(FinalGrade).filter(
        FinalGrade.course_id == course_id,
        FinalGrade.student_id == student.id
    ).first()


