from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User, Student, Faculty
from schemas import (
    StudentCreate,
    AdminStudentCreate,
    FacultyCreate
)
from auth import get_current_user, hash_password
from models import Department, Course
from schemas import DepartmentCreate, CourseCreate

from models import Enrollment, FacultyCourse
from schemas import EnrollmentCreate, FacultyCourseCreate


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


'''@router.get("/ping")
def admin_ping():
    return {"msg": "admin alive"}'''

def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# =====================================================
# CREATE STUDENT (ADMIN ONLY)
@router.post("/students", status_code=201)
def create_student(
    data: AdminStudentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    # 1. Prevent duplicate user
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "User already exists")

    # 2. Create auth user
    user = User(
        email=data.email,
        hashed_password=hash_password("Temp@123"),
        role="student"
    )

    # 3. Create student profile
    student = Student(
        name=data.name,
        reg_no=data.reg_no,
        department_id=data.department_id,
        user=user
    )

    db.add_all([user, student])
    db.commit()
    db.refresh(student)

    return student


@router.put("/students/{student_id}")
def update_student(
    student_id: int,
    name: str | None = None,
    reg_no: str | None = None,
    department_id: int | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if name is not None:
        student.name = name
    if reg_no is not None:
        student.reg_no = reg_no
    if department_id is not None:
        student.department_id = department_id

    db.commit()
    db.refresh(student)
    return student


@router.delete("/students/{student_id}", status_code=204)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 👇 KEY FIX
    user = db.query(User).filter(User.id == student.user_id).first()

    db.delete(student)

    if user:
        db.delete(user)

    db.commit()



from schemas import AdminFacultyCreate

@router.get("/faculty")
def get_all_faculty(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    faculty = (
        db.query(Faculty)
        .join(User, User.id == Faculty.user_id)
        .join(Department, Department.id == Faculty.department_id)
        .all()
    )

    return [
        {
            "id": f.id,
            "name": f.name,
            "employee_id": f.employee_id,
            "email": f.user.email,
            "department_id": f.department_id,
            "department_name": f.department.name
        }
        for f in faculty
    ]


@router.post("/faculty", status_code=201)
def create_faculty(
    data: AdminFacultyCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    # check email uniqueness
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    # create auth user
    user = User(
        email=data.email,
        hashed_password=hash_password("Temp@123"),
        role="faculty"
    )

    # create faculty profile
    faculty = Faculty(
        name=data.name,
        employee_id=data.employee_id,
        department_id=data.department_id,
        user=user
    )

    db.add_all([user, faculty])
    db.commit()
    db.refresh(faculty)

    return faculty


@router.put("/faculty/{faculty_id}")
def update_faculty(
    faculty_id: int,
    name: str | None = None,
    employee_id: str | None = None,
    department_id: int | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    if name is not None:
        faculty.name = name
    if employee_id is not None:
        faculty.employee_id = employee_id
    if department_id is not None:
        faculty.department_id = department_id

    db.commit()
    db.refresh(faculty)
    return faculty


@router.delete("/faculty/{faculty_id}", status_code=204)
def delete_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(404, "Faculty not found")

    # delete dependent rows first
    db.query(FacultyCourse).filter(
        FacultyCourse.faculty_id == faculty_id
    ).delete()

    user = db.query(User).filter(User.id == faculty.user_id).first()

    db.delete(faculty)
    if user:
        db.delete(user)

    db.commit()




@router.get("/departments")
def get_departments(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return db.query(Department).all()


@router.post("/departments", status_code=201)
def create_department(
    dept: DepartmentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    department = Department(code=dept.code, name=dept.name)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department

@router.get("/courses")
def get_all_courses(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return db.query(Course).all()


@router.post("/courses", status_code=201)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    course_obj = Course(**course.dict())
    db.add(course_obj)
    db.commit()
    db.refresh(course_obj)
    return course_obj

from sqlalchemy import func


@router.get("/faculty-courses")
def get_faculty_course_mapping(
    faculty_id: int | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    query = (
        db.query(
            Faculty.id.label("faculty_id"),
            Faculty.name.label("faculty_name"),
            Course.id.label("course_id"),
            Course.course_code,
            Course.course_name,
            func.count(Enrollment.id).label("student_count")
        )
        .join(FacultyCourse, FacultyCourse.faculty_id == Faculty.id)
        .join(Course, Course.id == FacultyCourse.course_id)
        .outerjoin(
            Enrollment,
            Enrollment.course_id == Course.id
        )
        .group_by(
            Faculty.id,
            Course.id
        )
    )

    if faculty_id:
        query = query.filter(Faculty.id == faculty_id)

    rows = query.all()

    return [
        {
            "faculty_id": r.faculty_id,
            "faculty_name": r.faculty_name,
            "course_id": r.course_id,
            "course_code": r.course_code,
            "course_name": r.course_name,
            "student_count": r.student_count
        }
        for r in rows
    ]




@router.delete("/faculty-courses", status_code=204)
def unassign_faculty_course(
    faculty_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    mapping = db.query(FacultyCourse).filter(
        FacultyCourse.faculty_id == faculty_id,
        FacultyCourse.course_id == course_id
    ).first()

    if not mapping:
        raise HTTPException(404, "Mapping not found")

    db.delete(mapping)
    db.commit()



@router.post("/enroll-student", status_code=201)
def enroll_student(
    data: EnrollmentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    student = db.query(Student).filter(Student.id == data.student_id).first()
    course = db.query(Course).filter(Course.id == data.course_id).first()

    if not student or not course:
        raise HTTPException(status_code=400, detail="Invalid student or course ID")

    existing = db.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Student already enrolled")

    enrollment = Enrollment(**data.dict())
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment


@router.post("/assign-faculty", status_code=201)
def assign_faculty_to_course(
        data: FacultyCourseCreate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_admin)
    ):

    faculty = db.query(Faculty).filter(Faculty.id == data.faculty_id).first()
    course = db.query(Course).filter(Course.id == data.course_id).first()

    if not faculty or not course:
        raise HTTPException(status_code=400, detail="Invalid faculty or course ID")

    existing = db.query(FacultyCourse).filter(
        FacultyCourse.faculty_id == data.faculty_id,
        FacultyCourse.course_id == data.course_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Faculty already assigned to course")

    assignment = FacultyCourse(**data.dict())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


from schemas import FacultyUserCreate

@router.post("/faculty/{faculty_id}/create-user")
def create_user_for_faculty(
    faculty_id: int,
    data: FacultyUserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(404, "Faculty not found")

    if faculty.user_id is not None:
        raise HTTPException(400, "Faculty already has a user account")

    # prevent duplicate emails
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already exists")

    user = User(
        email=data.email,
        hashed_password=hash_password("Temp@123"),
        role="faculty"
    )

    faculty.user = user

    db.add(user)
    db.commit()
    db.refresh(faculty)

    return {
        "faculty_id": faculty.id,
        "email": user.email
    }

@router.get("/student-courses")
def get_student_courses(
    student_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    rows = (
        db.query(Course.id, Course.course_code, Course.course_name)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .filter(Enrollment.student_id == student_id)
        .all()
    )

    return [
        {
            "course_id": r.id,
            "course_code": r.course_code,
            "course_name": r.course_name
        }
        for r in rows
    ]

@router.delete("/enroll-student", status_code=204)
def unenroll_student(
    student_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id
    ).first()

    if not enrollment:
        raise HTTPException(404, "Enrollment not found")

    db.delete(enrollment)
    db.commit()
