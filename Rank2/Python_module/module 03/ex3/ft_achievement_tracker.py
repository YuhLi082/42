def main() -> None:
    """
    Achievement Tracker System that uses sets to manage
    and analyze player achievements.
    Demonstrates set operations: union, intersection, and difference.
    """
    print("=== Achievement Tracker System ===")
    print()
    """Initialize each player's achievement set using set()"""
    alice_set = set({'first_kill', 'level_10',
                     'treasure_hunter', 'speed_demon'})
    bob_set = set({'first_kill', 'level_10', 'boss_slayer', 'collector'})
    charlie_set = set({'level_10', 'treasure_hunter', 'boss_slayer',
                       'speed_demon', 'perfectionist'})
    print(f"Player alice achievements: {alice_set}")
    print(f"Player bob achievements: {bob_set}")
    print(f"Player charlie achievements: {charlie_set}")
    print()
    print("=== Achievement Analytics ===")

    """Combine all achievements from every player to get the full unique set"""
    all_achievements = alice_set.union(bob_set).union(charlie_set)
    total_unique_achievements = len(all_achievements)
    print(f"All unique achievements: {all_achievements}")
    print(f"Total unique achievements: {total_unique_achievements}")
    print()
    """Find achievements that every player has unlocked"""
    common = alice_set.intersection(bob_set).intersection(charlie_set)
    print(f"Common to all players: {common}")

    """Find achievements unlocked by exactly one player (rare achievements)"""
    alice_only = alice_set.difference(bob_set).difference(charlie_set)
    bob_only = bob_set.difference(alice_set).difference(charlie_set)
    charlie_only = charlie_set.difference(alice_set).difference(bob_set)
    rare = alice_only.union(bob_only).union(charlie_only)
    print(f"Rare achievements (1 player): {rare}")
    print()
    """Compare Alice and Bob: find shared and exclusive achievements"""
    a_b_common = alice_set.intersection(bob_set)
    alice_unique = alice_set.difference(bob_set)
    bob_unique = bob_set.difference(alice_set)
    print(f"Alice vs Bob common: {a_b_common}")
    print(f"Alice unique: {alice_unique}")
    print(f"Bob unique: {bob_unique}")


if __name__ == "__main__":
    main()
