def healing_potion() -> str:
    from .elements import create_fire, create_water
    fire_result = create_fire()
    water_result = create_water()
    return f"Healing potion brewed with {fire_result} and {water_result}"


def strength_potion() -> str:
    from .elements import create_fire, create_earth
    earth_result = create_earth()
    fire_result = create_fire()
    return f"Strength potion brewed with {earth_result} and {fire_result}"


def invisibility_potion() -> str:
    from .elements import create_air, create_water
    air_result = create_air()
    water_result = create_water()
    return f"Invisibility potion brewed with {air_result} and {water_result}"


def wisdom_potion() -> str:
    from .elements import create_air, create_water, create_fire, create_earth
    fire = create_fire()
    water = create_water()
    earth = create_earth()
    air = create_air()
    return (
        f"Wisdom potion brewed with all elements: "
        f"{fire}, {water}, {earth}, {air}"
    )
