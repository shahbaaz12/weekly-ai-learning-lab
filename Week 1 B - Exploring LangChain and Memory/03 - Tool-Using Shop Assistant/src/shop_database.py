"""Small local database used by the shop assistant tool."""

# This dictionary acts like a tiny database for the learning project.
PRICES = {
    "shoes": 799,
    "hat": 399,
    "bag": 1420,
    "shorts": 1299,
    "pants": 1699,
}


def get_price(item: str) -> str:
    """Look up one item in the local price database."""
    # Normalize the name so "Shoes" and " shoes " work the same way.
    item = item.strip().lower()
    price = PRICES.get(item)

    if price is None:
        return f"Sorry, I do not have a price for '{item}'."

    return f"The price of {item} is Rs {price}."
