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
import api from "./api";

export const fetchEAAccounts = async () => {
  try {
    const res = await api.get("/ea-accounts/");
    return res.data;
  } catch (err) {
    throw err;
  }
};

export const updateEADailyLimit = async (id, daily_limit) => {
  try {
    await api.patch(`/ea-accounts/${id}/daily-limit`, { daily_limit });
  } catch (err) {
    throw err;
  }
};

export const fetchLiveAlerts = async () => {
  try {
    const res = await api.get("/alerts/live");
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
