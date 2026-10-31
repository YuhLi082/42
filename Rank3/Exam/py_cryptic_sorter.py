def cryptic_sorter(strings: list[str]) -> list[str]:
    result = []

    for c in strings:
        result += [c]
        i = 0
        while i < len(result):
            j = 0
            while j < len(result) - i - 1:
                p = result[j]
                s = result[j + 1]
                if len(p) > len(s):
                    result[j + 1], result[j] = p, s
                elif len(p) == len(s):
                    if p.lower() > s.lower():
                        result[j + 1], result[j] = p, s
                j += 1
            i += 1
    return result