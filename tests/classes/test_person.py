"""
test_person.py
Samuel Koller
Created: 19 October 2024
Updated: 19 October 2024

Test Suite for the Person class.
"""

from src.classes.person import Person


def test_person_given():
    """
    - Tests the ability to initialize a given person.
    """
    test_person = Person(**{"weight": 150, "cargo": 25, "origin": 1, "destination": 10})
    assert isinstance(test_person.id, int)
    assert test_person.weight == 150
    assert test_person.cargo == 25
    assert test_person.location == 1
    assert test_person.destination == 10


def test_person_generated():
    """
    - Tests the ability to generate missing attributes when initializing a person.
    """
    test_person = Person(**{"origin": 1, "destination": 10})
    assert 20 <= test_person.weight <= 500
    assert 0 <= test_person.cargo <= 100
