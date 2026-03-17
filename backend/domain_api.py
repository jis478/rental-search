import time
import httpx
from config import DOMAIN_CLIENT_ID, DOMAIN_CLIENT_SECRET

TOKEN_URL = "https://auth.domain.com.au/v1/connect/token"
SEARCH_URL = "https://api.domain.com.au/v1/listings/residential/_search"

_cached_token: str | None = None
_token_expiry: float = 0


async def _get_token(client: httpx.AsyncClient) -> str:
    global _cached_token, _token_expiry

    if _cached_token and time.time() < _token_expiry:
        return _cached_token

    resp = await client.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": DOMAIN_CLIENT_ID,
            "client_secret": DOMAIN_CLIENT_SECRET,
            "scope": "api_listings_read",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    resp.raise_for_status()
    data = resp.json()
    _cached_token = data["access_token"]
    _token_expiry = time.time() + data.get("expires_in", 3600) - 60
    return _cached_token


async def search_listings(search_params: dict) -> list[dict]:
    async with httpx.AsyncClient(timeout=30) as client:
        token = await _get_token(client)
        resp = await client.post(
            SEARCH_URL,
            json=search_params,
            headers={"Authorization": f"Bearer {token}"},
        )
        resp.raise_for_status()
        return resp.json()
