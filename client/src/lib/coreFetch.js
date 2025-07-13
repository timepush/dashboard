export default async function coreFetch(path, { body, headers = {}, ...opts } = {}) {
  console.log("coreFetch options:", {
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(headers || {}) },
    body: body != null ? JSON.stringify(body) : undefined,
    ...opts
  }); // Log the headers being sent

  const res = await fetch(path, {
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(headers || {}) },
    body: body != null ? JSON.stringify(body) : undefined,
    ...opts
  });
  console.log("Response status:", res); // Log the response status

  let payload = null;
  try {
    payload = await res.json();
  } catch {}

  return {
    raw: res,
    data: res.ok ? payload : null,
    error: res.ok ? null : payload?.error || payload || res.statusText
  };
}
