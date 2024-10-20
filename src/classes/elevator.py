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

    IDLE = "Idle" # Idle means closed and not moving.
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
        self.next_cycle = []
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
                    self.open()
        else:
            self.status = Status.IDLE
            [self.add_stop(stop["stop"]) for stop in self.next_cycle]
            self.next_cycle = []
        if self.current_floor == 1:
            self.direction_up = True
            for stop in self.next_cycle:
                new_cycle_list = []
                if stop["up"]:
                    self.add_stop(stop["stop"])
                else:
                    new_cycle_list.append(stop)
        elif self.current_floor == TOP_FLOOR:
            self.direction_up = False
            for stop in self.next_cycle:
                new_cycle_list = []
                if not stop["up"]:
                    self.add_stop(stop["stop"])
                else:
                    new_cycle_list.append(stop)

    def open(self) -> None:
        """Opens the doors."""
        self.status = Status.OPEN
        self.stop_queue.pop(0)
        if not self.stop_queue:
            self.up_stop_queue = []
            self.down_stop_queue = []
        if self.current_floor == 1:
            self.down_stop_queue = []
        if self.current_floor == TOP_FLOOR:
            self.up_stop_queue = []
        self.load()
        if self.stop_queue:
            self.direction_up = self.stop_queue[0] > self.current_floor

    def load(self) -> None:
        """
        When the elevator is open, it exchanges persons. If the person's destination is the current floor, they are
        off boarded, if there are persons waiting to board, they board without breaching the limits.
        """
        self.persons["elevator"] = [
            person
            for person in self.persons["elevator"]
            if person.destination != self.current_floor
        ]
        total_weight = sum(
            person.weight + person.cargo for person in self.persons["elevator"]
        )

        enter_queue_index = 0
        while (
            total_weight < MAX_WEIGHT
            and enter_queue_index < len(self.persons.get(self.current_floor, []))
            and len(self.persons["elevator"]) < MAX_CAPACITY
        ):
            next_in_line = self.persons[self.current_floor][enter_queue_index]
            if (next_in_line.destination > self.current_floor and self.direction_up) or (next_in_line.destination < self.current_floor and not self.direction_up):
                self.persons["elevator"].append(next_in_line)
                self.persons[self.current_floor].pop(enter_queue_index)
                self.add_stop(next_in_line.destination, next_in_line.destination > self.current_floor)
                total_weight = sum(
                    person.weight + person.cargo for person in self.persons["elevator"]
                )
            else: enter_queue_index+=1

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

    def add_stop(self, stop: int, up=None) -> None:
        """
        Processes given list of floors to stop at and queues them in a logical order.

        Parameters:
            stops (list[int]): A list of the floors to stop at.
        """
        # If the person needs to wait for the next cycle
        if up == self.direction_up == True and stop < self.current_floor or up == self.direction_up == False  and   stop > self.current_floor:
            self.next_cycle.append({"stop": stop, "up": up})
            return
        if not 0 < stop <= TOP_FLOOR or stop in self.stop_queue:
            return
        if stop == TOP_FLOOR and up == False:
            return
        
        if stop == self.current_floor:
            # TODO: Open door
            return
        if not 0 < stop <= TOP_FLOOR:
            return
        # Requested stop should just happen in current direction.
        if up is None:
            up = self.direction_up
        if up:
            new_stops = self.up_stop_queue
        elif up == False:
            new_stops = self.down_stop_queue

        if stop in new_stops:
            return
        new_stops.append(stop)
        new_stops.sort()
        split_index: int = bisect.bisect_left(new_stops, self.current_floor)

        if self.direction_up:
            on_way: list[int] = new_stops[split_index:]
            on_return: list[int] = list(reversed(new_stops[:split_index]))
        else:
            on_way: list[int] = list(reversed(new_stops[:split_index]))
            on_return: list[int] = new_stops[split_index:]

        self.stop_queue = list(set(on_way)) + list(set(on_return))
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
            self.add_stop(person.location, person.destination > person.location)
