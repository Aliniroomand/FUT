import api from "./api";

/**
 * getTransactions:
 * filters: object with optional keys: card_id, transaction_type, customer_phone, customer_email,
 * is_settled, is_successful, debt_or_credit_type, min_amount, max_amount, start_date, end_date, sort_by, sort_order
 */
export const getTransactions = async (params = {}) => {
  try {
    const res = await api.get("/transactions", { params });
    if (!res.data || !("items" in res.data)) {
      throw new Error("Invalid response from server");
    }
    return res.data; // { items, total }
  } catch (err) {
    if (err.response) {
      const serverMsg = err.response.data?.detail || err.response.statusText;
      throw new Error(`Server error ${err.response.status}: ${serverMsg}`);
    }
    throw err;
  }
};


export const createTransaction = async (transactionData) => {
  try {
    const res = await api.post("/transactions/", transactionData);
    return res.data;
  } catch (err) {
    if (err.response) {
      const serverMsg = err.response.data?.detail || err.response.statusText;
      throw new Error(`Server error ${err.response.status}: ${serverMsg}`);
    }
    throw err;
  }
};

export const updateTransactionSettled = async (id, isSettled) => {
  try {
    const res = await api.patch(`/transactions/${id}`, { is_settled: isSettled });
    return res.data;
  } catch (err) {
    if (err.response) {
      const serverMsg = err.response.data?.detail || err.response.statusText;
      throw new Error(`Server error ${err.response.status}: ${serverMsg}`);
    }
    throw err;
  }
};
