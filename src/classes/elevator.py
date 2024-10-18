"""
elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 17 October 2024

Class for the Elevator object, which tracks the state an contents of the elevator.
"""

import bisect
from enum import Enum
import logging
from time import sleep

from ..utils.constants import PLAYBACK_SPEED

from ...app import stop_queue

logger = logging.Logger('Elevator')


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
        self.top_floor: int = 20  # Temporary assumption.

    def update(self) -> None:
        while True:
            if stop_queue:
                if self.current_floor != stop_queue[0]:
                    self.move()
                else:
                    stop_queue = stop_queue[1:]
                    logger.debug(f"Reached queued floor {self.current_floor}, new queue: {stop_queue}")
            else: self.status = Status.IDLE


    def move(self) -> None:
        if stop_queue[0] > self.current_floor:
            self.status = Status.UP
            sleep(5 / PLAYBACK_SPEED)
            self.current_floor += 1
        else:
            self.status = Status.DOWN
            sleep(5 / PLAYBACK_SPEED)
            self.current_floor -= 1
        logger.error(f"Move's queue {stop_queue}")
        logger.error(f"Floor: {self.current_floor}")

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
        if stop_queue:
            if requested_floor in stop_queue:
                return
            stop_queue.append(requested_floor)
        else:
            stop_queue = [requested_floor]

        stop_queue.sort()
        split_index: int = bisect.bisect_left(stop_queue, self.current_floor)

        if self.direction_up:
            on_way: list[int] = stop_queue[split_index:]
            on_return: list[int] = list(reversed(stop_queue[:split_index]))
        else:
            on_way : list[int]= list(reversed(stop_queue[:split_index]))
            on_return: list[int] = stop_queue[split_index:]

        stop_queue = on_way + on_return

        logger.error(stop_queue)
