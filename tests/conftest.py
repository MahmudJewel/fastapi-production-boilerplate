import os
import sys
from pathlib import Path
from uuid import uuid4

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

BASE_DB_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./integration_test.db")
USE_SEPARATE_DB = os.getenv("TEST_DB_ISOLATED", "0") == "1"
DB_SUFFIX = os.getenv("TEST_DB_RUN_SUFFIX", uuid4().hex[:8])


def resolve_test_db_url() -> str:
    if not USE_SEPARATE_DB:
        return BASE_DB_URL

    if BASE_DB_URL.startswith("sqlite:///"):
        db_path = BASE_DB_URL.replace("sqlite:///", "")
        base = Path(db_path)
        isolated_name = f"{base.stem}_{DB_SUFFIX}{base.suffix or '.db'}"
        isolated_path = base.with_name(isolated_name)
        return f"sqlite:///{isolated_path}"

    return BASE_DB_URL


TEST_DB_URL = resolve_test_db_url()

from app.core.dependencies import get_db
from app.main import create_app
from app.models.common import Base
from app.models.user import User


connect_args = {"check_same_thread": False} if TEST_DB_URL.startswith("sqlite") else {}
engine = create_engine(TEST_DB_URL, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest_asyncio.fixture(scope="session")
async def client():
    Base.metadata.create_all(bind=engine)
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="session")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
