def pattern_tracker(text:str) -> int:
    pairs = "01 12 23 34 45 56 67 78 89"
    i = 0
    count = 0

    while i < len(text) - 1:
        if text[i : i + 2] in pairs:
            count += 1
        i += 1
    return count