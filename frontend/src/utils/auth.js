// utils/auth.js

export function getUserRole() {
  // فرض: نقش کاربر در localStorage ذخیره شده (مثلاً بعد از لاگین)
  // مقدار می‌تواند 'admin' یا 'user' باشد
  return localStorage.getItem('role');
}
