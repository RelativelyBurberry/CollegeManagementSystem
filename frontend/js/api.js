export async function apiGet(url) {
    const token = localStorage.getItem("token");

    if (!token) {
        throw new Error("No token found");
    }

    const res = await fetch(url, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    });

    if (!res.ok) {
        throw new Error("API error");
    }

    return res.json();
}
