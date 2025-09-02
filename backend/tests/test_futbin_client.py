import asyncio
import json
import pytest
import httpx
from datetime import datetime
from types import SimpleNamespace

import app.services.futbin_client as futmod

# a tiny async redis-like stub
class AsyncRedisStub:
    def __init__(self):
        self._d = {}
    async def get(self, k):
        return self._d.get(k)
    async def set(self, k, v, ex=None):
        self._d[k] = v
    async def setnx(self, k, v):
        if k in self._d:
            return False
        self._d[k] = v
        return True
    async def expire(self, k, s):
        # no-op for stub
        return True
    async def delete(self, k):
        self._d.pop(k, None)
    # lock shim (context manager)
    def lock(self, name, timeout=None):
        class DummyLock:
            async def __aenter__(self):
                return True
            async def __aexit__(self, exc_type, exc, tb):
                return False
        return DummyLock()

@pytest.fixture(autouse=True)
def patch_get_redis(monkeypatch):
    stub = AsyncRedisStub()
    async def _get_redis():
        return stub
    monkeypatch.setattr("app.cache.get_redis", _get_redis)
    return stub

@pytest.mark.asyncio
async def test_json_endpoint_success(monkeypatch, patch_get_redis):
    # mock httpx AsyncClient.get to return JSON payload
    async def fake_get(self, url, timeout):
        class R:
            status_code = 200
            headers = {"content-type": "application/json"}
            def json(self):
                return {"prices": {"pc": { "123": 5555}}}
            text = '{"prices":{"pc":{"123":5555}}}'
            def raise_for_status(self):
                return None
        return R()
    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)
    res = await futmod.get_player_price("123", "pc", ttl=1)
    assert res["price"] == 5555

@pytest.mark.asyncio
async def test_html_parse_success(monkeypatch, patch_get_redis):
    # return a HTML that contains price near 'pc' token
    async def fake_get(self, url, timeout):
        class R:
            status_code = 200
            headers = {"content-type": "text/html"}
            text = '<html><body><span class="pc">12,345</span></body></html>'
            def raise_for_status(self): pass
        return R()
    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)
    res = await futmod.get_player_price("123", "pc", ttl=1)
    assert res["price"] == 12345

@pytest.mark.asyncio
async def test_captcha_triggers_alert_and_negative(monkeypatch, patch_get_redis):
    # html contains 'captcha'
    async def fake_get(self, url, timeout):
        class R:
            status_code = 200
            headers = {"content-type": "text/html"}
            text = '<html><body>please verify you are human (captcha)</body></html>'
            def raise_for_status(self): pass
        return R()
    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)

    # patch create_alert to capture calls
    called = {}
    async def fake_create_alert(player_id, platform, reason, sample_html=None):
        called["called"] = True
        called["reason"] = reason
    monkeypatch.setattr("app.services.futbin_client._create_alert", fake_create_alert)

    redis_stub = patch_get_redis
    res = await futmod.get_player_price("999", "pc", ttl=1)
    assert res["price"] is None
    assert called.get("called") is True
    # negative block key should be set in redis stub
    neg_key = f"futbin:negative:999:pc"
    assert await redis_stub.get(neg_key) is not None
