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

from src.classes.person import Person
from src.utils.constants import MAX_CAPACITY, MAX_WEIGHT, TOP_FLOOR

logger = logging.Logger("Elevator")


class Status(Enum):
    """Possible Statuses of the Elevator."""

    IDLE = "Idle"
    UP = "Up"
    DOWN = "Down"
    OPEN = "Open"


class Elevator:
    """
    The Elevator object: transports persons to their requested destination.

    Attributes:
        stop_queue (list[int]): A priority queue of floors to stop at, priority is determined by closest floor in
            direction of travel.
        status (str): The status of the elevator. Can be a string of select choices defined by the Status enum.
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
        self.status: str = Status.OPEN
        self.current_floor: int = 1
        self.direction_up: bool = True
        self.persons = {"elevator": []}

    def process_request(self, **kwargs):
        """
        Processes the given button request and determines what to do.

        Parameters:
            **kwargs: A dictionary of the following structure: {"source": int | str, "button": int | str}
        """
        button = kwargs.get("button", None)
        source = kwargs.get("source", None)

        if source == "elevator":
            if isinstance(button, int) and 0 < button < TOP_FLOOR:
                self.add_stop(button)
        elif isinstance(source, int) and 0 < source < TOP_FLOOR:
            if button == "down":
                self.add_stop(source)
            elif button == "up":
                self.add_stop(source)

    def update(self) -> None:
        """Determines what the next action for the elevator is."""
        if self.stop_queue:
            if self.current_floor != self.stop_queue[0]:
                if self.status == Status.OPEN:
                    self.close()
                else:
                    self.move_to_next_floor()
            else:
                if self.status in [Status.DOWN, Status.UP]:
                    logger.debug(f"Reached queued floor {self.current_floor}")
                    self.open()
        else:
            self.status = Status.IDLE

    def open(self) -> None:
        """Opens the doors."""
        self.status = Status.OPEN
        self.load()
        self.stop_queue.pop(0)

    def load(self) -> None:
        """
        When the elevator is open, it exchanges persons. If the person's destination is the current floor, they are
        off boarded, if there are persons waiting to board, they board without breaching the limits.
        """
        new_current_floor_persons = []
        new_current_floor_persons.extend(self.persons.get(self.current_floor, []))
        new_current_floor_persons.extend(
            [
                person
                for person in self.persons["elevator"]
                if person.destination == self.current_floor
            ]
        )
        self.persons["elevator"] = [
            person
            for person in self.persons["elevator"]
            if person.destination != self.current_floor
        ]
        total_weight = sum(
            person.weight + person.cargo for person in self.persons["elevator"]
        )
        while (
            total_weight < MAX_WEIGHT
            and self.persons.get(self.current_floor, [])
            and len(self.persons["elevator"]) < MAX_CAPACITY
        ):
            entered_person = self.persons[self.current_floor][0]
            self.persons["elevator"].append(entered_person)
            self.persons[self.current_floor].pop(0)
            self.add_stop(entered_person.destination)

    def close(self) -> None:
        """Closes the elevator and determines direction of travel."""
        self.status = (
            Status.UP if self.stop_queue[0] > self.current_floor else Status.DOWN
        )

    def move_to_next_floor(self) -> None:
        """Moves the elevator in a determined direction."""
        if self.stop_queue[0] > self.current_floor:
            self.direction_up = True
            self.status = Status.UP
            self.current_floor += 1
        else:
            self.direction_up = False
            self.status = Status.DOWN
            self.current_floor -= 1
        logger.info(f"Arrived at floor: {self.current_floor}")

    def add_stop(self, stop: int) -> None:
        """
        Processes given list of floors to stop at and queues them in a logical order.

        Parameters:
            stops (list[int]): A list of the floors to stop at.
        """
        if not 0 < stop <= TOP_FLOOR or stop in self.stop_queue:
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
        """
        Adds a person to the elevator and queues their location.

        Parameters:
            person (Person): The person to add to the elevator.
        """
        person_location = person.location
        if self.persons.get(person_location):
            self.persons[person_location].append(person)
        else:
            self.persons[person_location] = [person]
        # ? If the added person is on the floor of the current elevator and it is open, load immediately.
        if person_location == self.current_floor and self.status == Status.OPEN:
            self.load()
        else:
            self.add_stop(person.location)
