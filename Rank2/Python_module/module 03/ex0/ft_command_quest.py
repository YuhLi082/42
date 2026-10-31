import sys
"""Import sys module to access command-line arguments via sys.argv"""


def main() -> None:
    """
    Main function that processes and displays command-line arguments.
    Prints different outputs based on whether arguments were provided.
    """
    print("=== Command Quest ===")

    num = len(sys.argv)
    if num == 1:
        print("No arguments provided!")
        print(f"Program name: {sys.argv[0]}")
        print(f"Total arguments: {num}")
    else:
        print(f"Program name: {sys.argv[0]}")
        print(f"Arguments received: {num - 1}")
        for i in range(1, num):
            print(f"Argument {i}: {sys.argv[i]}")
        print(f"Total arguments: {num}")


if __name__ == "__main__":
    main()
