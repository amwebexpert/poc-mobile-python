def is_blank(myString = None) -> bool:
    if myString is None:
        return True
    return not myString.strip()

def is_not_blank(myString = None) -> bool:
    return not is_blank(myString)
