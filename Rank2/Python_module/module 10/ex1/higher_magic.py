from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple[str, str]:
        return spell1(target, power), spell2(target, power)
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def conditional(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return conditional


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence(target: str, power: int) -> list[str]:
        return [s(target, power) for s in spells]
    return sequence


if __name__ == "__main__":
    def fireball(target: str, power: int) -> str:
        return f"Fireball hits {target}"

    def heal(target: str, power: int) -> str:
        return f"Heals {target}"

    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon", 10)
    print(f"Combined spell result: {result[0]}, {result[1]}")

    print("\nTesting power amplifier...")
    amplified_spell = power_amplifier(fireball, 3)
    original_power = 10
    print(f"Original power: {original_power}, Amplified: {original_power * 3}")

    print("\nTesting conditional caster...")

    cautious = conditional_caster(lambda t, p: p > 20, fireball)
    print(f"Power=15: {cautious('Orc', 15)}")
    print(f"Power=30: {cautious('Orc', 30)}")

    print("\nTesting spell sequence...")
    combo = spell_sequence([fireball, heal, fireball])
    results = combo("Goblin", 5)
    print(f"Sequence results: {results}")
