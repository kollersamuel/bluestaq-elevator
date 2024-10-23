"""
id_generator.py
Samuel Koller
Created: 19 October 2024
Updated: 22 October 2024

Generates unique identifiers.
"""

INITIAL_ID: int = -1


def id_generator():
    """Returns the current id and increments."""
    global INITIAL_ID  # pylint: disable=global-statement
    INITIAL_ID += 1
    return INITIAL_ID
