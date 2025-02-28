class Structurize:
    @staticmethod
    def structurized_recipe(recipe: dict) -> str:
        """Returns a structurized and detailed version of the meal."""

        ingredients = ""
        i = 1

        while True:
            ingredient = (recipe.get(f"strIngredient{i}") or "").strip()
            measure = (recipe.get(f"strMeasure{i}") or "").strip()

            if not ingredient and not measure:
                break

            if ingredient:
                ingredients += ingredient
            if measure:
                ingredients += f": {measure}"
            ingredients += "\n"

            i += 1

        meal_name = recipe.get("strMeal", "Unknown Meal").upper()
        category = recipe.get("strCategory", "N/A")
        tags = recipe.get("strTags", "N/A")
        country = recipe.get("strArea", "N/A")
        instructions = recipe.get(
            "strInstructions", "No instructions provided.")

        return (
            f"*{meal_name}*\n\n\n"
            f"Category: {category}\n"
            f"Tags: {tags}\n"
            f"Country of origin: {country}\n\n"
            f"Ingredients:\n"
            f"{ingredients if ingredients else 'No ingredients available.'}\n"
            f"How to cook this meal:\n"
            f"{instructions}"
        )
