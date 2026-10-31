def bracket_validator(s: str) -> bool:
    result = []

    for c in s:
        if c in "([{":
            result += c
        elif c in "}])":
            if result == []:
                return False
            if c == ")" and result[-1] != "(":
                return False
            if c == "}" and result[-1] != "{":
                return False
            if c == "]" and result[-1] != "[":
                return False
            result = result[:-1]
    return result == []
            
