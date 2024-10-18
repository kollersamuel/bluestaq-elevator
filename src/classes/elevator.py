"""
elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 17 October 2024

Class for the Elevator object, which tracks the state an contents of the elevator.
"""

import bisect
from enum import Enum


class Status(Enum):
    """Possible Statuses of the Elevator."""

    IDLE = "Idle"
    UP = "Up"
    DOWN = "Down"


# TODO: Remove this pylint once a second public method is added.
# pylint: disable-next=R0903
class Elevator:
    """
    The Elevator object: transports persons to their requested destination.

    Attributes:
        status (str): The status of the elevator. Can be a string of select choices defined by the Status enum.
        stop_queue (list[int]): A priority queue of floors to stop at, priority is determined by closest floor in
            direction of travel.

    Examples:
        elevator = Elevator()
    """

    def __init__(self) -> None:
        """Initializes an Elevator class, sets initial state to Idle."""
        self.status: str = Status.IDLE
        self.current_floor: int = 1
        self.direction_up: bool = True
        self.stop_queue: list[int] = []
        self.top_floor: int = 20  # Temporary assumption.

    def add_stop(self, requested_floor: int) -> None:
        """
        Adds the requested floor the the priority queue in the correct position.

        Ignores the request if the floor does not exist or the request is for the current floor.

        Parameters:
            requested_floor (int): The floor to add to the priority queue.
        """
        # Catch a request to the current floor, and open door.
        # TODO: Have this open doors.
        if requested_floor == self.current_floor:
            return
        if requested_floor <= 0 or requested_floor > self.top_floor:
            return
        if self.stop_queue:
            if requested_floor in self.stop_queue:
                return
            self.stop_queue.append(requested_floor)
        else:
            self.stop_queue = [requested_floor]

        self.stop_queue.sort()
        split_index = bisect.bisect_left(self.stop_queue, self.current_floor)

        if self.direction_up:
            on_way = self.stop_queue[split_index:]
            on_return = list(reversed(self.stop_queue[:split_index]))
        else:
            on_way = list(reversed(self.stop_queue[:split_index]))
            on_return = self.stop_queue[split_index:]

        self.stop_queue = on_way + on_return
