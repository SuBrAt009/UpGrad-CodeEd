// src/api.js
export const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:5000";

async function request(path, { method = "GET", body, token } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
    credentials: "include", // ok even if you aren't using cookies
  });

  let data = null;
  try { data = await res.json(); } catch { /* non-JSON */ }

  if (!res.ok) {
    throw new Error((data && (data.message || data.error)) || `HTTP ${res.status}`);
  }
  return data;
}

export const api = {
  login: (userId, password) =>
    request("/api/auth/login", { method: "POST", body: { userId, password } }),

  saveWorkingProfessional: (payload, token) =>
    request("/api/profile/working-professional", { method: "POST", body: payload, token }),

  saveCollegeStudent: (payload, token) =>
    request("/api/profile/college-student", { method: "POST", body: payload, token }),

  getDashboard: (token) =>
    request("/api/suggest/dashboard", { method: "GET", token }),
};
