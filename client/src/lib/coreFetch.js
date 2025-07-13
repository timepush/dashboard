export default async function coreFetch(path, { body, headers, ...opts } = {}) {
  const res = await fetch(path, {
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(headers || {}) },
    body: body != null ? JSON.stringify(body) : undefined,
    ...opts
  });

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
