import api from "./api";

export const getTransferMethodById = async (id) => {
  try {
    const res = await api.get(`/transfer-methods/${id}`);
    return res.data;
  } catch (err) {
    if (err.response) {
      const serverMsg = err.response.data?.detail || err.response.statusText;
      throw new Error(`Server error ${err.response.status}: ${serverMsg}`);
    }
    throw err;
  }
};
