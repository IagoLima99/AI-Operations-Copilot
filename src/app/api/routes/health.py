"""Health-check API route."""

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health_check():
    """Return the API health status."""
    return {"status": "ok"}
