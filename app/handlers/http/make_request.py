async def make_request(session, url: str, params=None) -> dict | None:
    """Makes HTTP requests with aiohttp."""

    params = params or {}

    async with session.get(url, params=params) as res:
        return await res.json()
