def validate_ingredients(ingredients: str) -> str:
    valid_ingredients = ["fire", "water", "earth", "air"]
    if any(elem in ingredients for elem in valid_ingredients):
        return f"{ingredients} - VALID"
    else:
        return f"{ingredients} - INVALID"
