// now http.js only imports the *token* logic from auth.js
import coreFetch from "./coreFetch";
import { getAccessToken, refreshToken, clearAccessToken } from "./auth";

async function request(path, opts = {}, isRetry = false) {
  const token = getAccessToken();
  const cfg = {
    ...opts,
    headers: {
      ...(opts.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    }
  };

  const { raw, data, error } = await coreFetch(path, cfg);

  if (raw.status === 401 && !isRetry) {
    try {
      await refreshToken();
      return request(path, opts, true);
    } catch {
      clearAccessToken();
      return { data: null, error: "Session expired" };
    }
  }

  return raw.ok ? { data, error: null } : { data: null, error };
}

export default {
  get: (path, headers) => request(path, { method: "GET", headers }),
  post: (path, body, headers) => request(path, { method: "POST", body, headers }),
  put: (path, body, headers) => request(path, { method: "PUT", body, headers }),
  delete: (path, headers) => request(path, { method: "DELETE", headers })
};
