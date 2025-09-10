import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});



api.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(error); // خطاها به کامپوننت پاس داده می‌شن
  }
);



export const getLatestPrice = async () => {
  const response = await api.get("/prices/latest");
  return response.data;
};

export const setPrice = async (priceObj) => {
  const response = await api.post("/prices/", priceObj);
  return response.data;
};

export const getTransferMethods = async () => {
  const response = await api.get("/transfer-methods/");
  return response.data;
};

export const createTransferMethod = async (data) => {
  const response = await api.post("/transfer-methods/", data);
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
  const response = await api.get("/card-ranges/");
  return response.data;
};

export const createCardRange = async (data) => {
  const response = await api.post("/card-ranges/", data);
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
