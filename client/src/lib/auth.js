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

// — SIGNIN —
export async function signin(email, password) {
  const { data, error } = await coreFetch("/api/auth/signin", {
    method: "POST",
    body: { email, password }
  });
  if (data) setAccessToken(data.token);
  return { data, error };
}

// — SIGNUP —
export async function signup(first_name, last_name, email, password) {
  const { data, error } = await coreFetch("/api/auth/signup", {
    method: "POST",
    body: { first_name, last_name, email, password }
  });
  if (data) setAccessToken(data.token);
  return { data, error };
}

// — REFRESH used by http.js —
export async function refreshToken() {
  const { raw, data, error } = await coreFetch("/api/auth/refresh", { method: "POST" });
  if (error || raw.status !== 200) throw new Error(error || "Refresh failed");
  setAccessToken(data.token);
  return data.token;
}

// — SIGNOUT —
export async function signout() {
  clearAccessToken();
  await coreFetch("/api/auth/signout", { method: "POST" });
}
