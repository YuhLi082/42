def crisis_handler(filename: str) -> None:
    """
    Handle archive access attempts and manage errors gracefully.
    Catches FileNotFoundError, PermissionError and other exceptions.
    """
    try:
        with open(filename, "r") as f:
            content = f.read()
            print(f"ROUTINE ACCESS: Attempting access to '{filename}'...")
            print(f"SUCCESS: Archive recovered - ``{content}''")
            print("STATUS: Normal operations resumed")
    except FileNotFoundError:
        print(f"CRISIS ALERT: Attempting access to '{filename}'...")
        print("RESPONSE: Archive not found in storage matrix")
        print("STATUS: Crisis handled, system stable")
    except PermissionError:
        print(f"CRISIS ALERT: Attempting access to '{filename}'...")
        print("RESPONSE: Security protocols deny access")
        print("STATUS: Crisis handled, security maintained")
    except Exception as e:
        print(f"CRISIS ALERT: Attempting access to '{filename}'...")
        print(f"RESPONSE: Unexpected anomaly - {e}")
        print("STATUS: Crisis handled, anomaly contained")


def main() -> None:
    """
    Run crisis response simulations on multiple archive files.
    Tests missing, restricted and standard archive access scenarios.
    """
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")
    crisis_handler("lost_archive.txt")
    print()
    crisis_handler("classified_vault.txt")
    print()
    crisis_handler("standard_archive.txt")
    print()
    print("All crisis scenarios handled successfully. Archives secure.")


if __name__ == "__main__":
    main()
