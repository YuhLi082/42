def ft_vault_security() -> None:
    """
    Recover ancient data from storage vault.
    Displays recovered data or error if vault not found.
    """
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")
    try:
        print("Initiating secure vault access...")
        print("Vault connection established with failsafe protocols\n")
        with open("classified_data.txt") as f:
            print("SECURE EXTRACTION:")
            print(f.read())
            print()

        with open("security_protocols.txt", "w") as d:
            print("SECURE PRESERVATION:")
            text = "[CLASSIFIED] New security protocols archived\n"
            d.write(text)
            print(text, end="")
            print("Vault automatically sealed upon completion")
    except Exception as e:
        print(f"Error: {e}")
    else:
        print("\nAll vault operations completed with maximum security.")


if __name__ == "__main__":
    ft_vault_security()
