import httpx
from bot.config import settings

class APIClient:
    def __init__(self, token: str | None = None):
        self.base_url = settings.backend_url
        self.token = token
        self.client = httpx.AsyncClient(trust_env=True)

    def _headers(self) -> dict[str, str]:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def get(self, path: str) -> dict:
        url = f"{self.base_url}/{path}"
        response = await self.client.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    async def post(self, path: str, json: dict | None = None) -> dict:
        url = f"{self.base_url}/{path}"
        response = await self.client.post(url, json=json, headers=self._headers())
        response.raise_for_status()
        return response.json()

    async def aclose(self) -> None:
        await self.client.aclose()