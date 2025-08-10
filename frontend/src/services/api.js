import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

// auth interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers["Authorization"] = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config;
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      try {
        const refresh_token = localStorage.getItem("refresh_token");
        if (refresh_token) {
          const r = await api.post("/auth/refresh-token", { refresh_token });
          if (r.data?.access_token) {
            localStorage.setItem("access_token", r.data.access_token);
            originalRequest.headers[
              "Authorization"
            ] = `Bearer ${r.data.access_token}`;
            return api(originalRequest);
          }
        }
      } catch (e) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      }
    }
    return Promise.reject(error);
  }
);

export default api;
