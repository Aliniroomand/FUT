import api from "../api";


export const fetchUnresolvedAlerts = async () => {
  try {
    const res = await api.get("/alerts/live");
    return res.data;
  } catch (err) {
    throw err;
  }
};

export const fetchResolvedAlerts = async () => {
  try {
    const res = await api.get("/alerts/resolved");
    return res.data;
  } catch (err) {
    throw err;
  }
};


  export const resolveAlert = async (alertId) => {
  try {
    await api.post(`/alerts/${alertId}/resolve`);
  } catch (err) {
    throw err;
  }
};
