def twist_sequence(arr: list[int], k: int) -> list[int]:
    if arr == []:
        return []
    k = k % len(arr)
    return arr[-k:] + arr[:-k]