import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    ops = {
        'add': operator.add,
        'multiply': operator.mul,
        'max': lambda x, y: x if x > y else y,
        'min': lambda x, y: x if x < y else y,
    }

    if operation not in ops:
        raise ValueError(f"Unknown operation: {operation}")

    return functools.reduce(ops[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    return {
        'fire': functools.partial(base_enchantment, 50, 'fire'),
        'ice': functools.partial(base_enchantment, 50, 'ice'),
        'lightning': functools.partial(base_enchantment, 50, 'lightning'),
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:

    @functools.singledispatch
    def cast_spell(arg: Any) -> str:
        return "Unknown spell type"

    @cast_spell.register(int)
    def _(arg: int) -> str:
        return f"Damage spell: {arg} damage"

    @cast_spell.register(str)
    def _(arg: str) -> str:
        return f"Enchantment: {arg}"

    @cast_spell.register(list)
    def _(arg: list) -> str:
        return f"Multi-cast: {len(arg)} spells"

    return cast_spell


if __name__ == "__main__":
    print("Testing spell reducer...")
    print(f"Sum: {spell_reducer([10, 20, 30, 40], 'add')}")
    print(f"Product: {spell_reducer([10, 20, 30, 40], 'multiply')}")
    print(f"Max: {spell_reducer([10, 20, 30, 40], 'max')}")

    print("\nTesting partial enchanter...")

    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"{element} enchantment on {target} with power {power}"

    enchanters = partial_enchanter(base_enchantment)
    print(enchanters['fire']('Sword'))
    print(enchanters['ice']('Shield'))
    print(enchanters['lightning']('Staff'))

    print("\nTesting memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    print("\nTesting spell dispatcher...")
    cast = spell_dispatcher()
    print(cast(42))
    print(cast("fireball"))
    print(cast(["fire", "ice", "lightning"]))
    print(cast(3.14))
