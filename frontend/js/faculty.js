import { requireRole } from "./auth.js";
import { apiGet } from "./api.js";

requireRole("faculty");

async function loadFacultyProfile() {
    const faculty = await apiGet("http://127.0.0.1:8000/faculty/me");
    document.querySelector(".profile-name").innerText = faculty.name;
}

async function loadFacultyDashboard() {
    const data = await apiGet("http://127.0.0.1:8000/faculty/dashboard");

    document.getElementById("coursesCount").innerText = data.courses;
    document.getElementById("studentsCount").innerText = data.students;
    document.getElementById("pendingPapers").innerText = data.pending_papers;
    document.getElementById("meetingsToday").innerText = data.meetings_today;
}

/* ===============================
   COURSES TAUGHT BY FACULTY
================================ */
async function loadFacultyCourses() {
    const courses = await apiGet("http://127.0.0.1:8000/faculty/my-courses");

    const courseSelect = document.getElementById("courseSelect");
    const resultCourseSelect = document.getElementById("resultCourseSelect");

    courseSelect.innerHTML = "";
    resultCourseSelect.innerHTML = "";

    courses.forEach(c => {
        courseSelect.add(new Option(c.course_name, c.id));
        resultCourseSelect.add(new Option(c.course_name, c.id));
    });

    // Auto-load students for first course
    if (courses.length > 0) {
        await loadAttendanceStudents();
    }
}

/* ===============================
   LOAD STUDENTS FOR ATTENDANCE
================================ */
async function loadAttendanceStudents() {
    const courseId = document.getElementById("courseSelect").value;

    const students = await apiGet(
        `http://127.0.0.1:8000/faculty/course/${courseId}/students`
    );

    const tableBody = document.getElementById("attendanceTable");
    tableBody.innerHTML = "";

    students.forEach(s => {
        tableBody.innerHTML += `
            <tr>
                <td>${s.reg_no}</td>
                <td>${s.name}</td>
                <td>
                    <select data-student="${s.id}">
                        <option value="true">Present</option>
                        <option value="false">Absent</option>
                    </select>
                </td>
            </tr>
        `;
    });
}

/* ===============================
   SAVE ATTENDANCE
================================ */
async function saveAttendance() {
    const courseId = document.getElementById("courseSelect").value;
    const date = new Date().toISOString().split("T")[0];

    // Create attendance session
    const sessionRes = await fetch(
        "http://127.0.0.1:8000/faculty/attendance/session",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + getToken()
            },
            body: JSON.stringify({ course_id: courseId, date })
        }
    );

    const session = await sessionRes.json();

    // Mark attendance
    const selects = document.querySelectorAll("select[data-student]");
    for (const sel of selects) {
        await fetch(
            "http://127.0.0.1:8000/faculty/attendance/mark",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + getToken()
                },
                body: JSON.stringify({
                    session_id: session.id,
                    student_id: sel.dataset.student,
                    present: sel.value === "true"
                })
            }
        );
    }

    alert("Attendance saved successfully");
}

/* ===============================
   SAVE FINAL GRADE
================================ */
async function saveGrade(studentId) {
    const courseId = document.getElementById("resultCourseSelect").value;
    const grade = document.getElementById(`grade-${studentId}`).value;

    await fetch("http://127.0.0.1:8000/faculty/final-grade", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
        },
        body: JSON.stringify({
            course_id: courseId,
            student_id: studentId,
            grade: grade
        })
    });

    alert("Grade saved");
}

/* ===============================
   DOCUMENT LISTENERS 
================================ */
document.addEventListener("DOMContentLoaded", async () => {
    await loadFacultyDashboard();
    await loadFacultyCourses();

    // Attendance course change
    const courseSelect = document.getElementById("courseSelect");
    if (courseSelect) {
        courseSelect.addEventListener("change", loadAttendanceStudents);
    }

    // Save attendance button
    const saveAttendanceBtn = document.getElementById("saveAttendanceBtn");
    if (saveAttendanceBtn) {
        saveAttendanceBtn.addEventListener("click", saveAttendance);
    }
});


const timetables = {
            "CSE": {
                "Monday": [
                    { time: "9:00 AM - 10:30 AM", subject: "Data Structures", room: "CS-101", batch: "CS-201 (A)" },
                    { time: "11:00 AM - 12:30 PM", subject: "Advanced Algorithms", room: "CS-102", batch: "CS-301 (B)" },
                    { time: "2:00 PM - 3:30 PM", subject: "Research Seminar", room: "CS-103", batch: "PhD Candidates" }
                ],
                "Tuesday": [
                    { time: "10:00 AM - 11:30 AM", subject: "Research Methods", room: "CS-104", batch: "CS-401 (C)" },
                    { time: "2:00 PM - 4:00 PM", subject: "Thesis Guidance", room: "CS-105", batch: "PhD Candidates" }
                ],
                "Wednesday": [
                    { time: "9:00 AM - 11:00 AM", subject: "Department Meeting", room: "CS-Conference", batch: "Faculty" }
                ],
                "Thursday": [
                    { time: "10:00 AM - 12:00 PM", subject: "Data Structures", room: "CS-101", batch: "CS-201 (A)" },
                    { time: "2:00 PM - 3:30 PM", subject: "Advanced Algorithms", room: "CS-102", batch: "CS-301 (B)" }
                ],
                "Friday": [
                    { time: "9:00 AM - 11:00 AM", subject: "Research Colloquium", room: "CS-Auditorium", batch: "All Faculty" }
                ]
            }
        };

        const attendanceData = {
            "CS201": [
                { id: "CS2021001", name: "Kumar Abhishek", status: "Present", remarks: "" },
                { id: "CS2021002", name: "Priya Patel", status: "Present", remarks: "" },
                { id: "CS2021003", name: "Amit Singh", status: "Absent", remarks: "Medical leave" },
                { id: "CS2021004", name: "Neha Gupta", status: "Present", remarks: "" },
                { id: "CS2021005", name: "Sanjay Verma", status: "Late", remarks: "Arrived 15 mins late" }
            ],
            "CS301": [
                { id: "CS2021006", name: "Anjali Reddy", status: "Present", remarks: "" },
                { id: "CS2021007", name: "Vikram Joshi", status: "Present", remarks: "" },
                { id: "CS2021008", name: "Deepak Kumar", status: "Absent", remarks: "" },
                { id: "CS2021009", name: "Meera Nair", status: "Present", remarks: "" }
            ]
        };

        const gradeData = {
            "CS201": {
                "midterm": [
                    { id: "CS2021001", name: "Kumar Abhishek", marks: "95/100", grade: "S" },
                    { id: "CS2021002", name: "Priya Patel", marks: "78/100", grade: "B+" },
                    { id: "CS2021003", name: "Amit Singh", marks: "92/100", grade: "A+" },
                    { id: "CS2021004", name: "Harsh Gupta", marks: "65/100", grade: "C+" }
                ],
                "final": [
                    { id: "CS2021001", name: "Kumar Abhishek", marks: "98/100", grade: "S" },
                    { id: "CS2021002", name: "Priya Patel", marks: "82/100", grade: "A-" },
                    { id: "CS2021003", name: "Amit Singh", marks: "95/100", grade: "A+" },
                    { id: "CS2021004", name: "Harsh Gupta", marks: "70/100", grade: "B-" }
                ]
            },
            "CS301": {
                "midterm": [
                    { id: "CS2021005", name: "Sanjay Verma", marks: "88/100", grade: "A" },
                    { id: "CS2021006", name: "Anjali Reddy", marks: "72/100", grade: "B" },
                    { id: "CS2021007", name: "Vikram Joshi", marks: "95/100", grade: "A+" },
                    { id: "CS2021008", name: "Deepak Kumar", marks: "68/100", grade: "C+" }
                ],
                "final": [
                    { id: "CS2021005", name: "Sanjay Verma", marks: "90/100", grade: "A" },
                    { id: "CS2021006", name: "Anjali Reddy", marks: "85/100", grade: "A-" },
                    { id: "CS2021007", name: "Vikram Joshi", marks: "98/100", grade: "A+" },
                    { id: "CS2021008", name: "Deepak Kumar", marks: "75/100", grade: "B" }
                ]
            }
        };

        // Function to update timetable content
        function updateTimetable() {
            const dept = document.getElementById("departmentSelect").value;
            const day = document.getElementById("daySelect").value;
            const schedule = timetables[dept]?.[day] || [{ time: "No classes scheduled", subject: "", room: "", batch: "" }];

            document.getElementById("timetableContent").innerHTML = `
                <table class="timetable">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Subject</th>
                            <th>Location</th>
                            <th>Batch</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${schedule.map(item => `
                            <tr>
                                <td class="class-time">${item.time}</td>
                                <td>
                                    <div class="class-subject">${item.subject}</div>
                                    <div class="class-details">${item.batch} | Prof. Rohan </div>
                                </td>
                                <td>${item.room}</td>
                                <td>${item.batch}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>`;
        }

        // Function to update attendance content
        function updateAttendance() {
            const classId = document.getElementById("classSelect").value;
            const date = document.getElementById("attendanceDate").value || new Date().toISOString().split('T')[0];
            const attendance = attendanceData[classId] || [];
            
            document.getElementById("attendanceContent").innerHTML = `
                <div style="padding: 15px; background: #f9f9f9; border-bottom: 1px solid #eee; font-weight: 500; border-radius: 12px 12px 0 0;">
                    Attendance for ${document.getElementById("classSelect").options[document.getElementById("classSelect").selectedIndex].text} - ${new Date(date).toDateString()}
                </div>
                <table class="attendance-table">
                    <thead>
                        <tr>
                            <th>Student ID</th>
                            <th>Student Name</th>
                            <th>Status</th>
                            <th>Remarks</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${attendance.map(student => `
                            <tr>
                                <td>${student.id}</td>
                                <td>${student.name}</td>
                                <td>
                                    <span class="attendance-status ${student.status === 'Present' ? 'status-present' : student.status === 'Absent' ? 'status-absent' : 'status-late'}" onclick="changeAttendanceStatus(this)">
                                        ${student.status}
                                    </span>
                                </td>
                                <td><input type="text" value="${student.remarks}" class="form-control" style="padding: 6px 10px; width: 100%;" placeholder="Enter remarks"></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                
                <div class="form-actions" style="margin-top: 15px; padding: 15px; background: #f9f9f9; border-radius: 0 0 12px 12px;">
                    <button class="btn btn-outline" onclick="exportAttendance()">
                        <i class="fas fa-download"></i> Export
                    </button>
                    <button class="btn btn-primary" onclick="saveAttendance()">
                        <i class="fas fa-save"></i> Save Attendance
                    </button>
                </div>`;
        }

        // Function to update results content
        function updateResults() {
            const classId = document.getElementById("resultClassSelect").value;
            const examType = document.getElementById("examType").value;
            const results = gradeData[classId]?.[examType] || [];
            
            document.getElementById("resultsContent").innerHTML = `
                <div style="padding: 15px; background: #f9f9f9; border-bottom: 1px solid #eee; font-weight: 500; border-radius: 12px 12px 0 0;">
                    ${examType.charAt(0).toUpperCase() + examType.slice(1)} Results for ${document.getElementById("resultClassSelect").options[document.getElementById("resultClassSelect").selectedIndex].text}
                </div>
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Student ID</th>
                            <th>Student Name</th>
                            <th>Marks</th>
                            <th>Grade</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${results.map(student => `
                            <tr>
                                <td>${student.id}</td>
                                <td>${student.name}</td>
                                <td><input type="text" value="${student.marks}" class="form-control" style="padding: 6px 10px; width: 90px;"></td>
                                <td>
                                    <select class="grade-select" style="padding: 6px 10px; border-radius: 18px; border: none; background: ${student.grade === 'A' ? '#00b894' : student.grade.includes('B') ? '#0984e3' : student.grade.includes('C') ? '#fdcb6e' : '#d63031'}; color: white; font-weight: 600; text-align: center;">
                                        <option value="A" ${student.grade === 'A' ? 'selected' : ''}>A</option>
                                        <option value="A-" ${student.grade === 'A-' ? 'selected' : ''}>A-</option>
                                        <option value="B+" ${student.grade === 'B+' ? 'selected' : ''}>B+</option>
                                        <option value="B" ${student.grade === 'B' ? 'selected' : ''}>B</option>
                                        <option value="B-" ${student.grade === 'B-' ? 'selected' : ''}>B-</option>
                                        <option value="C+" ${student.grade === 'C+' ? 'selected' : ''}>C+</option>
                                        <option value="C" ${student.grade === 'C' ? 'selected' : ''}>C</option>
                                        <option value="D" ${student.grade === 'D' ? 'selected' : ''}>D</option>
                                    </select>
                                </td>
                                <td>
                                    <button class="btn btn-outline" style="padding: 6px 12px; font-size: 0.8rem;" onclick="saveGradeChanges(this, '${student.id}')">
                                        <i class="fas fa-save"></i> Save
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                
                <div class="form-actions" style="margin-top: 15px; padding: 15px; background: #f9f9f9; border-radius: 0 0 12px 12px;">
                    <button class="btn btn-outline" onclick="exportGrades()">
                        <i class="fas fa-download"></i> Export Grades
                    </button>
                    <button class="btn btn-primary" onclick="saveAllGradeChanges()">
                        <i class="fas fa-save"></i> Save All Changes
                    </button>
                </div>`;
        }

        // Function to change attendance status
        function changeAttendanceStatus(element) {
            const currentStatus = element.textContent.trim();
            const statuses = ["Present", "Absent", "Late"];
            const currentIndex = statuses.indexOf(currentStatus);
            const nextIndex = (currentIndex + 1) % statuses.length;
            const nextStatus = statuses[nextIndex];
            
            // Remove all classes
            element.classList.remove("status-present", "status-absent", "status-late");
            
            // Add new class
            if (nextStatus === "Present") {
                element.classList.add("status-present");
            } else if (nextStatus === "Absent") {
                element.classList.add("status-absent");
            } else {
                element.classList.add("status-late");
            }
            
            // Update text
            element.textContent = nextStatus;
        }

        // Function to save attendance
        function saveAttendance() {
            alert("Attendance saved successfully!");
            // In a real application, you would send this data to the server
        }

        // Function to export attendance
        function exportAttendance() {
            alert("Attendance exported as CSV file!");
            // In a real application, this would generate and download a CSV file
        }

        // Function to save grade changes
        function saveGradeChanges(button, studentId) {
            const row = button.closest("tr");
            const marksInput = row.querySelector("input");
            const gradeSelect = row.querySelector("select");
            
            // Update the grade data
            const classId = document.getElementById("resultClassSelect").value;
            const examType = document.getElementById("examType").value;
            const student = gradeData[classId][examType].find(s => s.id === studentId);
            
            if (student) {
                student.marks = marksInput.value;
                student.grade = gradeSelect.value;
            }
            
            // Visual feedback
            button.innerHTML = '<i class="fas fa-check"></i> Saved';
            button.style.backgroundColor = "#00b894";
            button.style.color = "white";
            button.style.borderColor = "#00b894";
            
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-save"></i> Save';
                button.style.backgroundColor = "";
                button.style.color = "";
                button.style.borderColor = "";
            }, 2000);
        }

        // Function to save all grade changes
        function saveAllGradeChanges() {
            alert("All grade changes saved successfully!");
            // In a real application, you would send all changes to the server
        }

        // Function to export grades
        function exportGrades() {
            alert("Grades exported as CSV file!");
            // In a real application, this would generate and download a CSV file
        }

        // Function to open modal
        function openModal(modalId) {
            document.getElementById(modalId).style.display = "flex";
            document.body.style.overflow = "hidden";
        }

        // Function to close modal
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = "none";
            document.body.style.overflow = "auto";
        }

        // Function to create floating particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 20;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');
                
                // Random size between 5px and 15px
                const size = Math.random() * 10 + 5;
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                
                // Random position
                particle.style.left = `${Math.random() * 100}%`;
                particle.style.top = `${Math.random() * 100}%`;
                
                // Random opacity
                particle.style.opacity = Math.random() * 0.5 + 0.1;
                
                // Random animation duration and delay
                const duration = Math.random() * 20 + 10;
                const delay = Math.random() * 5;
                particle.style.animation = `float-particle ${duration}s linear ${delay}s infinite`;
                
                particlesContainer.appendChild(particle);
            }
        }

        // Menu navigation functionality
        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('click', function() {
                document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));
                document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
                
                this.classList.add('active');
                document.getElementById(this.dataset.section).classList.add('active');
                
                // Update page title
                const pageTitle = document.querySelector('.page-title');
                if (this.dataset.section === 'home') {
                    pageTitle.textContent = 'Faculty Dashboard';
                } else {
                    const sectionName = this.textContent.trim();
                    pageTitle.textContent = sectionName;
                }
            });
        });

        // Initialize event listeners
        document.getElementById("departmentSelect").addEventListener("change", updateTimetable);
        document.getElementById("daySelect").addEventListener("change", updateTimetable);
        document.getElementById("classSelect").addEventListener("change", updateAttendance);
        document.getElementById("attendanceDate").addEventListener("change", updateAttendance);
        document.getElementById("resultClassSelect").addEventListener("change", updateResults);
        document.getElementById("examType").addEventListener("change", updateResults);

        // View Schedule button
        document.getElementById("viewScheduleBtn").addEventListener("click", function() {
            document.querySelector('.menu-item[data-section="timetable"]').click();
        });

        // Set Reminder button
        document.getElementById("setReminderBtn").addEventListener("click", function() {
            const bellIcon = this.querySelector('i');
            bellIcon.classList.add('ringing');
            setTimeout(() => {
                bellIcon.classList.remove('ringing');
            }, 500);
            openModal('reminderModal');
        });

        // Save Reminder button
        document.getElementById("saveReminderBtn").addEventListener("click", function() {
            const title = document.getElementById("reminderTitle").value;
            const date = document.getElementById("reminderDate").value;
            
            if (title && date) {
                alert(`Reminder set for ${new Date(date).toLocaleString()}: ${title}`);
                closeModal('reminderModal');
            } else {
                alert("Please fill in all fields");
            }
        });

        // Stat cards click handlers
        document.getElementById("coursesCard").addEventListener("click", function() {
            openModal('coursesModal');
        });

        document.getElementById("studentsCard").addEventListener("click", function() {
            openModal('studentsModal');
        });

        document.getElementById("papersCard").addEventListener("click", function() {
            openModal('papersModal');
        });

        document.getElementById("meetingsCard").addEventListener("click", function() {
            openModal('meetingsModal');
        });

        // Close modal buttons
        document.querySelectorAll('.close-modal').forEach(button => {
            button.addEventListener('click', function() {
                const modal = this.closest('.modal');
                closeModal(modal.id);
            });
        });

        // Close modal when clicking outside
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', function(e) {
                if (e.target === this) {
                    closeModal(this.id);
                }
            });
        });

        // Initialize on page load
        document.addEventListener("DOMContentLoaded", function() {
            // Set default date for attendance
            document.getElementById("attendanceDate").valueAsDate = new Date();
            
            // Load initial content
            updateTimetable();
            updateAttendance();
            updateResults();
            
            // Create floating particles
            createParticles();
            
            // Add animation delay to sections
            document.querySelectorAll('.section').forEach((section, index) => {
                section.style.transitionDelay = `${index * 0.1}s`;
            });
        });