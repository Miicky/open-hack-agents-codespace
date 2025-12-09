import math
from typing import Dict

def recommend_pizza(adults: int, children: int) -> Dict[str, int]:
    """
    Recommend how many large pizzas to order based on number of adults and children.

    Assumptions:
    - 1 large pizza is suitable for 2 adults and 2 children.
    - 1 adult = 1 unit of appetite
    - 1 child = 0.5 unit of appetite
    - 1 large pizza covers 3 appetite units.
    """
    if adults < 0 or children < 0:
        raise ValueError("Number of adults and children must be non-negative.")

    appetite_units = adults + 0.5 * children
    large_pizzas = math.ceil(appetite_units / 3.0)

    return {
        "large_pizzas": large_pizzas,
        "adults": adults,
        "children": children
    }
