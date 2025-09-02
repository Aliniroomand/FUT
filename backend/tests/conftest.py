import asyncio
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models as models
from app.database import Base

import httpx

from app.main import app as fastapi_app
from app.cache import _redis as _real_redis, get_redis
from app.database import get_db
from app.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the session.

    This is the pytest-asyncio recommended pattern when using asyncio in tests.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a new in-memory SQLite database and yield a SQLAlchemy Session.

    Tables are created from the project's models. Each test gets a fresh
    database (using the same in-memory URL but new connection/session), so
    tests are isolated.
    """
    # Use an in-memory SQLite database for fast, isolated tests
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables based on the project's models
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # drop all tables to ensure clean state (optional for in-memory)
        Base.metadata.drop_all(bind=engine)


class FakeRedis:
    """A tiny async-compatible fake Redis using a Python dict.

    Only implements a minimal async API needed by the app: get, set, close.
    Values are stored as-is; expiration (ex) is accepted but not enforced.
    """

    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ex=None):
        # ex (expiry) is accepted but not implemented in this simple fake
        self.store[key] = value

    async def close(self):
        # no real connection to close
        self.store.clear()


@pytest.fixture(scope="function")
async def fake_redis():
    """Provide a fresh FakeRedis instance per test."""
    r = FakeRedis()
    try:
        yield r
    finally:
        await r.close()


@pytest.fixture(scope="function")
async def async_client(db_session, fake_redis):
    """Provide an httpx AsyncClient configured to use the FastAPI app.

    This fixture overrides the application's dependencies so that:
    - get_db yields the test `db_session`.
    - get_redis returns the `fake_redis` instance.
    It also ensures the transfer worker is disabled during tests.
    """
    # Ensure worker is disabled in tests
    # (settings is a pydantic BaseSettings instance; setattr affects runtime only)
    setattr(settings, "START_WORKER", False)

    # Dependency override functions
    async def _get_redis_override():
        return fake_redis

    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    # Apply overrides on the FastAPI app using the real dependency callables
    fastapi_app.dependency_overrides[get_db] = _get_db_override
    fastapi_app.dependency_overrides[get_redis] = _get_redis_override

    async with httpx.AsyncClient(app=fastapi_app, base_url="http://testserver") as client:
        yield client

    # Clear overrides after test
    fastapi_app.dependency_overrides.clear()
