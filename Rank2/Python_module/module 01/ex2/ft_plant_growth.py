class Plant:
    """
    Initialize a new Plant object.
    """
    def __init__(self, name, height, age1):
        self.name = name
        self.height = height
        self.age1 = age1

    def grow(self):
        """
        Simulate plant growth by increasing height by 1cm.
        This method modifies the plant's height attribute directly.
        """
        self.height += 1

    def age(self):
        """
        Simulate aging by increasing age by 1 day.
        This method modifies the plant's age attribute directly.
        """
        self.age1 += 1

    def get_info(self):
        """
        Display plant information in a formatted string.
        Prints plant name, current height, and current age.
        """
        print(f"{self.name}: {self.height}cm, {self.age1} days old")


if __name__ == "__main__":
    rose = Plant("Rose", 25, 30)
    sunflower = Plant("Sunflower", 80, 45)
    cactus = Plant("Cactus", 15, 120)

    plants = [rose, sunflower, cactus]

    print("=== Day 1 ===")
    for i in plants:
        i.get_info()

    start_growth = rose.height

    for _ in range(7):
        for i in plants:
            i.grow()
            i.age()

    print("=== Day 7 ===")
    for i in plants:
        i.get_info()

    growth = rose.height - start_growth
    print(f"Growth this week: +{growth}cm")
