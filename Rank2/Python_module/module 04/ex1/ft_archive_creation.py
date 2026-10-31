def ft_archive_creation() -> None:
    """
    Create a new archive and inscribe data entries.
    """
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
    file_name = "new_discovery.txt"
    text = ("[ENTRY 001] New quantum algorithm discovered\n"
            "[ENTRY 002] Efficiency increased by 347%\n"
            "[ENTRY 003] Archived by Data Archivist trainee\n")
    print(f"Initializing new storage unit: {file_name}")

    try:
        f = open(file_name, "w")
        print("Storage unit created successfully...\n")
        print("Inscribing preservation data...")
        f.write(text)
        print(text)
    except Exception as e:
        print(f"Error: {e}")
    else:
        f.close()
        print("Data inscription complete. Storage unit sealed.")
        print(f"Archive '{file_name}' ready for long-term preservation.")


if __name__ == "__main__":
    ft_archive_creation()
