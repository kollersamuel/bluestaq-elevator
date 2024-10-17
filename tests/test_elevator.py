"""
test_elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 17 October 2024

Test Suite for the Elevator class.
"""

from src.classes.elevator import Elevator


def test_elevator_init():
    """TODO: Replace this test with a permanent one; This was added to test the testing report."""
    test_elevator = Elevator()
    assert test_elevator.status == "Idle"
