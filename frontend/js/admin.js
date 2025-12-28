import { requireRole, logout } from "./auth.js";
import { apiGet } from "./api.js";

requireRole("admin");

const BASE = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");
console.log("TOKEN:", localStorage.getItem("token"));

let editingStudentId = null;

async function loadStudents() {
  try {
    const students = await apiGet("http://127.0.0.1:8000/students");
    const tbody = document.getElementById("studentsTable");
    tbody.innerHTML = "";

    students.forEach(s => {
      tbody.innerHTML += `
        <tr>
          <td>${s.id}</td>
          <td>${s.name}</td>
          <td>${s.reg_no}</td>
          <td>${s.email}</td>
          <td>${s.department_name}</td>
          <td class="action-cell">
            <button class="action-btn delete"
              onclick="deleteStudent(${s.id})">Delete</button>
            <button class="action-btn edit"
              onclick="editStudent(
                ${s.id},
                '${s.name}',
                '${s.reg_no}',
                '${s.email}',
                ${s.department_id}
              )">Edit</button>
          </td>
        </tr>
      `;
    });
  } catch (err) {
    console.error("Failed to load students:", err);
    alert("Failed to load students. Check auth or server.");
  }
}



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




document.addEventListener("DOMContentLoaded", () => {
  loadStudents();
  loadDepartments();
});

