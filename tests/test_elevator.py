"""
test_elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 17 October 2024

Test Suite for the Elevator class.
"""

from src.classes.elevator import Elevator


def test_elevator_add_stop():
    """
    - Tests the ability to add a stop to an elevator.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(2)
    assert test_elevator.stop_queue == [2]


def test_elevator_add_ignored_stops():
    """
    - Tests the ability of the elevator to not add the current floor to the stop queue.
    - Tests the ability of the elevator to not add a floor that does not exist.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(0)
    test_elevator.add_stop(1)
    test_elevator.add_stop(100)
    assert test_elevator.stop_queue == []


def test_elevator_add_stop_multiple_times():
    """
    - Tests the ability of the elevator to not add the requested floor to the stop queue if already queued.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(4)
    test_elevator.add_stop(4)
    assert test_elevator.stop_queue == [4]


def test_elevator_add_multiple_stops():
    """
    - Tests the ability to multiple stops to an elevator.
    - Tests the ability of the elevator to organize the stops in the correcct order.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(4)
    test_elevator.add_stop(3)
    assert test_elevator.stop_queue == [3, 4]


def test_elevator_add_passed_stops_below():
    """
    - Tests the ability to multiple stops to an elevator.
    - Tests the ability of the elevator to organize the stops in the correcct order.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 5
    test_elevator.add_stop(10)
    test_elevator.add_stop(3)
    test_elevator.add_stop(1)
    assert test_elevator.stop_queue == [10, 3, 1]


def test_elevator_add_passed_stops_above():
    """
    - Tests the ability to multiple stops to an elevator.
    - Tests the ability of the elevator to organize the stops in the correcct order.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 5
    test_elevator.add_stop(1)
    # ! Temporary, as nothing currently sets this.
    test_elevator.direction_up = False
    test_elevator.add_stop(10)
    test_elevator.add_stop(3)
    assert test_elevator.stop_queue == [3, 1, 10]
