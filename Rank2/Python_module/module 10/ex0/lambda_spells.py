from typing import Any


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda x: x['power'], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda x: x['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: f"* {x} *", spells))


def mage_stats(mages: list[dict]) -> dict[str, Any]:
    if not mages:
        return {'max_power': 0, 'min_power': 0, 'avg_power': 0.0}

    max_power = max(mages, key=lambda m: m['power'])['power']
    min_power = min(mages, key=lambda m: m['power'])['power']
    avg_power = round(sum(m['power'] for m in mages) / len(mages), 2)

    return {
        'max_power': max_power,
        'min_power': min_power,
        'avg_power': avg_power
    }


if __name__ == "__main__":
    artifacts = [
        {'name': 'Fire Staff', 'power': 92, 'type': 'weapon'},
        {'name': 'Crystal Orb', 'power': 85, 'type': 'focus'},
        {'name': 'Shadow Dagger', 'power': 78, 'type': 'weapon'},
    ]

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    a1 = sorted_artifacts[0]
    a2 = sorted_artifacts[1]
    print(
        f"{a1['name']} ({a1['power']} power)"
        f" comes before"
        f" {a2['name']} ({a2['power']} power)"
    )

    mages = [
        {'name': 'Alex', 'power': 50, 'element': 'fire'},
        {'name': 'Jordan', 'power': 30, 'element': 'water'},
        {'name': 'Riley', 'power': 70, 'element': 'earth'},
    ]

    print("\nTesting power filter...")
    filtered = power_filter(mages, 40)
    names = list(map(lambda m: m['name'], filtered))
    print(f"Mages with power >= 40: {names}")

    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f"Max power: {stats['max_power']}")
    print(f"Min power: {stats['min_power']}")
    print(f"Avg power: {stats['avg_power']}")

    spells = ['fireball', 'heal', 'shield']
    print("\nTesting spell transformer...")
    transformed = spell_transformer(spells)
    print(" ".join(transformed))
