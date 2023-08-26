def is_blank(my_string=None) -> bool:
    if my_string is None:
        return True
    return not my_string.strip()


def is_not_blank(my_string=None) -> bool:
    return not is_blank(my_string)
