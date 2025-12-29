# 🎓 College Management System  
**From chaotic spreadsheets to a production-grade academic platform**

---

## 🧭 Overview

The **College Management System (CMS)** is a full-stack web application built to solve a real, messy, and deeply fragmented problem:  
**managing academic data across students, faculty, and administrators without breaking consistency, security, or sanity.**

This project replaces manual spreadsheets and disconnected tools with a **centralized, role-based, API-driven system** that enforces correctness at every layer — database, backend, and frontend.

What began as “just another CRUD app” evolved into a **deep exercise in systems thinking, backend architecture, and real-world debugging**.

This repository represents not just a product — but a **learning curve conquered**.
 <br>
[Deployed CMS](https://collegemanagementsystem-frontend.onrender.com/login.html)

---

## 🎯 Why This Project Exists

Academic systems are deceptively complex:
- Multiple user roles with overlapping but restricted permissions
- Strong data relationships (students ↔ courses ↔ faculty ↔ departments)
- Time-based entities (timetables, schedules)
- High expectations of correctness

The goal of this project was to **design and implement such a system properly**, without shortcuts — even when it got painful.



---
## 🎥 Demo Videos

<video src = "https://github.com/user-attachments/assets/1a299361-c699-4edc-a5fc-b6fd4448f4af"></video> <br>

<video src = "https://github.com/user-attachments/assets/4aba6537-f192-4357-8d29-c2d520fb8c19"> </video> <br>

<video src="https://github.com/user-attachments/assets/4e6c360d-deee-45dc-9c16-881a880e9db4"></video> <br>

---


## 🛠️ Tech Stack

### Frontend
- HTML5  
- CSS3  
- JavaScript (ES6)  
- Fetch API  

### Backend
- Python  
- FastAPI  
- SQLAlchemy (ORM)  
- Pydantic  
- JWT Authentication  

### Database
- PostgreSQL  

### Dev & Deployment
- Git & GitHub  
- Render (Backend + PostgreSQL)  
- CORS Middleware  

---

## 🧱 System Architecture
```
Frontend (HTML/CSS/JS) 
| 
| REST APIs (JWT Secured)  
v 
FastAPI Backend 
| 
| ORM (SQLAlchemy) 
v 
PostgreSQL Database 
```
---



### Architectural Principles
- **Separation of concerns** — routers, schemas, models
- **Strict role isolation** — Admin ≠ Faculty ≠ Student
- **Stateless authentication** using JWT
- **Strong contracts** via Pydantic validation
- **Database-first thinking**, not UI-first shortcuts

---

## ✨ Features

### 🔐 Authentication & Authorization
- Secure JWT-based login
- Dependency-based role validation
- Protected routes per user type
- Zero trust between frontend and backend

### 🎓 Student Module
- Enrolled course visibility
- Attendance percentage calculation
- Results display with grade badges (S, A+, A, B, C, D, E, F)
- Dashboard summary metrics

### 🧑‍🏫 Faculty Module
- Faculty profile linked via foreign keys
- Teaching schedule (timetable)
- Assigned courses visibility

### 🛠️ Admin Module
- Student and faculty creation
- Department and course management
- Faculty–course mapping
- Controlled reassignment (“Change Faculty”) logic
- Backend-enforced filtering (no frontend hacks)

---

## 🧠 How This Was Built (The Real Version)

This project was built **iteratively, painfully, and correctly**.

### 1. Database First (No Shortcuts)
- Designed a normalized PostgreSQL schema
- Enforced foreign-key relationships
- Fixed cascading issues after breaking them
- Learned why **bad schemas haunt you forever**

### 2. Authentication Done Right
- Implemented JWT-based auth from scratch
- Learned the difference between:
  - Authentication vs Authorization
  - “Working” vs **secure**
- Debugged token handling across frontend and backend

### 3. Modular Backend Architecture
- Separate routers for admin, faculty, and student
- Dependency-injected role guards
- Pydantic schemas to prevent silent failures

### 4. Frontend–Backend Integration
- Manual Fetch API wiring (no frameworks to hide mistakes)
- Token storage and headers done explicitly
- UI state driven purely by backend truth

### 5. Debugging Hell (And Escaping It)
This project broke — repeatedly — in ways tutorials never warn you about:

- CORS failures that blocked everything
- ES module scoping bugs that silently killed functions
- Foreign-key filters that returned “nothing” but didn’t error
- Time datatype mismatches that broke timetables
- Faculty reassignment logic failing due to frontend assumptions

Each bug forced a deeper understanding of **why systems behave the way they do**.

---

## 📚 What I Learned (Beyond Code)

- Backend engineering is about **guarantees**, not features
- Databases are the real source of truth
- Role-based systems fail quietly if designed poorly
- Debugging is a skill, not a phase
- Reading logs beats guessing
- Clean architecture saves you when complexity explodes
- Building “properly” is harder — and worth it

Most importantly:
> I stopped thinking like someone writing code,  
> and started thinking like someone **building systems**.

---

## 🚀 Upcoming Features

- 📊 Advanced analytics dashboards
- 📅 Automated timetable generation
- 📎 Assignment upload & evaluation
- 📧 Email notifications
- 📱 Fully responsive UI redesign
- 🔐 Refresh token support
- 🧪 Automated API & integration testing

---

## 📂 Repository Structure



```
backend/
│── auth.py
│── database.py
│── models.py
│── schemas.py
│── routers/
│ ├── admin.py
│ ├── student.py
│ ├── faculty.py

frontend/
│── login.html
│── student.html
│── faculty.html
│── admin.html
│── js/
│ ├── login.js
│ ├── student.js
│ ├── faculty.js
│ ├── admin.js
```



---

## 🤝 Contributing

This project is under active development.  
Bug reports, feature suggestions, and pull requests are welcome.

---

## ⭐ Acknowledgements

Built as a real-world full-stack project to understand how **academic management systems work end-to-end**, from database design to role-based access control.


