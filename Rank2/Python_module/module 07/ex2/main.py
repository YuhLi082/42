from ex2.EliteCard import EliteCard


def main() -> None:
    print("=== DataDeck Ability System ===")
    print()

    print("EliteCard capabilities:")
    print("- Card: ['play', 'get_card_info', 'is_playable']")
    print("- Combatable: ['attack', 'defend', 'get_combat_stats']")
    print("- Magical: ['cast_spell', 'channel_mana', 'get_magic_stats']")

    arcane_warrior = EliteCard("Arcane Warrior", 6, "Legendary", 5, 8, 4)
    print(f"Playing {arcane_warrior.name} (Elite Card):")

    print("Combat phase:")
    print(f"Attack result: {arcane_warrior.attack('Enemy')}")
    print(f"Defense result: {arcane_warrior.defend(5)}")

    print("Magic phase:")
    channel_result = arcane_warrior.channel_mana(3)
    spell_result = arcane_warrior.cast_spell('Fireball', ['Enemy1', 'Enemy2'])
    print(f"Spell cast: {spell_result}")
    print(f"Mana channel: {channel_result}")

    print("Multiple interface implementation successful!")


if __name__ == "__main__":
    main()
