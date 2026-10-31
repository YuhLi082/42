import alchemy
import alchemy.elements


def ft_sacred_scroll() -> None:
    print("=== Sacred Scroll Mastery ===")
    print()

    print("Testing direct module access:")
    try:
        e = alchemy.elements.create_fire()
        print(f"alchemy.elements.create_fire(): {e}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        e = alchemy.elements.create_water()
        print(f"alchemy.elements.create_water(): {e}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        e = alchemy.elements.create_earth()
        print(f"alchemy.elements.create_earth(): {e}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        e = alchemy.elements.create_air()
        print(f"alchemy.elements.create_air(): {e}")
    except AttributeError:
        print("AttributeError - not exposed")
    print()

    print("\nTesting package-level access (controlled by __init__.py):")
    try:
        print(f"alchemy.create_fire(): {alchemy.create_fire()}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print(f"alchemy.create_water(): {alchemy.create_water()}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print(f"alchemy.create_earth(): {alchemy.create_earth()}")
    except AttributeError:
        print("alchemy.create_earth(): AttributeError - not exposed")
    try:
        print(f"alchemy.create_air(): {alchemy.create_air()}")
    except AttributeError:
        print("alchemy.create_air(): AttributeError - not exposed")
    print()

    print("Package metadata:")
    print(f"Version: {alchemy.__version__}")
    print(f"Author: {alchemy.__author__}")


if __name__ == "__main__":
    ft_sacred_scroll()
