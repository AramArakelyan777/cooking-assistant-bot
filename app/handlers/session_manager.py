import aiohttp


session = None


async def init_session():
    """Creates a global aiohttp client session for multiple requests.
    """

    global session
    session = aiohttp.ClientSession()


async def close_session():
    """Closes the aiohttp client session.
    """

    global session
    if session:
        await session.close()
