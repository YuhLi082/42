def shadow_merge(list1:[list[int]], list2:[list[int]]) -> list[int]:
    result = []
    i = 0
    j = 0

    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            result += [list1[i]]
            i += 1
        else:
            result += [list2[j]]
            j += 1
    result += list1[i:]
    result += list2[j:]
    return result