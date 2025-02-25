import pytest

from app.config import settings


@pytest.mark.asyncio
async def test_env_settings():
    assert settings.MODE == "TEST"
    assert settings.LOG_LEVEL == "DEBUG"
