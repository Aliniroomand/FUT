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


// Player Cards APIs
export const getPlayerCards = async () => {
  const response = await api.get("/player-cards/");
  return response.data;
};

export const createPlayerCard = async (data) => {
  const response = await api.post("/player-cards/", data);
  return response.data;
};

export const getPlayerCard = async (id) => {
  const response = await api.get(`/player-cards/${id}`);
  return response.data;
};

export const updatePlayerCard = async (id, data) => {
  const response = await api.put(`/player-cards/${id}`, data);
  return response.data;
};

export const deletePlayerCard = async (id) => {
  const response = await api.delete(`/player-cards/${id}`);
  return response.data;
};

// Authentication APIs

// بررسی اینکه بازیکن در بازه‌ای استفاده شده یا نه
export async function checkPlayerUsage(playerId) {
  const response = await fetch(`/api/player-cards/${playerId}/usage`);
  if (!response.ok) throw new Error("Failed to check player usage");
  return await response.json();
}

// حذف همه بازه‌هایی که بازیکن primary_card آن‌ها بوده
export async function deleteRangesWithPrimaryCard(playerId) {
  const response = await fetch(`/api/card-ranges/by-primary-card/${playerId}`, {
    method: "DELETE",
  });
  if (!response.ok) throw new Error("Failed to delete related ranges");
  return await response.json();
}
