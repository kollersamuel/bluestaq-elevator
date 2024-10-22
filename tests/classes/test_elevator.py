"""
test_elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 21 October 2024

Test Suite for the Elevator class.
"""

from src.classes.elevator import Elevator
from src.classes.person import Person
from src.utils.constants import MAX_WEIGHT, TOP_FLOOR


def test_elevator_add_stop():
    """
    - Tests the ability to add a stop to an elevator.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(2)

    assert test_elevator.up_queue == [2]


def test_elevator_add_ignored_stops():
    """
    - Tests the ability of the elevator to not add the current floor to the stop queue.
    - Tests the ability of the elevator to not add a floor that does not exist.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(0)
    test_elevator.add_stop(1)
    test_elevator.add_stop(int(TOP_FLOOR) + 1)

    assert test_elevator.up_queue == []
    assert test_elevator.down_queue == []


def test_elevator_add_up_stop_multiple_times():
    """
    - Tests the ability of the elevator to not add the requested floors to the queues if already queued.
    """
    test_elevator = Elevator()
    test_elevator.add_down_stop(4)
    test_elevator.add_down_stop(4)
    test_elevator.add_up_stop(4)
    test_elevator.add_up_stop(4)

    assert test_elevator.up_queue == [4]
    assert test_elevator.down_queue == [4]


def test_elevator_add_multiple_stops():
    """
    - Tests the ability to multiple stops to an elevator.
    - Tests the ability of the elevator to organize the stops in the correcct order.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(4)
    test_elevator.add_stop(3)

    assert test_elevator.up_queue == [3, 4]


def test_elevator_process_request():
    """
    - Tests the ability to process requests and queue the right floors.
    """
    test_elevator = Elevator()
    test_elevator.process_request(**{"source": "elevator", "button": 2})
    test_elevator.process_request(**{"source": 3, "button": "up"})
    test_elevator.process_request(**{"source": 14, "button": "down"})

    assert test_elevator.up_queue == [2, 3]
    assert test_elevator.down_queue == [14]


def test_elevator_process_priority_request():
    """
    - Tests the ability to process a priority request and queue the right floors.
    """
    test_elevator = Elevator()
    test_elevator.process_request(**{"source": "elevator", "button": ["close", 15]})

    assert test_elevator.priority_queue == [15]


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

    assert test_elevator.up_queue == [10]
    assert test_elevator.down_queue == [3, 1]


def test_elevator_add_passed_stops_above():
    """
    - Tests the ability to multiple stops to an elevator.
    - Tests the ability of the elevator to organize the stops in the correcct order.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 5
    test_elevator.add_stop(2)
    test_elevator.update()
    test_elevator.add_stop(10)
    test_elevator.add_stop(3)

    assert test_elevator.down_queue == [3, 2]
    assert test_elevator.up_queue == [10]


def test_elevator_skip_floor_thirteen():
    """
    - Tests the ability of the elevator to skip the thirteenth floor.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 12
    test_elevator.add_stop(14)
    test_elevator.update()
    test_elevator.update()

    assert test_elevator.current_floor == 14


def test_elevator_up():
    """
    - Tests the ability to move up to the next floor if there is a higher floor queued next.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(3)
    test_elevator.update()

    assert test_elevator.up_queue == [3]
    assert test_elevator.current_floor == 2


def test_elevator_down():
    """
    - Tests the ability to move down to the next floor if there is a lower floor queued next.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 3
    test_elevator.add_stop(2)
    test_elevator.update()

    assert test_elevator.current_floor == 2
    assert test_elevator.down_queue == [2]


def test_elevator_stop():
    """
    - Tests the ability to stop at the next queued floor, then continue.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 3
    test_elevator.add_stop(2)
    test_elevator.add_stop(1)
    test_elevator.update()
    test_elevator.update()

    assert test_elevator.current_floor == 2
    assert test_elevator.down_queue == [1]
    assert test_elevator.is_open

    test_elevator.update()

    assert test_elevator.current_floor == 1
    assert test_elevator.down_queue == [1]
    assert test_elevator.is_open is False


def test_elevator_swap_to_up_below_queue():
    """
    - Tests the ability to continue moving down if the down queue is empty, but the first item in the up queue is below.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 3
    test_elevator.direction_up = False
    test_elevator.add_up_stop(2)
    test_elevator.update()

    assert test_elevator.current_floor == 2
    assert test_elevator.up_queue == [2]


def test_elevator_swap_to_up_above_queue():
    """
    - Tests the ability to begin moving up if the down queue is empty and the first item in the up queue is above.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 3
    test_elevator.direction_up = False
    test_elevator.add_up_stop(4)
    test_elevator.update()

    assert test_elevator.current_floor == 4
    assert test_elevator.up_queue == [4]


def test_elevator_swap_to_down_below_queue():
    """
    - Tests the ability to begin moving down if the up queue is empty and the first item in the down queue is below.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 3
    test_elevator.add_down_stop(4)
    test_elevator.update()

    assert test_elevator.current_floor == 4
    assert test_elevator.down_queue == [4]


def test_elevator_priority_floor():
    """
    - Tests the ability to stop at the next priority floor.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 2
    test_elevator.add_stop(2, True)
    test_elevator.update()

    assert test_elevator.current_floor == 2
    assert not test_elevator.priority_queue


def test_elevator_priority_up():
    """
    - Tests the ability to move to the next priority floor if above current floor.
    """
    test_elevator = Elevator()
    test_elevator.add_stop(2, True)
    test_elevator.update()
    test_elevator.update()

    assert test_elevator.current_floor == 2
    assert not test_elevator.priority_queue


def test_elevator_priority_down():
    """
    - Tests the ability to move to the next priority floor if below current floor.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 2
    test_elevator.add_stop(1, True)
    test_elevator.update()
    test_elevator.update()

    assert test_elevator.current_floor == 1
    assert not test_elevator.priority_queue


def test_elevator_move_down_at_max_up_queue():
    """
    - Tests the ability to begin moving down if the maximum floor in the up queue has been reached, but there are more
    floors in the up queue.
    """
    test_elevator = Elevator()
    test_elevator.add_up_stop(3)
    test_elevator.update()  # 2
    test_elevator.add_up_stop(1)
    for _ in range(3):
        test_elevator.update()  # 3, 3 (open), 2

    assert test_elevator.direction_up is False
    assert test_elevator.up_queue == [1]


def test_elevator_move_up_at_min_down_queue():
    """
    - Tests the ability to begin moving up if the minimum floor in the down queue has been reached, but there are more
    floors in the down queue.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 5
    test_elevator.add_down_stop(3)
    test_elevator.update()  # 4
    test_elevator.add_down_stop(5)
    for _ in range(3):
        test_elevator.update()  # 3, 3 (open), 4

    assert test_elevator.direction_up
    assert test_elevator.down_queue == [5]


def test_elevator_add_person():
    """
    - Tests the ability of the elevator to add a person going up to the system.
    - Tests the ability of the elevator to add a person going down to the system.
    """
    test_elevator = Elevator()
    test_person_1 = Person(**{"origin": 10, "destination": 1})
    test_person_2 = Person(**{"origin": 10, "destination": 20})
    test_elevator.add_person(test_person_1)

    assert len(test_elevator.persons.get(10)) == 1

    test_elevator.add_person(test_person_2)

    assert len(test_elevator.persons.get(10)) == 2
    assert test_elevator.down_queue == [10]
    assert test_elevator.up_queue == [10]


def test_elevator_add_person_to_current_floor():
    """
    - Tests the ability to load a passenger.
    - Tests the ability for loading passengers to not press a floor if already queued.
    - Tests the ability of the elevator to add a person to the elevator after spawning if they are on the current floor.
    """
    test_elevator = Elevator()
    test_person = Person(**{"origin": 1, "destination": 10})
    test_elevator.add_person(test_person)

    assert len(test_elevator.persons.get("elevator")) == 1


def test_elevator_stop_adding_at_capacity():
    """
    - Tests the ability to only load the elevator to capacity.
    """
    test_elevator = Elevator()
    # ? MAX_WEIGHT - 1, so that the elevator is not at capacity, and tries to load the next passenger.
    test_person_1 = Person(
        **{"origin": 1, "destination": 10, "weight": MAX_WEIGHT - 1, "cargo": 0}
    )
    test_person_2 = Person(**{"origin": 1, "destination": 10})
    test_elevator.add_person(test_person_1)
    test_elevator.add_person(test_person_2)

    assert len(test_elevator.persons.get("elevator")) == 1
    assert len(test_elevator.persons.get(1)) == 1


def test_elevator_switch_direction_at_limit():
    """
    - Tests the ability to change the direction of travel if the elevator has reached a limit.
    """
    test_elevator = Elevator()
    test_elevator.current_floor = 19
    test_elevator.add_stop(20)
    test_elevator.update()

    assert test_elevator.direction_up is False


def test_elevator_switch_direction_at_end_of_queue():
    """
    - Tests the ability to change the direction of travel if the elevator is empty.
    """
    test_elevator = Elevator()
    test_person_up = Person(**{"origin": 1, "destination": 2})
    test_person_down = Person(**{"origin": 2, "destination": 1})
    test_elevator.add_person(test_person_up)
    test_elevator.add_person(test_person_down)
    test_elevator.update()
    test_elevator.update()

    assert test_elevator.direction_up is False
    assert len(test_elevator.persons["elevator"]) == 1
    assert len(test_elevator.persons[2]) == 0
