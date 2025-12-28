# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, student, faculty, admin, course

# =====================================================
# CREATE FASTAPI APP
# =====================================================

app = FastAPI(title="College Management System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# CREATE DATABASE TABLES
# =====================================================

Base.metadata.create_all(bind=engine)

# =====================================================
# INCLUDE ROUTERS
# =====================================================

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(faculty.router)
app.include_router(admin.router)
app.include_router(course.router)

# =====================================================
# ROOT ENDPOINT
# =====================================================

@app.get("/")
def root():
    return {"message": "College Management System Backend Running"}
