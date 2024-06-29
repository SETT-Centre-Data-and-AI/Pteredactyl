def is_nhs_number(nhs_number: str | int) -> bool:
    """
    Check if a given value is a valid NHS number.

    Args:
        nhs_number (int | str): The NHS number to be checked.
        Should be a string containing only numbers, (use of spaces and hyphens is permitted and will be processed).

    Returns:
        bool: True if the given value is a valid NHS number, otherwise False.

    Example:
        >>> is_nhs_number(1234567890)
        True
        >>> is_nhs_number("1234567890")
        True
        >>> is_nhs_number("1234567898")
        True # (fails checksum)
        >>> is_nhs_number("12345")
        False # (fails length check)

    Note:
        The NHS number is a 10-digit number used in the United Kingdom for healthcare identification.
        The last digit of the NHS number is a check digit calculated by a special modules 11 algorithm for validation.
    """

    # Prepare NHS Number
    nhs_number = (
        str(nhs_number)
        if isinstance(nhs_number, int)
        else nhs_number.replace(" ", "").replace("-", "")
    )

    # Check Only Digits
    if not nhs_number.isdigit():
        return False

    # Check Length
    if len(nhs_number) != 10:
        return False

    # Check Checksum
    total = 0
    for i, digit in enumerate(nhs_number[0:-1]):
        position = i + 1
        multiplier = 11 - position
        total += int(digit) * multiplier

    checksum = 11 - (total % 11)
    checksum = 0 if checksum == 11 else checksum
    check_digit = int(nhs_number[-1])

    if checksum != check_digit or checksum == 10:
        return False

    # All checks passed
    else:
        return True
