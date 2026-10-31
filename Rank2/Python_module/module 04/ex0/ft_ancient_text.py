def ft_ancient_text() -> None:
    """
    Recover ancient data fragments from storage vault.
    Displays recovered data or error if vault not found.
    """
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")

    file_name = "ancient_fragment.txt"
    print(f"Accessing Storage Vault: {file_name}")
    try:
        f = open(file_name, "r")
        print("Connection established...\n")
        print("RECOVERED DATA:")
        print(f.read())
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")
    else:
        f.close()
        print("\nData recovery complete. Storage unit disconnected.")


if __name__ == "__main__":
    ft_ancient_text()
