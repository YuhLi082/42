def hidenp(small: str, big: str) -> bool:
    remaining = small

    for c in big:
        if remaining == "":
            return True
        if c == remaining[0]:
            remaining = remaining[1:]
    return remaining == ""