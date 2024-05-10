import re


def validate_phone_number(phone_number: str) -> bool:
    """
    Validates user's phone number
    :param phone_number:
    :return: bool
    """
    pattern = r'^\+998\d{9}$'
    regex = re.compile(pattern)

    if regex.match(phone_number.replace(" ", "").replace("-", "").replace(")", "").replace("(", "")):
        return True
    return False
