class Plant:
    """
    Initialize a Plant object with given attributes.
    """
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def show_info(self):
        """
        Display the plant's information in a formatted string.
        Prints name, height, and age of the plant.
        """
        print(f"Created: {self.name} ({self.height}cm, {self.age} days)")


def main():
    """
    Main function demonstrating plant creation and display.
    Creates multiple Plant objects from data and displays their information.
    """
    plant_data = [
        ("Rose", 25, 30),
        ("Oak", 200, 365),
        ("Cactus", 5, 90),
        ("Sunflower", 80, 45),
        ("Fern", 15, 120),
    ]
    plants = [Plant(name, height, age) for name, height, age in plant_data]

    print("=== Plant Factory Output ===")
    for i in plants:
        i.show_info()

    print(f"Total plants created: {len(plants)}")


if __name__ == "__main__":
    main()
