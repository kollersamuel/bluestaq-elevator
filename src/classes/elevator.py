"""
elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 19 October 2024

Class for the Elevator object, which tracks the state an contents of the elevator.
"""

import bisect
import logging
from enum import Enum
from time import sleep

from src.classes.person import Person

from ..utils import PLAYBACK_SPEED, TOP_FLOOR

logger = logging.Logger("Elevator")


class Status(Enum):
    """Possible Statuses of the Elevator."""

    IDLE = "Idle"
    UP = "Up"
    DOWN = "Down"
    DOOR_OPEN = "DoorOpen"


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
        state_machine(iterations=0): Runs the state machine for the given number of iterations, or forever.
        update(): Determines and executes the next action.
        move_to_next_floor(): Moves to the next floor in the queue.
        update_stops(list[int]): Adds a floor to the queue.

    Examples:
        elevator = Elevator()
        elevator.state_machine()
    """

    def __init__(self) -> None:
        """Initializes an Elevator class, sets initial state to Idle."""
        self.stop_queue: list[int] = []
        self.status: str = Status.IDLE
        self.current_floor: int = 1
        self.direction_up: bool = True
        self.top_floor: int = int(TOP_FLOOR)
        self.persons = {}

    def process_request(self, **kwargs):
        button = kwargs.get("button", None)
        source = kwargs.get("source", None)

        if source == "elevator":
            if isinstance(button, int) and 0 < button < self.top_floor:
                self.add_stop(button)
        elif isinstance(source, int) and 0 < source < self.top_floor:
            if button == "down":
                pass
            elif button == "up":
                pass

    def update(self) -> None:
        """Determines what the next action for the elevator is."""
        if self.stop_queue:
            if self.current_floor != self.stop_queue[0]:
                self.move_to_next_floor()
            else:
                self.stop_queue.pop(0)
                logger.debug(
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
        logger.info(f"Arrived at floor: {self.current_floor}")

    def add_stop(self, stop: int) -> None:
        """
        Processes given list of floors to stop at and queues them in a logical order.

        Parameters:
            stops (list[int]): A list of the floors to stop at.
        """
        if not 0 < stop <= self.top_floor or stop in self.stop_queue:
            return
        if stop == self.current_floor:
            # TODO: Open door
            return
        
        new_stops = self.stop_queue
        new_stops.append(stop)
        new_stops.sort()
        split_index: int = bisect.bisect_left(new_stops, self.current_floor)

        if self.direction_up:
            on_way: list[int] = new_stops[split_index:]
            on_return: list[int] = list(reversed(new_stops[:split_index]))
        else:
            on_way: list[int] = list(reversed(new_stops[:split_index]))
            on_return: list[int] = new_stops[split_index:]

        self.stop_queue = on_way + on_return
        logger.debug(self.stop_queue)


    def add_person(self, person: Person):
        person_location = person.origin
        if self.persons.get(person_location):
            self.persons[person_location].append(person)
        else:
            self.persons[person_location] = [person]
        print(self.persons)
        self.add_stop(person.destination)