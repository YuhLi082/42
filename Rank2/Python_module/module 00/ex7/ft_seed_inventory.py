def ft_seed_inventory(seed_type: str, quantity: int, unit: str):
    seed_type = seed_type.capitalize()
    if (unit == "packets"):
        unit_text = f"{quantity} packets available"
    elif (unit == "grams"):
        unit_text = f"{quantity} grams total"
    elif (unit == "area"):
        unit_text = f"covers {quantity} square meters"
    else:
        unit_text = "Unknown unit type"
    print(f"{seed_type} seeds: {unit_text}")
