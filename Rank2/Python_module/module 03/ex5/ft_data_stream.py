import time
from typing import Generator


PLAYERS = ["alice", "bob", "charlie", "diana", "eve"]
EVENT_TYPES = ["killed monster", "found treasure", "leveled up",
               "collected item", "defeated boss"]


def game_event_stream(count: int) -> Generator:
    """Generate game events on-demand without storing them all in memory."""
    for i in range(count):
        player_index = i % len(PLAYERS)
        event_index = i % len(EVENT_TYPES)
        level = (i % 20) + 1
        yield {
            "id": i + 1,
            "player": PLAYERS[player_index],
            "level": level,
            "event": EVENT_TYPES[event_index]
        }


def fibonacci_generator() -> Generator:
    """Generate Fibonacci numbers indefinitely."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def prime_generator() -> Generator:
    """Generate prime numbers indefinitely."""
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1


def process_stream(count: int) -> dict:
    """Process event stream and collect analytics
    without storing all events."""
    total = 0
    high_level = 0
    treasure = 0
    levelup = 0

    for event in game_event_stream(count):
        if event["id"] <= 3:
            print(f"Event {event['id']}: Player {event['player']} "
                  f"(level {event['level']}) {event['event']}")
        elif event["id"] == 4:
            print("...")

        total += 1
        if event["level"] >= 10:
            high_level += 1
        if event["event"] == "found treasure":
            treasure += 1
        if event["event"] == "leveled up":
            levelup += 1

    return {
        "total": total,
        "high_level": high_level,
        "treasure": treasure,
        "levelup": levelup
    }


def take(gen: Generator, n: int) -> list:
    """Take first n values from a generator."""
    result = []
    for value in gen:
        result.append(value)
        if len(result) == n:
            break
    return result


def main() -> None:
    print("=== Game Data Stream Processor ===")
    print("Processing 1000 game events...")
    print()

    start = time.time()
    stats = process_stream(1000)
    elapsed = time.time() - start

    print()
    print("=== Stream Analytics ===")
    print(f"Total events processed: {stats['total']}")
    print(f"High-level players (10+): {stats['high_level']}")
    print(f"Treasure events: {stats['treasure']}")
    print(f"Level-up events: {stats['levelup']}")
    print("\nMemory usage: Constant (streaming)")
    print(f"Processing time: {elapsed:.3f} seconds")

    print()
    print("=== Generator Demonstration ===")

    fib = fibonacci_generator()
    fib_values = take(fib, 10)
    fib_str = ""
    for i in range(len(fib_values)):
        if i > 0:
            fib_str += ", "
        fib_str += str(fib_values[i])
    print(f"Fibonacci sequence (first 10): {fib_str}")

    primes = prime_generator()
    prime_values = take(primes, 5)
    prime_str = ""
    for i in range(len(prime_values)):
        if i > 0:
            prime_str += ", "
        prime_str += str(prime_values[i])
    print(f"Prime numbers (first 5): {prime_str}")


if __name__ == "__main__":
    main()
