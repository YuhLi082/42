class Plant:
    """Base class for all plants with common attributes."""
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age


class Flower(Plant):
    """Flowering plant with color and blooming capability."""
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color

    def bloom(self):
        """Print blooming message."""
        print(f"{self.name} is blooming beautifully!")


class Tree(Plant):
    """Tree with trunk diameter and shade calculation."""
    def __init__(self, name, height, age, trunk_diameter):
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self):
        """Calculate and print shade area."""
        shade = self.trunk_diameter * 1.56
        print(f"{self.name} provides {int(shade)} square meters of shade")


class Vegetable(Plant):
    """Vegetable plant with harvest season and nutrition info."""
    def __init__(self, name, height, age, harvest_season, nutritional_value):
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value


def main():
    print("=== Garden Plant Types ===")

    flowers = [
        Flower("Rose", 25, 30, "red"),
        # Flower("Tulip", 20, 25, "yellow")
    ]

    trees = [
        Tree("Oak", 500, 1825, 50),
        # Tree("Pine", 300, 730, 30)
    ]

    vegetables = [
        Vegetable("Tomato", 80, 90, "summer", "vitamin C"),
        # Vegetable("Cabbage", 45, 60, "autumn", "vitamin A")
    ]

    for flower in flowers:
        print(f"{flower.name} (Flower): {flower.height}cm, "
              f"{flower.age} days, {flower.color} color")
        flower.bloom()
        print()

    for tree in trees:
        print(f"{tree.name} (Tree): {tree.height}cm, "
              f"{tree.age} days, {tree.trunk_diameter}cm diameter")
        tree.produce_shade()
        print()

    for vegetable in vegetables:
        print(f"{vegetable.name} (Vegetable): {vegetable.height}cm, "
              f"{vegetable.age} days, {vegetable.harvest_season} harvest")
        print(f"{vegetable.name} is rich in {vegetable.nutritional_value}")


if __name__ == "__main__":
    main()
