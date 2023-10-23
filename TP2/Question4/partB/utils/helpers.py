def format_currency(value):
    """
    Format the given value as a currency string.

    :param value: float: The value to be formatted.

    :return: The formatted currency string.
    :rtype: str
    """
    return "${:,.2f}".format(value)
