import { requireRole, logout } from "./auth.js";
import { apiGet } from "./api.js";

requireRole("admin");

const BASE = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");
console.log("TOKEN:", localStorage.getItem("token"));

let editingStudentId = null;
let allStudents = [];
let filteredStudents = [];
let studentPage = 1;
const STUDENTS_PER_PAGE = 5;

let selectedStudentId = null;

// reuse same allCourses from faculty flow
let studentFilteredCourses = [];
let studentCoursePage = 1;
const STUDENT_COURSES_PER_PAGE = 3;

let selectedStudentCourseId = null;


async function loadStudents() {
  allStudents = await apiGet(`${BASE}/students`);
  filteredStudents = allStudents;
  studentPage = 1;
  renderStudents();
}

function renderStudents() {
  const tbody = document.getElementById("studentsTable");
  tbody.innerHTML = "";

  const start = (studentPage - 1) * STUDENTS_PER_PAGE;
  const pageData = filteredStudents.slice(start, start + STUDENTS_PER_PAGE);

  pageData.forEach(s => {
    tbody.innerHTML += `
      <tr>
        <td>${s.id}</td>
        <td>${s.name}</td>
        <td>${s.reg_no}</td>
        <td>${s.email}</td>
        <td>${s.department_name}</td>
        <td>
          <button onclick="deleteStudent(${s.id})">Delete</button>
          <button onclick="editStudent(${s.id}, '${s.name}', '${s.reg_no}', '${s.email}', ${s.department_id})">Edit</button>
        </td>
      </tr>
    `;
  });

  document.getElementById("studentPageInfo").innerText =
    `Page ${studentPage} of ${Math.ceil(filteredStudents.length / STUDENTS_PER_PAGE)}`;
}

function nextStudentPage() {
  if (studentPage * STUDENTS_PER_PAGE < filteredStudents.length) {
    studentPage++;
    renderStudents();
  }
}

function prevStudentPage() {
  if (studentPage > 1) {
    studentPage--;
    renderStudents();
  }
}


document.getElementById("studentSearchInput")
  .addEventListener("input", e => {
    const q = e.target.value.toLowerCase();

    filteredStudents = allStudents.filter(s =>
      s.name.toLowerCase().includes(q) ||
      s.reg_no.toLowerCase().includes(q) ||
      s.email.toLowerCase().includes(q) ||
      s.department_name.toLowerCase().includes(q)
    );

    studentPage = 1;
    renderStudents();
  });

  let allFaculty = [];
let filteredFaculty = [];
let facultyPage = 1;
const FACULTY_PER_PAGE = 5;




window.deleteStudent = async function (id) {
    if (!confirm("Delete student?")) return;

    await fetch(`${BASE}/admin/students/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    });

    loadStudents();
};

window.logout = logout;

async function loadDepartments() {
  const res = await fetch("http://127.0.0.1:8000/admin/departments", {
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
  });

  const departments = await res.json();
  const select = document.getElementById("department_id");

  select.innerHTML = `<option value="">Select Department</option>`;

  departments.forEach(d => {
    const option = document.createElement("option");
    option.value = d.id;
    option.textContent = `${d.code} - ${d.name}`;
    select.appendChild(option);
  });
}

window.editStudent = function (
  id,
  name,
  regNo,
  email,
  departmentId
) {
  document.getElementById("name").value = name;
  document.getElementById("reg_no").value = regNo;
  document.getElementById("email").value = email;
  document.getElementById("department_id").value = departmentId;

  // email should NOT be editable once created
  document.getElementById("email").disabled = true;

  editingStudentId = id;
  document.getElementById("submitBtn").innerText = "Update";
};


window.submitStudent = async function () {
  const nameInput = document.getElementById("name");
    const regNoInput = document.getElementById("reg_no");
    const emailInput = document.getElementById("email");
    const deptSelect = document.getElementById("department_id");

    const nameVal = nameInput.value;
    const regNoVal = regNoInput.value;
    const deptIdVal = deptSelect.value;


  // CREATE: all fields required
    if (!editingStudentId) {
    if (!nameVal || !regNoVal || !email.value || !deptIdVal) {
        alert("Fill all fields");
        return;
    }
    }

    // UPDATE: email is ignored
    if (editingStudentId) {
    if (!nameVal || !regNoVal || !deptIdVal) {
        alert("Fill all fields");
        return;
    }
    }


  // CREATE
  if (!editingStudentId) {
    const payload = {
      name: nameVal,
      reg_no: regNoVal,
      email: email.value,
      department_id: parseInt(deptIdVal)
    };

    const res = await fetch("http://127.0.0.1:8000/admin/students", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      alert("Create failed");
      return;
    }
  }

  // UPDATE
  else {
    const url =
      `http://127.0.0.1:8000/admin/students/${editingStudentId}` +
      `?name=${nameVal}&reg_no=${regNoVal}&department_id=${deptIdVal}`;

    const res = await fetch(url, {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    });

    if (!res.ok) {
      alert("Update failed");
      return;
    }
  }

  // reset form
  editingStudentId = null;
  submitBtn.innerText = "Create";
  email.disabled = false;
  name.value = reg_no.value = email.value = "";
  department_id.value = "";

  loadStudents();
};

document.getElementById("studentSearchAssignInput")
  .addEventListener("input", e => {
    const q = e.target.value.toLowerCase();
    const box = document.getElementById("studentAssignResults");

    if (!q) {
      box.innerHTML = "";
      return;
    }

    const matches = allStudents
      .filter(s =>
        s.name.toLowerCase().includes(q) ||
        s.reg_no.toLowerCase().includes(q)
      )
      .slice(0, 3);

    box.innerHTML = "";

    matches.forEach(s => {
      const div = document.createElement("div");
      div.className = "search-item";
      div.innerText = `${s.name} (${s.reg_no})`;
      div.onclick = () => selectStudentForAssign(s);
      box.appendChild(div);
    });
});

function selectStudentForAssign(student) {
  selectedStudentId = student.id;

  document.getElementById("studentSearchAssignInput").value =
    `${student.name} (${student.reg_no})`;
  document.getElementById("studentSearchAssignInput").disabled = true;

  document.getElementById("studentAssignResults").innerHTML = "";
  document.getElementById("selectedStudentBox").style.display = "block";
  document.getElementById("selectedStudentText").innerText =
    `${student.name} – ${student.department_name}`;

  document.getElementById("changeStudentBtn").style.display = "inline-block";
  document.getElementById("assignStudentCourseCard").style.display = "block";

  loadStudentCourseMapping(student.id);
  loadCoursesForStudentAssign();
}

window.resetStudentAssign = function () {
  selectedStudentId = null;

  const input = document.getElementById("studentSearchAssignInput");
  input.value = "";
  input.disabled = false;

  document.getElementById("studentAssignResults").innerHTML = "";
  document.getElementById("selectedStudentBox").style.display = "none";
  document.getElementById("changeStudentBtn").style.display = "none";
  document.getElementById("assignStudentCourseCard").style.display = "none";
  document.getElementById("studentCourseTable").innerHTML = "";
};

function loadCoursesForStudentAssign() {
  studentFilteredCourses = allCourses;
  studentCoursePage = 1;
  renderStudentCourseResults();
}

document.getElementById("studentCourseSearchInput")
  .addEventListener("input", e => {
    const q = e.target.value.toLowerCase();

    studentFilteredCourses = allCourses.filter(c =>
      c.course_code.toLowerCase().includes(q) ||
      c.course_name.toLowerCase().includes(q)
    );

    studentCoursePage = 1;
    renderStudentCourseResults();
});

function renderStudentCourseResults() {
  const box = document.getElementById("studentCourseResults");
  box.innerHTML = "";

  if (studentFilteredCourses.length === 0) {
    box.innerHTML = `<div class="search-item muted">No courses found</div>`;
    document.getElementById("studentCoursePageInfo").innerText = "Page 0 of 0";
    return;
  }

  const start = (studentCoursePage - 1) * STUDENT_COURSES_PER_PAGE;
  const pageData = studentFilteredCourses.slice(start, start + STUDENT_COURSES_PER_PAGE);

  pageData.forEach(c => {
    const div = document.createElement("search-item");
    div.className = "search-item";
    div.innerText = `${c.course_code} – ${c.course_name}`;
    div.onclick = () => selectedStudentCourseId = c.id;
    box.appendChild(div);
  });

  document.getElementById("studentCoursePageInfo").innerText =
    `Page ${studentCoursePage} of ${Math.ceil(studentFilteredCourses.length / STUDENT_COURSES_PER_PAGE)}`;
}

window.nextStudentCoursePage = function () {
  if (studentCoursePage * STUDENT_COURSES_PER_PAGE < studentFilteredCourses.length) {
    studentCoursePage++;
    renderStudentCourseResults();
  }
};

window.prevStudentCoursePage = function () {
  if (studentCoursePage > 1) {
    studentCoursePage--;
    renderStudentCourseResults();
  }
};

window.assignCourseToStudent = async function () {
  if (!selectedStudentId || !selectedStudentCourseId) {
    alert("Select student and course");
    return;
  }

  const res = await fetch(`${BASE}/admin/enroll-student`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      student_id: selectedStudentId,
      course_id: selectedStudentCourseId
    })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Enrollment failed");
    return;
  }

  alert("✅ Student enrolled");
  loadStudentCourseMapping(selectedStudentId);
};


async function loadStudentCourseMapping(studentId) {
  const rows = await apiGet(`${BASE}/admin/student-courses?student_id=${studentId}`);
  const tbody = document.getElementById("studentCourseTable");

  tbody.innerHTML = "";

  rows.forEach(r => {
    tbody.innerHTML += `
      <tr>
        <td>${r.course_code} – ${r.course_name}</td>
        <td>${r.course_id}</td>
        <td>
          <button onclick="unassignStudentCourse(${studentId}, ${r.course_id})">
            Unassign
          </button>
        </td>
      </tr>
    `;
  });
}


window.unassignStudentCourse = async function (studentId, courseId) {
  if (!confirm("Unassign this course from student?")) return;

  await fetch(
    `${BASE}/admin/enroll-student?student_id=${studentId}&course_id=${courseId}`,
    {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    }
  );

  loadStudentCourseMapping(studentId);
};


let editingFacultyId = null;

async function loadFaculty() {
  allFaculty = await apiGet(`${BASE}/admin/faculty`);
  filteredFaculty = allFaculty;
  facultyPage = 1;
  renderFaculty();
}

function renderFaculty() {
  const tbody = document.getElementById("facultyTable");
  tbody.innerHTML = "";

  const start = (facultyPage - 1) * FACULTY_PER_PAGE;
  const pageData = filteredFaculty.slice(start, start + FACULTY_PER_PAGE);

  pageData.forEach(f => {
    tbody.innerHTML += `
      <tr>
        <td>${f.id}</td>
        <td>${f.name}</td>
        <td>${f.employee_id}</td>
        <td>${f.email || "-"}</td>
        <td>${f.department_name}</td>
        <td>
          <button onclick="editFaculty(${f.id}, '${f.name}', '${f.employee_id}', '${f.email}', ${f.department_id})">Edit</button>
          <button onclick="deleteFaculty(${f.id})">Delete</button>
        </td>
      </tr>
    `;
  });

  document.getElementById("facultyPageInfo").innerText =
    `Page ${facultyPage} of ${Math.ceil(filteredFaculty.length / FACULTY_PER_PAGE)}`;
}

function nextFacultyPage() {
  if (facultyPage * FACULTY_PER_PAGE < filteredFaculty.length) {
    facultyPage++;
    renderFaculty();
  }
}

function prevFacultyPage() {
  if (facultyPage > 1) {
    facultyPage--;
    renderFaculty();
  }
}


document.getElementById("facultyTableSearch")
  .addEventListener("input", e => {
    const q = e.target.value.toLowerCase();

    filteredFaculty = allFaculty.filter(f =>
      f.name.toLowerCase().includes(q) ||
      f.employee_id.toLowerCase().includes(q) ||
      (f.email || "").toLowerCase().includes(q) ||
      f.department_name.toLowerCase().includes(q)
    );

    facultyPage = 1;
    renderFaculty();
  });


window.addFacultyEmail = async function (facultyId) {
  const email = prompt("Enter faculty email:");
  if (!email) return;

  const res = await fetch(
    `http://127.0.0.1:8000/admin/faculty/${facultyId}/create-user`,
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email })
    }
  );

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Failed to create user");
    return;
  }

  alert("✅ User account created");
  loadFaculty();
};

let selectedFacultyId = null;
let selectedFacultyName = "";

window.searchFaculty = async function () {
  const q = document.getElementById("facultySearchInput").value.trim().toLowerCase();
  if (!q) return alert("Enter search term");

  const faculty = await apiGet(`${BASE}/admin/faculty`);

  const found = faculty.find(f =>
    f.name.toLowerCase().includes(q) ||
    f.employee_id.toLowerCase().includes(q)
  );

  if (!found) {
    alert("Faculty not found");
    return;
  }

  selectedFacultyId = found.id;
  selectedFacultyName = found.name;

  document.getElementById("selectedFacultyText").innerText =
    `${found.name} (${found.department_name})`;

  document.getElementById("selectedFacultyBox").style.display = "block";

  loadFacultyCourseMapping(); // 🔥 filtered
};


window.submitFaculty = async function () {
  const name = f_name.value.trim();
  const emp = f_emp.value.trim();
  const email = f_email.value.trim();
  const dept = f_department.value;

  if (!name || !emp || !dept || (!editingFacultyId && !email)) {
    alert("Fill all fields");
    return;
  }

  let res;

  if (!editingFacultyId) {
    res = await fetch(`${BASE}/admin/faculty`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name,
        employee_id: emp,
        email,
        department_id: parseInt(dept)
      })
    });
  } else {
    res = await fetch(
      `${BASE}/admin/faculty/${editingFacultyId}?name=${name}&employee_id=${emp}&department_id=${dept}`,
      {
        method: "PUT",
        headers: { "Authorization": `Bearer ${token}` }
      }
    );
  }

  if (!res.ok) {
    const err = await res.json();
    alert(err.detail || "Operation failed");
    return;
  }

  // reset
  editingFacultyId = null;
  f_submitBtn.innerText = "Create";
  f_email.disabled = false;
  f_name.value = f_emp.value = f_email.value = "";
  f_department.value = "";

  loadFaculty();
};


window.editFaculty = function (id, name, emp, email, dept) {
  f_name.value = name;
  f_emp.value = emp;
  f_email.value = email;
  f_department.value = dept;
  f_email.disabled = true;
  editingFacultyId = id;
  f_submitBtn.innerText = "Update";
};

window.deleteFaculty = async function (id) {
  if (!confirm("Delete faculty?")) return;
  await fetch(`http://127.0.0.1:8000/admin/faculty/${id}`, {
    method: "DELETE",
    headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
  });
  loadFaculty();
};

async function loadFacultyDepartments() {
  const depts = await apiGet("http://127.0.0.1:8000/admin/departments");
  f_department.innerHTML = `<option value="">Select Department</option>`;
  depts.forEach(d => {
    f_department.innerHTML += `<option value="${d.id}">${d.code} - ${d.name}</option>`;
  });
}


document.getElementById("facultySearchInput")
  .addEventListener("input", async (e) => {
    const q = e.target.value.trim();
    const resultsBox = document.getElementById("facultySearchResults");

    if (!q) {
      resultsBox.innerHTML = "";
      return;
    }

    const regex = new RegExp(q, "i");
    const faculty = await apiGet(`${BASE}/admin/faculty`);

    const matches = faculty
      .filter(f => regex.test(f.name) || regex.test(f.employee_id))
      .slice(0, 3);

    resultsBox.innerHTML = "";

    matches.forEach(f => {
      const div = document.createElement("div");
      div.className = "search-item";
      div.innerText = `${f.name} (${f.employee_id})`;
      div.onclick = () => selectFaculty(f);
      resultsBox.appendChild(div);
    });
});

function selectFaculty(faculty) {
  selectedFacultyId = faculty.id;

  const input = document.getElementById("facultySearchInput");
  input.value = `${faculty.name} (${faculty.employee_id})`;
  input.disabled = true;

  document.getElementById("facultySearchResults").innerHTML = "";

  document.getElementById("selectedFacultyBox").style.display = "block";
  document.getElementById("selectedFacultyText").innerText =
    `${faculty.name} (${faculty.department_name})`;

  document.getElementById("changeFacultyBtn").style.display = "inline-block";
  document.getElementById("assignCourseCard").style.display = "block";

  loadFacultyCourseMapping(selectedFacultyId);
  loadCoursesForAssign();

}



window.resetFaculty = function () 
{
  selectedFacultyId = null;

  const input = document.getElementById("facultySearchInput");
  input.value = "";
  input.disabled = false;

  document.getElementById("facultySearchResults").innerHTML = "";

  document.getElementById("selectedFacultyBox").style.display = "none";
  document.getElementById("changeFacultyBtn").style.display = "none";
  document.getElementById("assignCourseCard").style.display = "none";

  document.getElementById("facultyCourseTable").innerHTML = "";
}





let allCourses = [];
let filteredCourses = [];
let selectedCourseId = null;

let coursePage = 1;
const COURSES_PER_PAGE = 3;

function renderCourseResults() {
  const box = document.getElementById("courseSearchResults");
  box.innerHTML = "";

  if (filteredCourses.length === 0) {
    box.innerHTML = `<div class="search-item muted">No courses found</div>`;
    document.getElementById("coursePageInfo").innerText = "Page 0 of 0";
    return;
  }

  const start = (coursePage - 1) * COURSES_PER_PAGE;
  const pageData = filteredCourses.slice(start, start + COURSES_PER_PAGE);

  pageData.forEach(c => {
    const div = document.createElement("div");
    div.className = "search-item";
    div.innerText = `${c.course_code} – ${c.course_name}`;
    div.onclick = () => selectCourse(c);
    box.appendChild(div);
  });

  const totalPages = Math.ceil(filteredCourses.length / COURSES_PER_PAGE);

  document.getElementById("coursePageInfo").innerText =
    `Page ${coursePage} of ${totalPages}`;
}


document.getElementById("courseSearchInput")
  .addEventListener("input", e => {
    const q = e.target.value.toLowerCase();

    filteredCourses = allCourses.filter(c =>
      c.course_code.toLowerCase().includes(q) ||
      c.course_name.toLowerCase().includes(q)
    );

    coursePage = 1;
    renderCourseResults();
  });

  window.nextCoursePage = function () {
  if (coursePage * COURSES_PER_PAGE < filteredCourses.length) {
    coursePage++;
    renderCourseResults();
  }
}

window.prevCoursePage = function () {

  if (coursePage > 1) {
    coursePage--;
    renderCourseResults();
  }
}

function selectCourse(course) {
  selectedCourseId = course.id;

  document.getElementById("courseSearchInput").value =
    `${course.course_code} – ${course.course_name}`;

  document.getElementById("courseSearchResults").innerHTML = "";
}


async function loadCoursesForAssign() {
  allCourses = await apiGet(`${BASE}/admin/courses`);
  filteredCourses = allCourses;
  coursePage = 1;

  console.log("COURSES LOADED:", allCourses); // ✅ sanity check

  renderCourseResults();
}



window.assignCourse = async function () {
  if (!selectedFacultyId) {
    alert("Select a faculty first");
    return;
  }

  if (!selectedCourseId) {
    alert("Select a course");
    return;
  }

  const res = await fetch(
    `${BASE}/admin/assign-faculty`,
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        faculty_id: selectedFacultyId,
        course_id: selectedCourseId
      })
    }
  );

  if (!res.ok) {
    const err = await res.json();
    alert(err.detail || "Assignment failed");
    return;
  }

  alert("✅ Course assigned");
  selectedCourseId = null;
  document.getElementById("courseSearchInput").value = "";
  loadFacultyCourseMapping(selectedFacultyId);
};




async function loadFacultyCourseMapping(facultyId = null) {
  let url = "http://127.0.0.1:8000/admin/faculty-courses";
  if (facultyId) url += `?faculty_id=${facultyId}`;

  const rows = await apiGet(url);
  const tbody = document.getElementById("facultyCourseTable");

  tbody.innerHTML = "";

  rows.forEach(r => {
  tbody.innerHTML += `
    <tr>
      <td>${r.course_code} – ${r.course_name}</td>
      <td>${r.course_id}</td>
      <td>${r.student_count}</td>
      <td>
        <button class="action-btn delete"
          onclick="unassignCourse(${r.faculty_id}, ${r.course_id})">
          Unassign
        </button>
      </td>
    </tr>
  `;
});

}


window.unassignCourse = async function (facultyId, courseId) {
  if (!confirm("Unassign this course from faculty?")) return;

  const res = await fetch(
    `${BASE}/admin/faculty-courses?faculty_id=${facultyId}&course_id=${courseId}`,
    {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      }
    }
  );

  if (!res.ok) {
    const err = await res.text();
    alert(err || "Failed to unassign course");
    return;
  }

  alert("✅ Course unassigned");
  loadFacultyCourseMapping(facultyId);
};





document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".menu").forEach(item => {
    item.addEventListener("click", () => {
      document.querySelectorAll(".menu").forEach(m => m.classList.remove("active"));
      document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));

      item.classList.add("active");
      document.getElementById(item.dataset.section).classList.add("active");
    });
  });

  loadStudents();
  loadDepartments();
  loadFaculty();
  loadFacultyDepartments();
  loadCoursesForAssign();

});


