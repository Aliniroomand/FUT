import axios from 'axios';

// ایجاد یک instance از axios با تنظیمات پایه
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// افزودن interceptor برای مدیریت خطاها
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error('API Error:', error.response.data);
      return Promise.reject(error.response.data);
    }
    console.error('API Connection Error:', error.message);
    return Promise.reject(error);
  }
);

// Price APIs
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

// Transfer Method APIs
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
  try {
    const response = await api.get('/card-ranges/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createCardRange = async (data) => {
  try {
    const response = await api.post('/card-ranges/', data);
    return response.data;
  } catch (error) {
    throw error;
  }
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

// Authentication APIs (در صورت نیاز)
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