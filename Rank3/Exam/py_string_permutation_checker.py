def string_permutation_checker(s1: str, s2: str) -> bool:
    count1 = {}
    count2 = {}

    for c in s1:
        if c not in count1:
            count1[c] = 0
        count1[c] += 1
    for c in s2:
            if c not in count2:
                count2[c] = 0
            count2[c] += 1
    return count1 == count2