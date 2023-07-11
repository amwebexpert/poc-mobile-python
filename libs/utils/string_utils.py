def is_blank(myString=None):
    if myString is None:
        return True
    return not myString.strip()

def is_not_blank (myString=None):
    return not isBlank(myString)
