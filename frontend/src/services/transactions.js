import axios from "axios";

export const getTransactions = async (page, limit) => {
  const token = localStorage.getItem("access_token");
  const skip = (page - 1) * limit;
  const res = await axios.get(`/api/transactions?skip=${skip}&limit=${limit}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  console.log(res.data);
  return res.data;

};
