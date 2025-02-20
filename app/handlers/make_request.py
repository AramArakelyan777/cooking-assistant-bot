import aiohttp


async def make_request(url, params={}):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as res:
            return await res.json()
