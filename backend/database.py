# database.py
import os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =====================================================
# DATABASE CONFIG
# =====================================================

# Change these according to your PostgreSQL setup
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "college_db"

DATABASE_URL = os.getenv("DATABASE_URL")


#connection string format for PostgreSQL

# =====================================================
# ENGINE
# =====================================================

engine = create_engine(
    DATABASE_URL,
    echo=True,          # Set False in production
    future=True
) #connection to the database

# =====================================================
# SESSION
# =====================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
) #each request gets its own session of db

# =====================================================
# BASE CLASS
# =====================================================

Base = declarative_base() #all models will inherit from this base class "Base"

# =====================================================
# DEPENDENCY
# =====================================================

def get_db():
    """
    Dependency to get DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#fast API dependency to get a database session for each request
'''Prevents:
connection leaks
crashes under load'''