// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// قبل از ارسال هر درخواست محافظت‌شده، توکن JWT را اضافه کن
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

// رفرش توکن خودکار در صورت 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refresh_token = localStorage.getItem('refresh_token');
        if (refresh_token) {
          const res = await api.post('/auth/refresh-token', { refresh_token });
          if (res.data?.access_token) {
            localStorage.setItem('access_token', res.data.access_token);
            originalRequest.headers['Authorization'] = `Bearer ${res.data.access_token}`;
            return api(originalRequest);
          }
        }
      } catch (refreshErr) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }
    return Promise.reject(error);
  }
);

// سرویس‌های احراز هویت
export const login = async ({ email, password }) => {
  const response = await api.post('/auth/login', { email, password });
  if (response.data?.access_token) {
    localStorage.setItem('access_token', response.data.access_token);
  }
  if (response.data?.refresh_token) {
    localStorage.setItem('refresh_token', response.data.refresh_token);
  }
  return response.data;
};

// ثبت‌نام کامل (ایمیل + شماره + رمز)
export const register = async ({ phone_number, email, password }) => {
  const response = await api.post('/auth/register', { phone_number, email, password });
  if (response.data?.access_token) {
    localStorage.setItem('access_token', response.data.access_token);
  }
  if (response.data?.refresh_token) {
    localStorage.setItem('refresh_token', response.data.refresh_token);
  }
  return response.data;
};

// دریافت پروفایل کاربر جاری (شامل نقش)
export const getProfile = async () => {
  const response = await api.get('/profile/me');
  return response.data;
};

// logout ساده (پاک کردن توکن)
export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

// گرفتن access token جدید با refresh token
export const refreshToken = async () => {
  const refresh_token = localStorage.getItem('refresh_token');
  if (!refresh_token) throw new Error('No refresh token');
  const response = await api.post('/auth/refresh-token', { refresh_token });
  if (response.data?.access_token) {
    localStorage.setItem('access_token', response.data.access_token);
  }
  return response.data;
};
