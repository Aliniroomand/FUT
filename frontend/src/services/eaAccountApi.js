import api from "./api";


export const addEAAccount = async (account) => {
  try {
    const res = await api.post("/ea-accounts/", account);
    return res.data;
  } catch (err) {
    throw err;
  }
};

export const deleteEAAccount = async (id) => {
  try {
    await api.delete(`/ea-accounts/${id}`);
  } catch (err) {
    throw err;
  }
};

export const fetchEAAccounts = async () => {
  try {
    const res = await api.get("/ea-accounts/");
    return res.data;
  } catch (err) {
    throw err;
  }
};
export const updateEADailyLimit = async (id, dailyLimit) => {
  try {
    const response = await api.patch(`/ea-accounts/${id}/daily-limit`, { daily_limit: dailyLimit });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message || "خطای ناشناخته رخ داده است";
  }
};

export const fetchLiveAlerts = async () => {
  try {
    const res = await api.get("/admin/alerts");
    return res.data;
  } catch (err) {
    throw err;
  }
};

export const fetchPendingTransactions = async () => {
  try {
    const res = await api.get("/alerts/pending-transactions");
    return res.data;
  } catch (err) {
    throw err;
  }
};

export const resolveAlert = async (alertId) => {
  try {
    await api.post(`/alerts/resolve/${alertId}`);
  } catch (err) {
    throw err;
  }
};
