import axios from 'axios';

const API_BASE = 'http://localhost:8000';

// API برای قیمت‌ها (فقط یک قیمت کلی برای خرید و فروش)
export const getLatestPrice = async () => {
  const response = await axios.get(`${API_BASE}/prices/latest`);
  return response.data;
};

export const setPrice = async (buy_price, sell_price) => {
  const response = await axios.post(`${API_BASE}/prices/`, {
    buy_price,
    sell_price,
  });
  return response.data;
};

// API برای روش‌های انتقال
export const getTransferMethods = async () => {
  const res = await axios.get(`${API_BASE}/transfer-methods/`);
  return res.data;
};

export const createTransferMethod = async (data) => {
  const res = await axios.post(`${API_BASE}/transfer-methods/`, data);
  return res.data;
};

export const updateTransferMethod = async (id, data) => {
  const res = await axios.put(`${API_BASE}/transfer-methods/${id}`, data);
  return res.data;
};

export const deleteTransferMethod = async (id) => {
  const res = await axios.delete(`${API_BASE}/transfer-methods/${id}`);
  return res.data;
};

// API جدید برای بازه‌های قیمتی (CardRanges)
export const getCardRanges = async () => {
  const res = await axios.get(`${API_BASE}/card-ranges/`);
  return res.data;
};

export const createCardRange = async (data) => {
  const res = await axios.post(`${API_BASE}/card-ranges/`, data);
  return res.data;
};

export const updateCardRange = async (id, data) => {
  const res = await axios.put(`${API_BASE}/card-ranges/${id}`, data);
  return res.data;
};

export const deleteCardRange = async (id) => {
  const res = await axios.delete(`${API_BASE}/card-ranges/${id}`);
  return res.data;
};
