#!/usr/bin/env python3
class SecurePlant:
    def __init__(self, name, height, age):
        """Initialize plant with validation"""
        self.name = name
        self._height = 0
        self._age = 0

        print(f"Plant created: {self.name}")
        self.set_height(height)
        self.set_age(age)

    """Set height if non-negative"""
    def set_height(self, new_height):
        if new_height >= 0:
            self._height = new_height
            print(f"Height updated: {new_height}cm [OK]")
            return True
        else:
            print(f"Invalid operation attempted: "
                  f"height {new_height}cm [REJECTED]")
            print("Security: Negative height rejected")
            return False

    """Set age if non-negative"""
    def set_age(self, new_age):
        if new_age >= 0:
            self._age = new_age
            print(f"Age updated: {new_age} days [OK]")
            return True
        else:
            print(f"Invalid operation attempted: "
                  f"age {new_age} days [REJECTED]")
            print("Security: Negative age rejected")
            return False

    def get_height(self):
        """Get current height"""
        return self._height

    def get_age(self):
        """Get current age"""
        return self._age

    def show_info(self):
        """Display current plant status"""
        print(f"Current plant: "
              f"{self.name} ({self._height}cm, {self._age} days)")


def main():
    """Test the security system"""
    print("=== Garden Security System ===")

    rose = SecurePlant("Rose", 25, 30)
    print()

    rose.set_height(-5)
    print()

    rose.show_info()


if __name__ == "__main__":
    main()
