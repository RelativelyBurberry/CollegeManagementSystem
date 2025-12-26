import { requireRole } from "./auth.js";
import { apiGet } from "./api.js";

requireRole("student");


    async function loadStudentProfile() {
    const student = await apiGet("http://127.0.0.1:8000/students/me");

    // Name
    document.querySelector(".profile-name").innerText = student.name;

    // Department label
    const roleEl = document.querySelector(".profile-role");
    if (roleEl && student.department) {
        roleEl.innerText = `${student.department}`;
    }

    // Avatar initials
    const initials = student.name
        .split(" ")
        .map(n => n[0])
        .join("")
        .toUpperCase();

    const avatar = document.querySelector(".profile-img");
    if (avatar) {
        avatar.src = `https://ui-avatars.com/api/?name=${initials}&background=4361ee&color=fff&size=128`;
    }
}


    async function loadStudentCourses() {
        const courses = await apiGet("http://127.0.0.1:8000/students/my-courses");

        const select = document.getElementById("courseSelect");
        select.innerHTML = "";

        courses.forEach(c => {
            const opt = document.createElement("option");
            opt.value = c.id;
            opt.textContent = `${c.course_code} - ${c.course_name}`;
            select.appendChild(opt);
        });
    }

    async function loadAttendance() {
        const courseId = document.getElementById("courseSelect").value;

        const data = await apiGet(
            `http://127.0.0.1:8000/students/attendance/${courseId}`
        );

        document.getElementById("attendanceResult").innerText =
            data.attendance_percentage + "%";
    }

    async function loadFinalGrade() {
        const courseId = document.getElementById("courseSelect").value;

        const grade = await apiGet(
            `http://127.0.0.1:8000/students/final-grade/${courseId}`
        );

        document.getElementById("finalGrade").innerText =
            grade ? grade.grade : "Not Released";
    }

    async function loadStudentDashboard() {
        alert("dashboard function called");
        const data = await apiGet("http://127.0.0.1:8000/students/dashboard");
        console.log("Dashboard data:", data);

        const map = {
            coursesCount: data.courses,
            attendancePercent: data.attendance_percentage + "%",
            pendingAssignments: data.pending_assignments,
            daysToExam: data.days_to_exam
        };

        Object.entries(map).forEach(([id, value]) => {
            const el = document.getElementById(id);
            if (el) el.innerText = value;
        });
    }


    

    


    document.addEventListener("DOMContentLoaded", () => {
        loadStudentProfile();
        loadStudentDashboard();
        loadStudentCourses();
        const courseSelect = document.getElementById("courseSelect");

            if (courseSelect) {
            courseSelect.addEventListener("change", async () => {
                await loadAttendance();
                await loadFinalGrade();
            });
        }
    });

    

    const timetables = {
        "CSE": {
            "Monday": [
                { time: "8:00 AM - 9:30 AM", subject: "Data Structures", room: "CS-101", faculty: "Prof. Smith" },
                { time: "10:00 AM - 11:30 AM", subject: "Algorithms", room: "CS-102", faculty: "Prof. Johnson" },
                { time: "12:00 PM - 1:30 PM", subject: "Database Systems", room: "CS-103", faculty: "Prof. Williams" },
                { time: "2:00 PM - 3:30 PM", subject: "Operating Systems", room: "CS-104", faculty: "Prof. Brown" }
            ]
        }
    };

    function updateTimetable() {
        const dept = document.getElementById("departmentSelect").value;
        const day = document.getElementById("daySelect").value;
        const schedule = timetables[dept]?.[day] || [{ time: "No classes scheduled", subject: "-", room: "-", faculty: "-" }];

        document.getElementById("timetableContent").innerHTML = `
            <table class="timetable">
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Subject</th>
                        <th>Location</th>
                        <th>Faculty</th>
                    </tr>
                </thead>
                <tbody>
                    ${schedule.map(item => `
                        <tr>
                            <td class="class-time">${item.time}</td>
                            <td>
                                <div class="class-subject">${item.subject}</div>
                                ${item.faculty ? `<div class="class-details">${item.room} | ${item.faculty}</div>` : ''}
                            </td>
                            <td>${item.room}</td>
                            <td>${item.faculty}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>`;
    }

    // Sidebar navigation
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function() {
            document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            this.classList.add('active');
            document.getElementById(this.dataset.section).classList.add('active');

            // Update page title
            const pageTitle = document.querySelector('.page-title');
            pageTitle.textContent = this.dataset.section === 'home' ? 'Dashboard' : this.textContent.trim();
        });
    });

    // Timetable filter listeners
    document.getElementById("departmentSelect").addEventListener("change", updateTimetable);
    document.getElementById("daySelect").addEventListener("change", updateTimetable);
    document.addEventListener("DOMContentLoaded", updateTimetable);

    // Settings form buttons
    document.querySelector(".settings-form").addEventListener("submit", function(e) {
        e.preventDefault();
        alert("✅ Settings saved successfully!");
    });

    document.querySelector(".btn-outline").addEventListener("click", function() {
        if (confirm("Are you sure you want to cancel changes?")) {
            document.querySelector(".settings-form").reset();
        }
    });
