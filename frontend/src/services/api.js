// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// فقط خطا رو reject کن، نه console.log و نه toast
api.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(error); // خطاها به کامپوننت پاس داده می‌شن
  }
);

// فقط دیتا رو برگردون، نه catch و نه throw
export const getLatestPrice = async () => {
  const response = await api.get('/prices/latest');
  return response.data;
};

export const setPrice = async (buy_price, sell_price) => {
  const response = await api.post('/prices/', {
    buy_price,
    sell_price,
  });
  return response.data;
};

export const getTransferMethods = async () => {
  const response = await api.get('/transfer-methods/');
  return response.data;
};

export const createTransferMethod = async (data) => {
  const response = await api.post('/transfer-methods/', data);
  return response.data;
};

export const getTransferMethod = async (method_id) => {
  const response = await api.get(`/transfer-methods/${method_id}`);
  return response.data;
};

export const updateTransferMethod = async (method_id, data) => {
  const response = await api.put(`/transfer-methods/${method_id}`, data);
  return response.data;
};

export const deleteTransferMethod = async (method_id) => {
  const response = await api.delete(`/transfer-methods/${method_id}`);
  return response.data;
};

export const getRangesForMethod = async (method_id) => {
  const response = await api.get(`/transfer-methods/${method_id}/ranges`);
  return response.data;
};

// Card Ranges APIs
export const getCardRanges = async () => {
  const response = await api.get('/card-ranges/');
  return response.data;
};

export const createCardRange = async (data) => {
  const response = await api.post('/card-ranges/', data);
  return response.data;
};

export const updateCardRange = async (id, data) => {
  const response = await api.put(`/card-ranges/${id}`, data);
  return response.data;
};

export const deleteCardRange = async (id) => {
  const response = await api.delete(`/card-ranges/${id}`);
  return response.data;
};

export const getRangesForAmount = async (amount) => {
  const response = await api.get(`/card-ranges/for-amount/${amount}`);
  return response.data;
};

// Player Cards APIs
export const getPlayerCards = async () => {
  const response = await api.get('/player-cards/');
  return response.data;
};

export const createPlayerCard = async (data) => {
  const response = await api.post('/player-cards/', data);
  return response.data;
};

export const getPlayerCard = async (id) => {
  const response = await api.get(`/player-cards/${id}`);
  return response.data;
};

export const updatePlayerCard = async (id, data) => {
  const response = await api.put(`/player-cards/${id}`, data);
  return response.data;
};

export const deletePlayerCard = async (id) => {
  const response = await api.delete(`/player-cards/${id}`);
  return response.data;
};

// Authentication APIs
export const login = async (credentials) => {
  const response = await api.post('/auth/login', credentials);
  return response.data;
};

export const logout = async () => {
  const response = await api.post('/auth/logout');
  return response.data;
};

export const getProfile = async () => {
  const response = await api.get('/auth/profile');
  return response.data;
};
// بررسی اینکه بازیکن در بازه‌ای استفاده شده یا نه
export async function checkPlayerUsage(playerId) {
  const response = await fetch(`/api/player-cards/${playerId}/usage`);
  if (!response.ok) throw new Error("Failed to check player usage");
  return await response.json();
}

// حذف همه بازه‌هایی که بازیکن primary_card آن‌ها بوده
export async function deleteRangesWithPrimaryCard(playerId) {
  const response = await fetch(`/api/card-ranges/by-primary-card/${playerId}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error("Failed to delete related ranges");
  return await response.json();
}
