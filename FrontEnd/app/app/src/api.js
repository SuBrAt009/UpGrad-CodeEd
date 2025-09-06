// src/api.js
export const API_BASE = "http://localhost:5000";

// --- helpers ---
function extractTokenLoose(data) {
  // Try common fields
  if (data?.token) return data.token;
  if (data?.access_token) return data.access_token;
  if (data?.jwt) return data.jwt;

  // Try nested shapes
  if (data?.data?.token) return data.data.token;
  if (data?.data?.access_token) return data.data.access_token;
  if (data?.auth?.token) return data.auth.token;

  return null;
}

// Internal request helper with one automatic retry using alternate auth scheme
async function request(path, { method = "GET", body, token, _triedAlt } = {}) {
  const headers = {};

  // Only set JSON header when actually sending JSON
  if (method !== "OPTIONS" && method !== "GET") {
    headers["Content-Type"] = "application/json";
  }

  // Resolve token: explicit param wins, else localStorage
  const t = token ?? (typeof localStorage !== "undefined" ? localStorage.getItem("token") : null);

  // Choose auth scheme: default 'Bearer', or alternate 'JWT' on retry
  const useAltScheme = Boolean(_triedAlt);
  const scheme = useAltScheme ? "JWT" : "Bearer";
  if (t) headers.Authorization = `${scheme} ${t}`;

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body && method !== "GET" && method !== "OPTIONS" ? JSON.stringify(body) : null,
    credentials: "include",
  });

  // If 401 with Bearer and we have a token, retry once with JWT
  if (res.status === 401 && !_triedAlt && t) {
    console.warn(`[api] 401 with ${scheme}; retrying with ${useAltScheme ? "Bearer" : "JWT"}...`, path);
    return request(path, { method, body, token: t, _triedAlt: true });
  }

  let data = null;
  try { data = await res.json(); } catch { /* non-JSON */ }

  if (!res.ok) {
    const msg = (data && (data.message || data.error)) || `HTTP ${res.status}`;
    throw new Error(msg);
  }
  return data;
}

export const api = {
  // Login now AUTO-SAVES token from various response shapes
  login: async (email, password) => {
    const data = await request("/api/auth/login", {
      method: "POST",
      body: { email, password },
    });

    try {
      const tok = extractTokenLoose(data);
      if (tok) {
        localStorage.setItem("token", tok);
        console.log("[api] token saved to localStorage");
      } else {
        console.warn("[api] login response had no token; relying on cookies only", data);
      }
    } catch (e) {
      console.warn("[api] failed to parse token from login response:", e);
    }

    return data;
  },

  // Profile endpoints — call your actual routes
  saveCollegeStudent: (payload, token) =>
    request("/api/profile/college-student", {
      method: "POST",
      token,
      body: {
        degree: payload.degree,
        specialization: payload.specialisation,         // backend expects 'specialization'
        college: payload.collegeOrganization,           // backend expects 'college'
        interested_profession: payload.interestedProfessionStudent,
      },
    }),

  saveWorkingProfessional: (payload, token) =>
    request("/api/profile/working-professional", {
      method: "POST",
      token,
      body: {
        current_role: payload.currentRole,
        organization: payload.organization,
        interested_profession: payload.interestedProfession,
      },
    }),

  getDashboard: () => request("/api/suggest/dashboard", { method: "GET" }),
};
