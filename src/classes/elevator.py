"""
elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 17 October 2024

Class for the Elevator object, which tracks the state an contents of the elevator.
"""

from enum import Enum


class Status(Enum):
    IDLE = "Idle"
    UP = "Up"
    DOWN = "Down"


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
        self.direction_up: bool | None = None
        self.stop_queue: list[int] = []
        self.top_floor: int = 5  # Temporary assumption.

    def add_stop(self, requested_floor: int) -> None:
        # If there are no scheduled stops, add the requested floor and set the direction.
        if not self.stop_queue:
            if requested_floor > self.current_floor:
                self.direction_up = True
            elif requested_floor < self.current_floor:
                self.direction_up = False
            else:
                return
            self.stop_queue = [requested_floor]
        # If the elevator is already going up, insert the new request such that it falls chronologically in the
        # ascending sequence if the floor is above or in the descending sequence if the floor is below.
        elif self.direction_up:
            if requested_floor > self.current_floor:
                index_to_insert = next(
                    (
                        i
                        for i, v in enumerate(self.stop_queue)
                        if v < requested_floor or v < self.current_floor
                    ),
                    None,
                )
                self.stop_queue.insert(index_to_insert, requested_floor)
            elif requested_floor < self.current_floor:
                index_to_insert = next(
                    (
                        i
                        for i, v in enumerate(self.stop_queue)
                        if v > requested_floor or v > self.current_floor
                    ),
                    None,
                )
                self.stop_queue.insert(index_to_insert, requested_floor)
            else:
                return
        # If the elevator is already going down, insert the new request such that it falls chronologically in the
        # ascending sequence if the floor is above or in the descending sequence if the floor is below.
        elif self.direction_up == False:
            if requested_floor > self.current_floor:
                index_to_insert = next(
                    (
                        i
                        for i, v in enumerate(reversed(self.stop_queue))
                        if v < requested_floor or v < self.current_floor
                    ),
                    None,
                )
                self.stop_queue.insert(index_to_insert, requested_floor)
            elif requested_floor < self.current_floor:
                index_to_insert = next(
                    (
                        i
                        for i, v in enumerate(reversed(self.stop_queue))
                        if v > requested_floor or v > self.current_floor
                    ),
                    None,
                )
                self.stop_queue.insert(index_to_insert, requested_floor)
            else:
                return
        # Else catches a request to the current floor, and ignores.
        # TODO: Have this open doors.
        else:
            return
