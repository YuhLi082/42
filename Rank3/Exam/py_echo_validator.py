def echo_validator(text: str) -> bool:
    result = ""

    for c in text:
        if c.isalpha():
            c = c.lower()
            result += c
    if result == "":
        return False
    return result == result[:: -1]
            