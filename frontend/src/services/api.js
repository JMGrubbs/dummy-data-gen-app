const API_URL = (import.meta.env.VITE_API_URL || "http://localhost:8010").replace(/\/$/, "");

export class ApiError extends Error {
  constructor(message, status, payload) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}/api/v1${path}`, {
    ...options,
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : null;
  if (!response.ok) {
    const validationDetail = Array.isArray(payload?.detail)
      ? payload.detail.map((issue) => issue.msg).filter(Boolean).join(" ")
      : null;
    const detail = typeof payload?.detail === "string" ? payload.detail : validationDetail || payload?.message;
    throw new ApiError(detail || `Request failed (${response.status})`, response.status, payload);
  }
  return payload;
}

export const api = {
  login: (username, password) => request("/auth/login", { method: "POST", body: JSON.stringify({ username, password }) }),
  register: (username, password) => request("/auth/register", { method: "POST", body: JSON.stringify({ username, password }) }),
  me: () => request("/auth/me"),
  logout: () => request("/auth/logout", { method: "POST" }),
  health: () => request("/health"),
  ready: () => request("/health/ready"),
  live: () => request("/health/live"),
  projects: {
    list: () => request("/projects"),
    get: (projectId) => request(`/projects/${encodeURIComponent(projectId)}`),
    create: (name) => request("/projects", { method: "POST", body: JSON.stringify({ name }) }),
    update: (projectId, name) =>
      request(`/projects/${encodeURIComponent(projectId)}`, { method: "PUT", body: JSON.stringify({ name }) }),
    remove: (projectId) => request(`/projects/${encodeURIComponent(projectId)}`, { method: "DELETE" }),
  },
};
