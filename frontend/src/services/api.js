import axios from 'axios';

const API_BASE = 'http://localhost:8000';

// Price APIs
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

// Transfer Method APIs
export const getTransferMethods = async () => {
  const res = await axios.get(`${API_BASE}/transfer-methods/`);
  return res.data;
};

export const createTransferMethod = async (data) => {
  const res = await axios.post(`${API_BASE}/transfer-methods/`, data);
  return res.data;
};

export const getTransferMethod = async (method_id) => {
  const res = await axios.get(`${API_BASE}/transfer-methods/${method_id}`);
  return res.data;
};

export const updateTransferMethod = async (method_id, data) => {
  const res = await axios.put(`${API_BASE}/transfer-methods/${method_id}`, data);
  return res.data;
};

export const deleteTransferMethod = async (method_id) => {
  const res = await axios.delete(`${API_BASE}/transfer-methods/${method_id}`);
  return res.data;
};

export const getRangesForMethod = async (method_id) => {
  const res = await axios.get(`${API_BASE}/transfer-methods/${method_id}/ranges`);
  return res.data;
};

// Card Range APIs
export const getCardRanges = async () => {
  const res = await axios.get(`${API_BASE}/card-ranges/`);
  return res.data;
};

export const createCardRange = async (data) => {
  const res = await axios.post(`${API_BASE}/card-ranges/`, data);
  return res.data;
};

export const getCardRange = async (id) => {
  const res = await axios.get(`${API_BASE}/card-ranges/${id}`);
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

export const getRangesForCard = async (card_id) => {
  const res = await axios.get(`${API_BASE}/card-ranges/card/${card_id}`);
  return res.data;
};

// Player Card APIs
export const createPlayerCard = async (data) => {
  const res = await axios.post(`${API_BASE}/player-cards/`, data);
  return res.data;
};

export const getPlayerCards = async () => {
  const res = await axios.get(`${API_BASE}/player-cards/`);
  return res.data;
};

export const getPlayerCard = async (card_id) => {
  const res = await axios.get(`${API_BASE}/player-cards/${card_id}`);
  return res.data;
};

export const updatePlayerCard = async (card_id, data) => {
  const res = await axios.put(`${API_BASE}/player-cards/${card_id}`, data);
  return res.data;
};

export const deletePlayerCard = async (card_id) => {
  const res = await axios.delete(`${API_BASE}/player-cards/${card_id}`);
  return res.data;
};

export const getCardTransactions = async (card_id) => {
  const res = await axios.get(`${API_BASE}/player-cards/${card_id}/transactions`);
  return res.data;
};

export const sellPlayerCard = async (card_id, data) => {
  const res = await axios.post(`${API_BASE}/player-cards/${card_id}/sell`, data);
  return res.data;
};

export const buyPlayerCard = async (card_id, data) => {
  const res = await axios.post(`${API_BASE}/player-cards/${card_id}/buy`, data);
  return res.data;
};

// Transaction APIs
export const getTransactions = async () => {
  const res = await axios.get(`${API_BASE}/transactions/`);
  return res.data;
};

export const createTransaction = async (data) => {
  const res = await axios.post(`${API_BASE}/transactions/`, data);
  return res.data;
};

export const getTransaction = async (transaction_id) => {
  const res = await axios.get(`${API_BASE}/transactions/${transaction_id}`);
  return res.data;
};

export const getTransactionsForCard = async (card_id) => {
  const res = await axios.get(`${API_BASE}/transactions/card/${card_id}`);
  return res.data;
};

export const getTransactionStats = async (card_id) => {
  const res = await axios.get(`${API_BASE}/transactions/stats/${card_id}`);
  return res.data;
};