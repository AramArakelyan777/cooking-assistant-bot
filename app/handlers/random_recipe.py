from aiohttp import ClientError
from dotenv import dotenv_values
from http.make_request import make_request
from middlewares.logging_middleware import AsyncLoggingMiddleware


config = dotenv_values(".env")
logger = AsyncLoggingMiddleware()


async def get_random_recipe() -> dict:
    """Fetches and returns a random recipe using an API, handles possible errors."""

    try:
        recipe_api = config["RANDOM_RECIPE_API"]

        if recipe_api:
            random_recipe = await make_request(url=recipe_api)
        else:
            await logger.log(level="error", message="The recipe API is invalid.")
            return {}

        if random_recipe.get("meals") and isinstance(random_recipe["meals"], list) and len(random_recipe["meals"]) > 0:
            return random_recipe["meals"][0]
        else:
            await logger.log(level="error",
                             message="API returned no meals or invalid structure.")
            return {}

    except ClientError as e:
        await logger.log(level="error", message=f"Network error: {e}")
        return {}

    except KeyError as e:
        await logger.log(level="error", message=f"Missing configuration key: {e}")
        return {}

    except Exception as e:
        await logger.log(level="error", message=f"Unexpected error: {e}")
        return {}
