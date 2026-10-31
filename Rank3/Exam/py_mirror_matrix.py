def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    result = []

    for raw in matrix:
        result += [raw[::-1]]
    return result