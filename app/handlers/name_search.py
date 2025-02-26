from aiohttp import ClientError
from dotenv import dotenv_values
from handlers.http.make_request import make_request
from middlewares.logging_middleware import AsyncLoggingMiddleware
from handlers.http.session_manager import get_session


config = dotenv_values(".env")
logger = AsyncLoggingMiddleware()


async def get_recipe_by_name(name: str) -> list | None:
    """Fetches and returns recipes by their name using an API, handles possible errors."""

    try:
        recipe_api = config.get("NAME_SEARCH_RECIPE_API")

        if recipe_api:
            session = get_session()
            if session:
                random_recipe = await make_request(session, url=recipe_api + name)
            else:
                await logger.log(level="error", message="Session is not initialized.")
                return None
        else:
            await logger.log(level="error", message="The recipe API is invalid.")
            return None

        if random_recipe and random_recipe.get("meals"):
            return random_recipe["meals"]
        else:
            await logger.log(level="error",
                             message="API returned no meals or invalid structure.")
            return None

    except ClientError as e:
        await logger.log(level="error", message=f"Network error: {e}")
        return None

    except KeyError as e:
        await logger.log(level="error", message=f"Missing configuration key: {e}")
        return None

    except Exception as e:
        await logger.log(level="error", message=f"Unexpected error: {e}")
        return None
