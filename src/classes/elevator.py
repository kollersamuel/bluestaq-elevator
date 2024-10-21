"""
elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 20 October 2024

Class for the Elevator object, which tracks the state an contents of the elevator.
"""

import bisect
import logging
from enum import Enum

from src.classes.person import Person
from src.utils.constants import MAX_CAPACITY, MAX_WEIGHT, TOP_FLOOR

logger = logging.Logger("Elevator")


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
        self.up_queue: list[int] = []
        self.down_queue: list[int] = []
        self.priority_queue = []
        self.current_floor: int = 1
        self.direction_up: bool = True
        self.is_open = True
        self.persons = {"elevator": []}

    def process_request(self, **kwargs):
        """
        Processes the given button request and determines what to do.

        Parameters:
            **kwargs: A dictionary of the following structure: {"source": int | str, "button": int | str}
        """
        priority = False
        button = kwargs.get("button", None)
        if isinstance(button, list):
            if "close" in button:
                priority = True
                button.remove("close")
                # Make sure a number is at the beginning, when taking first index.
                button = sorted(button, key=lambda x: (isinstance(x, str), x))
                button = button[0]
        source = kwargs.get("source", None)

        if source == "elevator":
            if isinstance(button, int) and 0 < button < TOP_FLOOR:
                self.add_stop(button, priority)
        elif isinstance(source, int) and 0 < source < TOP_FLOOR:
            if button == "down":
                self.add_down_stop(source)
            elif button == "up":
                self.add_up_stop(source)

    def update(self) -> None:
        """Determines what the next action for the elevator is."""
        if len(self.priority_queue + self.up_queue + self.down_queue) == 0:
            return
        if self.priority_queue:
            if self.current_floor == self.priority_queue[0]:
                self.priority_queue.pop(0)
                self.open()
            elif self.priority_queue[0] > self.current_floor:
                self.move_up()
            else:
                self.move_down()

        elif self.direction_up:
            if self.up_queue:
                if self.current_floor == self.up_queue[0]:
                    self.up_queue.pop(0)
                    self.open()
                elif self.up_queue[0] > self.current_floor:
                    self.move_up()
                else:
                    self.move_down()
            else:
                if self.down_queue:
                    if self.down_queue[0] < self.current_floor:
                        self.move_down()
                    else:
                        self.move_up()

        elif not self.direction_up:
            if self.down_queue:
                if self.current_floor == self.down_queue[0]:
                    self.down_queue.pop(0)
                    self.open()
                elif self.down_queue[0] < self.current_floor:
                    self.move_down()
                else:
                    self.move_up()
            else:
                if self.up_queue:
                    if self.up_queue[0] < self.current_floor:
                        self.move_down()
                    else:
                        self.move_up()

    def open(self) -> None:
        """
        Opens the doors.

        When the elevator is open, it exchanges persons. If the person's destination is the current floor, they are
        off boarded, if there are persons waiting to board, they board without breaching the limits.
        """
        self.is_open = True
        self.persons["elevator"] = [
            person
            for person in self.persons["elevator"]
            if person.destination != self.current_floor
        ]

        total_weight = sum(
            person.weight + person.cargo for person in self.persons["elevator"]
        )
        entering_person_index = 0
        while (
            total_weight < MAX_WEIGHT
            and self.persons.get(self.current_floor)
            and len(self.persons.get(self.current_floor)) > entering_person_index
            and len(self.persons["elevator"]) < MAX_CAPACITY
        ):
            entering_person = self.persons[self.current_floor][entering_person_index]
            if (
                entering_person.destination > self.current_floor
                and self.direction_up
                or entering_person.destination < self.current_floor
                and not self.direction_up
            ):
                if (
                    total_weight + entering_person.weight + entering_person.cargo
                    < MAX_WEIGHT
                ):
                    self.persons["elevator"].append(entering_person)
                    self.persons[self.current_floor].pop(0)
                    self.add_stop(entering_person.destination)
                    total_weight = sum(
                        person.weight + person.cargo
                        for person in self.persons["elevator"]
                    )
            entering_person_index += 1

        # If no one is in the elevator but there are people waiting to get on, the elevator must be switching direction.
        if len(self.persons.get("elevator")) == 0 and len(
            self.persons.get(self.current_floor, [])
        ):
            self.direction_up = not self.direction_up
            self.open()
            self.up_queue = [
                stop for stop in self.up_queue if stop != self.current_floor
            ]
            self.down_queue = [
                stop for stop in self.down_queue if stop != self.current_floor
            ]

    def move_up(self) -> None:
        """Moves the elevator in a determined direction."""
        self.is_open = False
        self.direction_up = True
        self.current_floor += 1
        if self.current_floor == 13:
            self.move_up()
        if self.current_floor == TOP_FLOOR:
            self.direction_up = False

    def move_down(self) -> None:
        """Moves the elevator in a determined direction."""
        self.is_open = False
        self.direction_up = False
        self.current_floor -= 1
        if self.current_floor == 13:
            self.move_down()
        if self.current_floor == 1:
            self.direction_up = True

    def add_stop(self, stop: int, priority=False) -> None:
        """
        Processes given list of floors to stop at and queues them in a logical order.

        Parameters:
            stops (list[int]): A list of the floors to stop at.
        """
        if not 0 < stop <= TOP_FLOOR:
            return
        if stop == self.current_floor:
            self.open()
            return
        if priority:
            if stop not in self.priority_queue:
                self.priority_queue.append(stop)
            return

        if stop > self.current_floor:
            self.add_up_stop(stop)
        else:
            self.add_down_stop(stop)

    def add_up_stop(self, stop: int) -> None:
        if stop in self.up_queue:
            return
        up_stops = self.up_queue
        up_stops.append(stop)
        up_stops.sort()
        split_index: int = bisect.bisect_left(up_stops, self.current_floor)

        if self.direction_up:
            on_way: list[int] = up_stops[split_index:]
            on_return: list[int] = list(reversed(up_stops[:split_index]))
        else:
            on_way: list[int] = list(reversed(up_stops[:split_index]))
            on_return: list[int] = up_stops[split_index:]

        self.up_queue = on_way + on_return

    def add_down_stop(self, stop: int) -> None:
        if stop in self.down_queue:
            return
        down_stops = self.down_queue
        down_stops.append(stop)
        down_stops.sort()
        split_index: int = bisect.bisect_left(down_stops, self.current_floor)

        if self.direction_up:
            on_way: list[int] = down_stops[split_index:]
            on_return: list[int] = list(reversed(down_stops[:split_index]))
        else:
            on_way: list[int] = list(reversed(down_stops[:split_index]))
            on_return: list[int] = down_stops[split_index:]

        self.down_queue = on_way + on_return

    def add_person(self, person: Person):
        """
        Adds a person to the elevator and queues their location.

        Parameters:
            person (Person): The person to add to the elevator.
        """
        if self.persons.get(person.location):
            self.persons[person.location].append(person)
        else:
            self.persons[person.location] = [person]
        # ? If the added person is on the floor of the current elevator and it is open, load immediately.
        if person.location == self.current_floor and self.is_open:
            self.open()
        else:
            if person.location < person.destination:
                self.add_up_stop(person.location)
            else:
                self.add_down_stop(person.location)
