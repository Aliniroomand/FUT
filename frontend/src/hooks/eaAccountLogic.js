import {
  fetchEAAccounts,
  updateEADailyLimit,
  fetchLiveAlerts,
  fetchPendingTransactions,
  resolveAlert,
} from "../services/eaAccountApi";

export const useEAAccountLogic = () => {
  const fetchAccounts = async (setAccounts, setError) => {
    try {
      const data = await fetchEAAccounts();
      setAccounts(data);
    } catch (err) {
      setError && setError(err);
    }
  };

  const fetchAlerts = async (setAlerts, setError) => {
    try {
      const data = await fetchLiveAlerts();
      setAlerts(data);
    } catch (err) {
      setError && setError(err);
    }
  };

  const fetchPendingTxs = async (setPendingTxs, setError) => {
    try {
      const data = await fetchPendingTransactions();
      setPendingTxs(data);
    } catch (err) {
      setError && setError(err);
    }
  };

  const handleEdit = (setEditId, setEditLimit, id, limit) => {
    setEditId(id);
    setEditLimit(limit);
  };

  const handleSave = async (id, editLimit, setEditId, setLoading, fetchAccounts, setError) => {
    setLoading(true);
    try {
      await updateEADailyLimit(id, editLimit);
      setEditId(null);
      fetchAccounts();
    } catch (err) {
      setError && setError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleResolveAlert = async (alertId, fetchAlerts, fetchAccounts, setError) => {
    try {
      await resolveAlert(alertId);
      fetchAlerts();
      fetchAccounts();
    } catch (err) {
      setError && setError(err);
    }
  };

  return {
    fetchAccounts,
    fetchAlerts,
    fetchPendingTxs,
    handleEdit,
    handleSave,
    handleResolveAlert,
  };
};
