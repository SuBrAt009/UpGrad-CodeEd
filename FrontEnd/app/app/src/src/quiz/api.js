// src/quiz/api.js
const API_BASE =
  (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE) ||
  process.env.REACT_APP_API_BASE ||
  "http://localhost:5000";

const BASE_PATH = "/api/quiz";

async function post(path, body) {
  const r = await fetch(`${API_BASE}${BASE_PATH}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(localStorage.getItem("token")
        ? { Authorization: `Bearer ${localStorage.getItem("token")}` }
        : {}),
    },
    credentials: "include",
    body: JSON.stringify(body || {}),
  });
  if (!r.ok) {
    const msg = await r.text().catch(() => "");
    throw new Error(msg || `HTTP ${r.status}`);
  }
  return r.json();
}

export const api = {
  start:        (payload) => post("/session/start",         payload),
  next:         (payload) => post("/session/next",          payload),
  hint:         (payload) => post("/session/hint",          payload),
  answer:       (payload) => post("/session/answer",        payload),
  explainBatch: (payload) => post("/session/explain_batch", payload),
};
