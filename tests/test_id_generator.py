"""
test_id_generator.py
Samuel Koller
Created: 19 October 2024
Updated: 19 October 2024

Test for the id_generator function.
"""

from src.utils import id_generator


def test_id_generator():
    """
    - Tests the ability of the id generator to increment the ID returned.
    """
    first_id = id_generator()
    second_id = id_generator()
    assert first_id + 1 == second_id
