import sys


ITEMS_DATA = {
    "sword": {"type": "weapon", "rarity": "rare", "value": 500},
    "potion": {"type": "consumable", "rarity": "common", "value": 50},
    "shield": {"type": "armor", "rarity": "uncommon", "value": 200},
    "armor": {"type": "armor", "rarity": "common", "value": 150},
    "helmet": {"type": "armor", "rarity": "common", "value": 100}
}


def parse_args() -> dict[str, int]:
    """Parse command line arguments (format: item:qty)."""
    inventory = {}
    for arg in sys.argv[1:]:
        item, qty_str = arg.split(":")
        inventory.update({item: int(qty_str)})
    return inventory


def get_stats(inventory: dict[str, int]) -> dict:
    """Calculate inventory statistics."""
    total_items = sum(inventory.values())
    unique_types = len(inventory.keys())

    items_list = [(name, qty) for name, qty in inventory.items()]
    most = items_list[0]
    least = items_list[0]
    for item in items_list:
        if item[1] > most[1]:
            most = item
        if item[1] < least[1]:
            least = item

    return {
        "total": total_items,
        "unique": unique_types,
        "most": most,
        "least": least
    }


def categorize(inventory: dict[str, int]) -> dict[str, dict]:
    """Group items by quantity (Moderate >=5, Scarce <=4)."""
    cats = {"Moderate": {}, "Scarce": {}}
    for name, qty in inventory.items():
        if qty >= 5:
            cats["Moderate"].update({name: qty})
        else:
            cats["Scarce"].update({name: qty})
    return cats


def get_restock(inventory: dict[str, int]) -> list[str]:
    """Find items with quantity 1."""
    restock = []
    for name, qty in inventory.items():
        if qty == 1:
            restock.append(name)
    for i in range(len(restock)):
        for j in range(i + 1, len(restock)):
            if restock[i] > restock[j]:
                restock[i], restock[j] = restock[j], restock[i]
    return restock


def main() -> None:
    """Run inventory system."""
    if len(sys.argv) < 2:
        print("Usage: python3 ft_inventory_system.py item:qty ...")
        return

    inv = parse_args()
    stats = get_stats(inv)

    print("=== Inventory System Analysis ===")
    print(f"Total items in inventory: {stats['total']}")
    print(f"Unique item types: {stats['unique']}")

    print("\n=== Current Inventory ===")
    items = [(name, qty) for name, qty in inv.items()]
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i][1] < items[j][1]:
                items[i], items[j] = items[j], items[i]

    for name, qty in items:
        pct = (qty / stats['total']) * 100
        unit = "unit" if qty == 1 else "units"
        print(f"{name}: {qty} {unit} ({pct:.1f}%)")

    print("\n=== Inventory Statistics ===")
    most_unit = "unit" if stats['most'][1] == 1 else "units"
    least_unit = "unit" if stats['least'][1] == 1 else "units"
    print(f"Most abundant: {stats['most'][0]} "
          f"({stats['most'][1]} {most_unit})")
    print(f"Least abundant: {stats['least'][0]} "
          f"({stats['least'][1]} {least_unit})")

    print("\n=== Item Categories ===")
    cats = categorize(inv)
    for cat_name in cats:
        if cats[cat_name]:
            print(f"{cat_name}: {cats[cat_name]}")

    print("\n=== Management Suggestions ===")
    restock = get_restock(inv)
    if restock:
        restock_str = restock[0]
        for i in range(1, len(restock)):
            restock_str += ", " + restock[i]
        print(f"Restock needed: {restock_str}")
    else:
        print("No restock needed")

    print("\n=== Dictionary Properties Demo ===")
    keys_str = ""
    first = True
    for k in inv.keys():
        if not first:
            keys_str += ", "
        keys_str += k
        first = False
    print(f"Dictionary keys: {keys_str}")

    vals_str = ""
    first = True
    for v in inv.values():
        if not first:
            vals_str += ", "
        vals_str += str(v)
        first = False
    print(f"Dictionary values: {vals_str}")

    print(f"Sample lookup - 'sword' in inventory: {inv.get('sword', 0) > 0}")


if __name__ == "__main__":
    main()
