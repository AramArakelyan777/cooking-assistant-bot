from handlers.http.session_manager import session


async def make_request(url: str, params: dict = {}) -> dict:
    """
    Asynchronously makes an HTTP GET request to the specified URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (dict, optional): A dictionary of query parameters to include in the request. Defaults to an empty dictionary.

    Returns:
        dict: The JSON response from the server as a dictionary.

    Raises:
        aiohttp.ClientError: If an error occurs during the request.
        aiohttp.ClientResponseError: If the response contains an HTTP error status.
    """

    async with session.get(url=url, params=params) as res:
        return await res.json()
