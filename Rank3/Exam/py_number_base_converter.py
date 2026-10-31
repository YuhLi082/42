def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "0123456789abcdefghijklmnopqrstuvwxyz"

    if from_base < 2 or from_base > 36:
        return "ERROR"
    if to_base < 2 or to_base > 36:
        return "ERROR"
    if number == "":
        return "ERROR"

    negative = False
    if number[0] == "-":
        negative = True
        number = number[1:]
    if number == "":
        return "ERROR"

    value = 0
    for c in number:
        digit = 0
        while digit < 36:
            if c == digits[digit] or c == lower[digit]:
                break
            digit += 1
        if digit >= from_base:
            return "ERROR"
        value = value * from_base + digit

    if value == 0:
        return "0"

    result = ""
    while value > 0:
        remainder = value % to_base
        result = digits[remainder] + result
        value //= to_base

    if negative:
        result = "-" + result
    return result