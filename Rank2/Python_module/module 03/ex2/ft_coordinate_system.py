import math


def calculate_distance(p1: tuple, p2: tuple) -> float:
    """
    Calculate Euclidean distance between two 3D points
    Formula: √((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²)
    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2), 2)


def parse_coordinates(enter_str: str) -> tuple | None:
    """
    Parse a string like "x,y,z" into a tuple (x, y, z)
    """
    try:
        parts = enter_str.split(",")
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        return (x, y, z)
    except ValueError as e:
        print(f"Error parsing coordinates: {e}")
        print(f"Error details - Type: ValueError, Args: {e.args}")
        return None


def main() -> None:
    print("=== Game Coordinate System ===\n")
    origen = (0, 0, 0)
    point1 = (10, 20, 5)
    distance = calculate_distance(point1, origen)
    print(f"Position created: {point1}")
    print(f"Distance between {origen} and {point1}: {distance}\n")

    coord_str = "3,4,0"
    print(f'Parsing coordinates: "{coord_str}"')
    parsed_position = parse_coordinates(coord_str)
    print(f"Parsed position: {parsed_position}")
    distance2 = calculate_distance(origen, parsed_position)
    print(f"Distance between {origen} and {parsed_position}: {distance2}\n")

    invalid_str = "abc,def,ghi"
    print(f'Parsing invalid coordinates: "{invalid_str}"')
    parse_coordinates(invalid_str)
    print()

    print("Unpacking demonstration:")
    x, y, z = parsed_position
    print(f"Player at x={x}, y={y}, z={z}")
    print(f"Coordinates: X={x}, Y={y}, Z={z}")


if __name__ == "__main__":
    main()
