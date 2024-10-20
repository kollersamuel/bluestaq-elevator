"""
test_elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 19 October 2024

Test Suite for the Elevator class.
"""

from src.classes.elevator import Elevator, Status
from src.classes.person import Person


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


def test_elevator_process_request():
    """
    - Tests the ability to process requests and queue the right floors.
    """
    test_elevator = Elevator()
    test_elevator.process_request(**{"source": "elevator", "button": 2})
    test_elevator.process_request(**{"source": 3, "button": "up"})
    test_elevator.process_request(**{"source": 14, "button": "down"})
    assert test_elevator.stop_queue == [2, 3, 14]


def test_elevator_delete_stop():
    """
    - Tests the ability of the elevator to stop if a request was deleted.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(4)
    test_elevator.update()
    test_elevator.stop_queue = []
    test_elevator.update()
    assert test_elevator.stop_queue == []
    assert test_elevator.status == Status.IDLE


def test_elevator_add_passed_stops_below():
    """
    - Tests the ability to multiple stops to an elevator.
    - Tests the ability of the elevator to organize the stops in the correcct order.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 5
    test_elevator.add_stop(10)
    test_elevator.update()
    test_elevator.add_stop(3)
    test_elevator.add_stop(1)
    test_elevator.update()
    assert test_elevator.stop_queue == [10, 3, 1]


def test_elevator_add_passed_stops_above():
    """
    - Tests the ability to multiple stops to an elevator.
    - Tests the ability of the elevator to organize the stops in the correcct order.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 5
    test_elevator.add_stop(2)
    test_elevator.update()
    test_elevator.update()
    test_elevator.add_stop(10)
    test_elevator.add_stop(3)
    test_elevator.update()
    assert test_elevator.stop_queue == [3, 2, 10]


def test_state_machine_up():
    """
    - Tests the ability to move up to the next floor if there is a higher floor queued next.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(3)
    test_elevator.update()

    assert test_elevator.stop_queue == [3]
    assert test_elevator.status == Status.UP


def test_state_machine_down():
    """
    - Tests the ability to move down to the next floor if there is a lower floor queued next.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(2)
    test_elevator.current_floor = 3
    test_elevator.update()
    test_elevator.update()

    assert test_elevator.current_floor == 2
    assert test_elevator.stop_queue == [2]
    assert test_elevator.status == Status.DOWN


def test_state_machine_stop():
    """
    - Tests the ability to stop at the next queued floor, then continue.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 3
    test_elevator.add_stop(2)
    test_elevator.add_stop(1)
    for _ in range(3):
        test_elevator.update()

    assert test_elevator.current_floor == 2
    assert test_elevator.stop_queue == [1]
    assert test_elevator.status == Status.OPEN

    test_elevator.update()

    assert test_elevator.stop_queue == [1]
    assert test_elevator.current_floor == 2
    assert test_elevator.status == Status.DOWN


def test_elevator_add_person():
    """
    - Tests the ability of the elevator to add a person to the system.
    """
    test_elevator = Elevator()
    test_person_1 = Person(**{"origin": 10, "destination": 1})
    test_person_2 = Person(**{"origin": 10, "destination": 1})

    test_elevator.add_person(test_person_1)
    assert len(test_elevator.persons.get(10)) == 1
    test_elevator.add_person(test_person_2)
    assert len(test_elevator.persons.get(10)) == 2
    assert test_elevator.stop_queue == [10]


def test_elevator_add_person_to_current_floor():
    """
    - Tests the ability to load a passenger.
    - Tests the ability of the elevator to add a person to the elevator after spawning if they are on the current floor.
    """
    test_elevator = Elevator()
    test_person = Person(**{"origin": 1, "destination": 10})

    test_elevator.add_person(test_person)
    assert len(test_elevator.persons.get("elevator")) == 1
