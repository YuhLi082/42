def whisper_cipher(text: str, shift: int) -> str:
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    for c in text:
        i = 0
        if c in upper:
            while c != upper[i]:
                i += 1
            c  = upper[(i + shift) % 26]
            result += c
        elif c in lower:
            while c != lower[i]:
                i += 1
            c  = lower[(i + shift) % 26]
            result += c
        else:
            result += c
    return result