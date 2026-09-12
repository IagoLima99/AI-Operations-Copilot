"""Tests for the health endpoint."""

import pytest

from app.api.routes.health import health_check


@pytest.mark.asyncio
async def test_health_check():
    """Verify that the health endpoint reports its status."""
    assert await health_check() == {"status": "ok"}
