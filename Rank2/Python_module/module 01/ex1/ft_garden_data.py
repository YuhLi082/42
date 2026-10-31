class Plant:
    def __init__(self, name: str, height: int, age: int):
        """
        Initialize a Plant object with given attributes.
        """
        self.name = name
        self.height = height
        self.age = age

    def show_info(self):
        """
        Display the plant's information in a formatted string.
        Prints name, height, and age of the plant.
        """
        print(f"{self.name}: {self.height}cm, {self.age} days old")


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    rose = Plant("Rose", 25, 30)
    sunflower = Plant("Sunflower", 80, 45)
    cactus = Plant("Cactus", 15, 120)
    plants = [rose, sunflower, cactus]
    for i in plants:
        i.show_info()
