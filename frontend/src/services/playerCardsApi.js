import api from "@/services/api";

// ================== Player Cards APIs ==================
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

// delete: keep previous signature but backend supports replacement & force
export const deletePlayerCard = async (
  id,
  replacementId = null,
  force = false
) => {
  const params = {};
  if (replacementId) params.replacement_id = replacementId;
  if (force) params.force = true;
  const response = await api.delete(`/player-cards/${id}`, { params });
  return response.data;
};

// new: get dependencies for a given card
export const getPlayerDependencies = async (id) => {
  const response = await api.get(`/player-cards/dependencies/${id}`);
  return response.data;
};


// existing futbin/trade functions...
export async function fetchPriceForCard(id, platform = "pc") {
  return (
    await api.post(`/player-cards/${id}/fetch-price`, null, {
      params: { platform },
    })
  ).data;
}

export async function getTradeRange(id, methodId, platform = "pc") {
  return (
    await api.get(`/player-cards/${id}/trade-range`, {
      params: { method_id: methodId, platform },
    })
  ).data;
}
