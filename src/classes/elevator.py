"""
elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 18 October 2024

Class for the Elevator object, which tracks the state an contents of the elevator.
"""

import bisect
import logging
from enum import Enum
from time import sleep

from ..utils import PLAYBACK_SPEED, TOP_FLOOR

logger = logging.Logger("Elevator")


class Status(Enum):
    """Possible Statuses of the Elevator."""

    IDLE = "Idle"
    UP = "Up"
    DOWN = "Down"


class Elevator:
    """
    The Elevator object: transports persons to their requested destination.

    Attributes:
        stop_queue (list[int]): A priority queue of floors to stop at, priority is determined by closest floor in
        status (str): The status of the elevator. Can be a string of select choices defined by the Status enum.
            direction of travel.
        current_floor (int): The current floor the elevator is on.
        direction_up (bool): The current direction of the elevator.
        top_floor (int): The maximum floor of the elevator.

    Functions:
        start_state_machine(iterations=0): Runs the state machine for the given number of iterations, or forever.
        update(): Determines and executes the next action.
        move_to_next_floor(): Moves to the next floor in the queue.
        add_stop(): Adds a floor to the queue.

    Examples:
        elevator = Elevator([])
        elevator.start_state_machine()
    """

    def __init__(self, initial_queue) -> None:
        """Initializes an Elevator class, sets initial state to Idle."""
        self.stop_queue = initial_queue
        self.status: str = Status.IDLE
        self.current_floor: int = 1
        self.direction_up: bool = True
        self.top_floor: int = int(TOP_FLOOR)

    def start_state_machine(self, iterations: int = 0) -> None:
        """Once called, the elevator runs as a state machine for the given number of iterations or forever."""
        if iterations <= 0:
            while True:
                self.update()
        for _ in range(iterations):
            self.update()

    def update(self) -> None:
        """Determines what the next action for the elevator is."""
        if self.stop_queue:
            if self.current_floor != self.stop_queue[0]:
                self.move_to_next_floor()
            else:
                self.stop_queue = self.stop_queue[1:]
                logger.error(
                    f"Reached queued floor {self.current_floor}, new queue: {self.stop_queue}"
                )
        else:
            self.status = Status.IDLE

    def move_to_next_floor(self) -> None:
        """Moves the elevator in a determined direction."""
        if self.stop_queue[0] > self.current_floor:
            self.direction_up = True
            self.status = Status.UP
            sleep(5 / PLAYBACK_SPEED)
            self.current_floor += 1
        else:
            self.direction_up = False
            self.status = Status.DOWN
            sleep(5 / PLAYBACK_SPEED)
            self.current_floor -= 1
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
        if self.stop_queue:
            if requested_floor in self.stop_queue:
                return
            self.stop_queue.append(requested_floor)
        else:
            self.stop_queue = [requested_floor]

        self.stop_queue.sort()
        split_index: int = bisect.bisect_left(self.stop_queue, self.current_floor)

        if self.direction_up:
            on_way: list[int] = self.stop_queue[split_index:]
            on_return: list[int] = list(reversed(self.stop_queue[:split_index]))
        else:
            on_way: list[int] = list(reversed(self.stop_queue[:split_index]))
            on_return: list[int] = self.stop_queue[split_index:]

        self.stop_queue = on_way + on_return

        logger.error(self.stop_queue)
