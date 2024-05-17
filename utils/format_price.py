def format_price_digits(price: float) -> str:
    """
    Returns formatted version of a price
    :param price: product price
    :return: float
    """

    return f"{price:,.2f}".replace(',', ' ')
