// now http.js only imports the *token* logic from auth.js
import coreFetch from "./coreFetch";
import { getAccessToken, refreshToken, clearAccessToken } from "./auth";

async function request(path, opts = {}, isRetry = false) {
  const { skipAuthRetry, ...restOpts } = opts;
  const token = getAccessToken();
  const cfg = {
    ...restOpts,
    headers: {
      ...(restOpts.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    }
  };

  const { raw, data, error } = await coreFetch(path, cfg);

  if (raw.status === 401 && !isRetry && !skipAuthRetry) {
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
  post: (path, body, headers, opts = {}) => request(path, { method: "POST", body, headers, ...opts }),
  put: (path, body, headers, opts = {}) => request(path, { method: "PUT", body, headers, ...opts }),
  delete: (path, headers, opts = {}) => request(path, { method: "DELETE", headers, ...opts })
};
