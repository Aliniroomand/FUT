import axios from 'axios';


// api for prices 

const API_BASE = 'http://localhost:8000';

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
