# main.py

from fastapi import FastAPI

from database import engine, Base
from routers import auth, student, faculty

# =====================================================
# CREATE FASTAPI APP
# =====================================================

app = FastAPI(title="College Management System")

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

# =====================================================
# ROOT ENDPOINT
# =====================================================

@app.get("/")
def root():
    return {"message": "College Management System Backend Running"}
