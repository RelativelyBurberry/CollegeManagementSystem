# 🎓 College Management System
The Smart College Management System 🎓 is a centralized platform for colleges to manage student enrollment 📝, faculty allocation 👩‍🏫, attendance tracking 📊, exams &amp; grades 🧾, and notifications 🔔. Built with usability, scalability &amp; security in mind, it ensures a smooth digital experience for both students and faculty.

---

## 📌 Overview

This project implements a centralized platform for managing college operations such as **authentication, student records, faculty profiles, attendance, timetables, and academic results**.

The system is built with a **FastAPI + PostgreSQL backend** and a **responsive HTML/CSS frontend**, using **JWT-based authentication** and **role-based authorization** to ensure security and data isolation between users.

Roles supported:
- **Admin** – system control and profile management  
- **Student** – academic dashboard access  
- **Faculty** – teaching and grading interface  

---
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/f9e91adf-9857-4251-94b6-8e54c7284456" /> <br>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/5e4bad1b-8ad2-48fc-9a93-103f89eaba38" /> <br>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/b80f594e-0cfe-42cc-aaa5-3181f8d30ba8" /> <br>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/9f534ec1-18e0-43ca-aced-1aa720d5b9f6" /> <br>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/d41b5c53-6c1d-4576-9d2c-13739e13edf0" /> <br>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/242d27d0-69d0-41e9-baff-a7dc2ea74b4b" /> <br>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/dbfcc25b-7796-4064-a429-04ee0aa97fff" /> <br>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/06cfaf2d-7fa2-478a-8b0d-35b642970e78" /> <br>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/51c56cbd-304a-4a48-bafd-42942ee690a1" />

---

## 🧱 System Architecture
Frontend (HTML/CSS/JS) <br>
│ <br>
│ REST API (JSON) <br>
▼ <br> 
FastAPI Backend <br>
├── Auth Router (JWT) <br>
├── Student Router <br>
├── Faculty Router <br>
├── Admin Router <br> 
│ <br>
▼ <br>
PostgreSQL Database <br>
├── Users <br>
├── Students <br>
└── Faculty <br>


- **JWT tokens** secure API access  
- **SQLAlchemy ORM** for database abstraction  
- **Pydantic schemas** for validation  
- **Role guards** for protected routes  

---

## 🛠️ Tech Stack

### Backend
- **Python 3**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy ORM**
- **Pydantic**
- **JWT (OAuth2)**
- **Passlib (bcrypt)**

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript**
- **Font Awesome**
- **Google Fonts**

### Tools & Utilities
- Git & GitHub  
- Postman (API testing)  
- pgAdmin / psql  

---

## ✨ Features

### 🔐 Authentication & Security
- JWT-based login system
- Password hashing using bcrypt
- Role-based access control (RBAC)
- Secure protected routes

### 👨‍🎓 Student Module
- Personalized dashboard
- View timetable
- Attendance overview
- Academic results
- Profile management

### 👩‍🏫 Faculty Module
- Teaching schedule
- Student attendance tracking
- Grade management
- Faculty dashboard analytics

### 🧑‍💼 Admin Module
- Create & manage users
- Assign roles (student / faculty)
- System-level access control

### ⚙️ Backend Design
- Clean RESTful API design
- Modular router structure
- ORM-based relational modeling
- Scalable project structure

---

## 🔨 How We Built It

1. **Designed database schema**
   - Separate `User`, `Student`, and `Faculty` tables
   - One-to-one relationships via foreign keys

2. **Implemented authentication**
   - JWT token creation & verification
   - OAuth2 password flow
   - Role guards (`admin`, `student`, `faculty`)

3. **Built REST APIs**
   - Modular routers for each role
   - Dependency-based DB session handling
   - Clean request/response validation

4. **Developed frontend**
   - Separate dashboards for students & faculty
   - Responsive UI with modern styling
   - API integration using `fetch`

5. **Integrated backend & frontend**
   - CORS configuration
   - Token-based session flow
   - Role-aware navigation

---

## 📚 What I Learned

- Designing **role-based backend architectures**
- Implementing **JWT authentication securely**
- Structuring scalable **FastAPI projects**
- Using **SQLAlchemy relationships correctly**
- Frontend–backend integration using REST APIs
- Debugging real-world auth & permission bugs
- Writing clean, production-style backend code

---

## 🚀 Upcoming Features

- 📊 Admin analytics dashboard
- 📝 Assignment & submission system
- 📧 Email notifications
- 🗂️ File uploads (notes, assignments)
- 📱 React frontend migration
- 🧪 Automated testing (PyTest)
- 🐳 Dockerized deployment

---

## ▶️ How to Run Locally

```bash
# Clone repository
git clone https://github.com/your-username/college-management-system.git
cd college-management-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload
```


