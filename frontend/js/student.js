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

    // Populate Department dropdown with student's department
    const deptSelect = document.getElementById("departmentSelect");

    if (deptSelect && student.department) {
        deptSelect.innerHTML = ""; // clear placeholder

        const option = document.createElement("option");
        option.value = student.department;
        option.textContent = student.department;
        option.selected = true;

        deptSelect.appendChild(option);
        deptSelect.disabled = true; // lock it
    }
    
    document.title = `${student.name} | Student Portal`;


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


    async function loadFinalGrade() {
        const courseId = document.getElementById("courseSelect").value;

        const grade = await apiGet(
            `http://127.0.0.1:8000/students/final-grade/${courseId}`
        );

        document.getElementById("finalGrade").innerText =
            grade ? grade.grade : "Not Released";
    }

    async function loadTimetable() {
        const container = document.getElementById("timetableContent");
        const daySelect = document.getElementById("daySelect");

        if (!container || !daySelect) return; // page guard

        const data = await apiGet("http://127.0.0.1:8000/students/my-timetable");

        function render(day) {
            const rows = data.filter(d => d.day_of_week === day);

            if (!rows.length) {
                container.innerHTML = "<p>No classes scheduled.</p>";
                return;
            }

            container.innerHTML = `
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
                        ${rows.map(r => `
                            <tr>
                                <td>${r.start_time} - ${r.end_time}</td>
                                <td>${r.subject}</td>
                                <td>${r.room ?? "-"}</td>
                                <td>${r.faculty ?? "-"}</td>
                            </tr>
                        `).join("")}
                    </tbody>

                </table>
            `;
        }

        // initial render
        render(daySelect.value);

        // re-render on day change
        daySelect.addEventListener("change", () => {
            render(daySelect.value);
        });
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


    async function loadAttendance() {
        try {
            
            const data = await apiGet("http://127.0.0.1:8000/students/attendance");
            document.getElementById("attendancePercent").innerText =
            data.attendance_percentage + "%";
        } catch (err) {
            console.error("Attendance failed:", err);
        }
    }


    
    async function loadAttendanceTable() {
    const tbody = document.querySelector(".attendance-table tbody");
    if (!tbody) return;

    try {
        const data = await apiGet(
            "http://127.0.0.1:8000/students/my-attendance-summary"
        );

        tbody.innerHTML = "";

        if (!data.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4">No attendance data available</td>
                </tr>
            `;
            return;
        }

        data.forEach(row => {
            let percentClass = "percent-high";
            if (row.percentage <60) percentClass = "percent-low";
            else if (row.percentage <=80) percentClass = "percent-medium";

            tbody.innerHTML += `
                <tr>
                    <td>${row.subject}</td>
                    <td>${row.attended}</td>
                    <td>${row.total}</td>
                    <td>
                        <span class="attendance-percent ${percentClass}">
                            ${row.percentage}%
                        </span>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        console.error("Attendance table failed:", err);
    }
}


    document.addEventListener("DOMContentLoaded", () => {
        loadStudentProfile();
        loadStudentDashboard();
        loadStudentCourses();
        loadTimetable();
        loadAttendanceTable();
        const courseSelect = document.getElementById("courseSelect");

            if (courseSelect) {
            courseSelect.addEventListener("change", async () => {
                await loadAttendance();
                await loadFinalGrade();
                
            });
        }
    });

    

    


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
