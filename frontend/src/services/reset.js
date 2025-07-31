import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const requestReset = async (email) => {
  const response = await api.post('/auth/forgot-password', { email });
  // فرض بر این است که توکن ریست در ایمیل ارسال می‌شود
  // اگر توکن در پاسخ باشد، ذخیره کن:
  if (response.data && response.data.token) {
    localStorage.setItem('reset_token', response.data.token);
  }
  return response.data;
};

export const resetPassword = async ({ token, new_password }) => {
  const response = await api.post('/auth/reset-password', { token, new_password });
  // اگر توکن ریست نیاز به حذف دارد:
  localStorage.removeItem('reset_token');
  return response.data;
};
