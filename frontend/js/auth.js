export function getToken() {
    return localStorage.getItem("token");
}

export function getRole() {
    return localStorage.getItem("role");
}

export function requireRole(role) {
    const token = getToken();
    const userRole = getRole();

    if (!token || userRole !== role) {
        window.location.href = "login.html";
    }
}

export function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}
