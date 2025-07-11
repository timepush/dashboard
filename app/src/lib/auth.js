// ⚠️ DOES NOT import http.js
import coreFetch from "./coreFetch";

// in-memory storage
let accessToken = null;
export function getAccessToken() {
  return accessToken;
}
export function setAccessToken(t) {
  accessToken = t;
}
export function clearAccessToken() {
  accessToken = null;
}

// — LOGIN —
export async function login(username, password) {
  const { data, error } = await coreFetch("/auth/login", {
    method: "POST",
    body: { username, password }
  });
  if (error) throw new Error(error);
  setAccessToken(data.access);
  return data;
}

// — SIGNUP —
export async function signup(username, email, password) {
  const { data, error } = await coreFetch("/auth/signup", {
    method: "POST",
    body: { username, email, password }
  });
  if (error) throw new Error(error);
  setAccessToken(data.access);
  return data;
}

// — REFRESH used by http.js —
export async function refreshToken() {
  const { raw, data, error } = await coreFetch("/auth/refresh", {
    method: "POST"
  });
  if (error || raw.status !== 200) throw new Error(error || "Refresh failed");
  setAccessToken(data.access);
  return data.access;
}

// — LOGOUT —
export function logout() {
  clearAccessToken();
  // optionally clear server cookie:
  // coreFetch('/auth/logout', { method: 'POST' })
}
