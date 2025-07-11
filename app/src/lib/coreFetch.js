const BASE = import.meta.env.VITE_API_URL;

export default async function coreFetch(path, { body, headers, ...opts } = {}) {
  const res = await fetch(BASE + path, {
    credentials: "include", // cookies for refresh
    headers: { "Content-Type": "application/json", ...(headers || {}) },
    body: body != null ? JSON.stringify(body) : undefined,
    ...opts
  });

  let payload = null;
  try {
    payload = await res.json();
  } catch {}

  return { raw: res, data: res.ok ? payload : null, error: res.ok ? null : payload?.detail || res.statusText };
}
