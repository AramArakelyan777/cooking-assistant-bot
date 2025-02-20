class Structurize:
    @staticmethod
    def structurized_recipe(recipe: dict) -> str:
        """Returns a structurized and detailed version of the meal."""

        return f"*{recipe.get('strMeal', 'Unknown Meal')}*\n\nCategory: {recipe.get('strCategory', 'N/A')}\nTags: {recipe.get('strTags', 'N/A')}\nCountry of origin: {recipe.get('strArea', 'N/A')}\n\nHow to cook this meal:\n\n{recipe.get('strInstructions', 'No instructions provided.')}"
