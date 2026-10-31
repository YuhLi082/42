from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform


def main() -> None:
    print("=== DataDeck Tournament Platform ===")
    print()

    platform = TournamentPlatform()

    print("Registering Tournament Cards...")
    dragon = TournamentCard("Fire Dragon", 5, "Legendary", 7, 8, 1200)
    wizard = TournamentCard("Ice Wizard", 4, "Rare", 5, 6, 1150)

    dragon_id = platform.register_card(dragon, "dragon_001")
    wizard_id = platform.register_card(wizard, "wizard_001")

    print(f"{dragon.name} (ID: {dragon_id}):")
    print("- Interfaces: [Card, Combatable, Rankable]")
    print(f"- Rating: {dragon.calculate_rating()}")
    print(f"- Record: {dragon.wins}-{dragon.losses}")
    print()

    print(f"{wizard.name} (ID: {wizard_id}):")
    print("- Interfaces: [Card, Combatable, Rankable]")
    print(f"- Rating: {wizard.calculate_rating()}")
    print(f"- Record: {wizard.wins}-{wizard.losses}")
    print()

    print("Creating tournament match...")
    match_result = platform.create_match(dragon_id, wizard_id)
    print(f"Match result: {match_result}")
    print()

    print("Tournament Leaderboard:")
    leaderboard = platform.get_leaderboard()
    for entry in leaderboard:
        print(
            f"{entry['rank']}. {entry['name']} "
            f"- Rating: {entry['rating']} ({entry['record']})"
        )
    print()

    print("Platform Report:")
    print(platform.generate_tournament_report())
    print()

    print("=== Tournament Platform Successfully Deployed! ===")
    print("All abstract patterns working together harmoniously!")


if __name__ == "__main__":
    main()
