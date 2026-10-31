class Plant:
    """Base class for all plants in the garden system.
    Represents a generic plant with basic attributes and behaviors."""
    def __init__(self, name, height):
        self.name = name
        self.height = height
        self.type_id = 1

    def grow(self, amount=1):
        """
        Instance method: Increase plant height by specified amount.
        Prints growth confirmation message.
        """
        self.height += amount
        print(f"{self.name} grew {amount}cm")

    def __str__(self):
        """
        String representation of the plant for display purposes.
        Returns formatted string with plant name and height.
        """
        return f"{self.name}: {self.height}cm"


class FloweringPlant(Plant):
    """
    Subclass of Plant representing flowering plants.
    Inherits basic plant attributes and adds flower-specific properties.
    """
    def __init__(self, name, height, color, blooming=True):
        super().__init__(name, height)
        self.color = color
        self.blooming = blooming
        self.type_id = 2

    def __str__(self):
        """
        Overrides parent's __str__ method to include flower information.
        Returns formatted string with plant details and blooming status.
        """
        status = "blooming" if self.blooming else "not blooming"
        return (f"{self.name}: {self.height}cm, "
                f"{self.color} flowers ({status})")


class PrizeFlower(FloweringPlant):
    """
    Subclass of FloweringPlant representing prize-winning flowers.
    Inherits flowering plant attributes and adds prize-specific properties.
    """
    def __init__(self, name, height, color, points, blooming=True):
        super().__init__(name, height, color, blooming)
        self.points = points
        self.type_id = 3

    def __str__(self):
        """
        Extends parent's string representation to include prize points.
        Returns formatted string with all plant details and prize information.
        """
        base_str = super().__str__()
        return (f"{base_str}, Prize points: {self.points}")


class Garden:
    """
    Represents an individual garden belonging to an owner.
    Manages collection of plants and tracks garden statistics.
    """
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.plants = []
        self.total_growth = 0

    def add_plant(self, plant):
        """
        Instance method: Add a plant to the garden.
        Appends plant to internal list and prints confirmation.
        Returns new total number of plants in garden.
        """
        self.plants.append(plant)
        print(f"Added {plant.name} to {self.owner_name}'s garden")
        return len(self.plants)

    def grow_all(self, amount=1):
        """
        Instance method: Make all plants in garden grow by specified amount.
        Calls grow() on each plant and updates total growth tracking.
        """
        print()
        print(f"{self.owner_name} is helping all plants grow...")
        for plant in self.plants:
            plant.grow(amount)
            self.total_growth += amount

    def get_stats(self):
        """
        Instance method: Calculate comprehensive garden statistics.
        Uses type_id for plant classification (avoiding isinstance).
        Returns dictionary with various statistical metrics.
        """
        stats = {
            'total_plants': len(self.plants),
            'regular_plants': 0,
            'flowering_plants': 0,
            'prize_flowers': 0,
            'total_height': 0,
        }
        for plant in self.plants:
            stats['total_height'] += plant.height
            if plant.type_id == 3:
                stats['prize_flowers'] += 1
            elif plant.type_id == 2:
                stats['flowering_plants'] += 1
            else:
                stats['regular_plants'] += 1
        return stats

    def display_report(self):
        """
        Instance method: Display comprehensive garden report.
        Shows all plants with details and statistical summary.
        """
        print(f"\n=== {self.owner_name}'s Garden Report ===")
        print("Plants in garden:")
        for plant in self.plants:
            print(f"- {plant}")
        stats = self.get_stats()
        print(f"\nPlants added: {stats['total_plants']}, "
              f"Total growth: {self.total_growth}cm")
        print(f"Plant types: {stats['regular_plants']} regular, "
              f"{stats['flowering_plants']} flowering, "
              f"{stats['prize_flowers']} prize flowers")


class GardenManager:
    """
    Manages multiple gardens and provides analytical capabilities.
    Contains nested helper class for statistical calculations.
    """
    class GardenStats:
        """
        Nested helper class dedicated to statistical calculations.
        Contains both static methods and class methods for analytics.
        """

        @staticmethod
        def calculate_garden_score(garden):
            """
            Static method: Calculate numerical score for a garden.
            Returns integer score representing garden quality.
            """
            stats = garden.get_stats()
            score = (stats['total_height'] +
                     stats['flowering_plants'] * 10 +
                     stats['prize_flowers'] * 30)
            return score

        @classmethod
        def compare_gardens(cls, garden1, garden2):
            """
            Class method: Compare two gardens by their calculated scores.
            Uses cls parameter to call the static
            calculate_garden_score method.
            Returns dictionary with both garden names and their scores.
            """
            score1 = cls.calculate_garden_score(garden1)
            score2 = cls.calculate_garden_score(garden2)
            return {garden1.owner_name: score1,
                    garden2.owner_name: score2}

    def __init__(self):
        """
        Initialize a new GardenManager instance.
        Creates empty dictionary for gardens and sets counter to zero.
        """
        self.gardens = {}
        self.total_gardens = 0

    def add_garden(self, garden):
        """
        Instance method: Add a garden to the manager's collection.
        Stores garden in dictionary with owner name as key.
        Increments the total gardens counter.
        """
        self.gardens[garden.owner_name] = garden
        self.total_gardens += 1

    @classmethod
    def create_garden_network(cls):
        """
        Class method: Factory method to create a GardenManager instance.
        Demonstrates class-level method that works on the class itself.
        Returns new instance of GardenManager.
        """
        return cls()

    def validate_all_heights(self):
        """
        Instance method: Validate that all plants have non-negative heights.
        Demonstrates data validation across all managed gardens.
        Returns True if all heights are valid, False otherwise.
        """
        for garden in self.gardens.values():
            for plant in garden.plants:
                if plant.height < 0:
                    return False
        return True


def main():
    """
    Main demonstration function showing all system features.
    Creates sample data, demonstrates inheritance, nested classes,
    and different types of methods (instance, class, static).
    Output matches the example provided in the exercise requirements.
    """
    print("=== Garden Management System Demo ===")
    print()
    manager = GardenManager.create_garden_network()

    alice_garden = Garden("Alice")
    manager.add_garden(alice_garden)

    alice_garden.add_plant(Plant("Oak Tree", 100))
    alice_garden.add_plant(FloweringPlant("Rose", 25, "red"))
    alice_garden.add_plant(PrizeFlower("Sunflower", 50, "yellow", 10))

    alice_garden.grow_all()

    alice_garden.display_report()
    print()
    print(f"Height validation test: {manager.validate_all_heights()}")

    bob_garden = Garden("Bob")
    manager.add_garden(bob_garden)
    bob_garden.add_plant(Plant("Maple Tree", 72))
    bob_garden.add_plant(FloweringPlant("Tulip", 10, "pink"))

    scores = GardenManager.GardenStats.compare_gardens(alice_garden,
                                                       bob_garden)
    print(f"Garden scores - Alice: {scores['Alice']}, "
          f"Bob: {scores['Bob']}")

    print(f"Total gardens managed: {manager.total_gardens}")


if __name__ == "__main__":
    main()
