def string_sculptor(text: str) -> str:
    result = ""
    count = 0

    for c in text:
        if c == " ":
            count = 0
            result += c
        elif c.isalpha():
            if count % 2 == 0:
                result += c.lower()
                count += 1
            else:
                result += c.upper()
                count += 1
        else:
            result += c
    return result
        