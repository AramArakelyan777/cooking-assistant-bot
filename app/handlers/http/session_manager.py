from aiohttp import ClientSession


_session = None


async def init_session():
    """Creates an aiohttp session."""

    global _session
    _session = ClientSession()


async def close_session():
    """Closes the aiohttp session."""

    global _session
    if _session:
        await _session.close()
        _session = None


def get_session() -> ClientSession | None:
    """Returns the active session or None if not initialized."""

    return _session
