"""
elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 23 October 2024

Class for the Elevator object, which tracks the state an contents of the elevator.
"""

import bisect
import logging

from src.classes.person import Person
from src.utils.constants import MAX_CAPACITY, MAX_WEIGHT, TOP_FLOOR
from src.utils.custom_exceptions import InvalidButton

logger = logging.Logger("Elevator")


class Elevator:
    """
    Transports Person objects to their requested destination.
    """

    def __init__(self) -> None:
        """
        The elevator object begins with open doors and empty queues, on the first floor, and in the upward direction.

        Attributes:
            up_queue (list[int]): A priority queue of floors in the upward direction to stop at, priority is determined
                by closest floor in direction of travel.
            down_queue (list[int]): A priority queue of floors in the downward direction to stop at, priority is
                determined by closest floor in direction of travel.
            priority_queue (list[int]): A priority queue of floors in the the have been prioritized due to an
                emergency, priority is determined by order of floors queued.
            current_floor (int): The current floor the elevator is on.
            direction_up (bool): The current direction of the elevator.
            is_open (bool): The status of the doors.
            persons (dict): A dictionary containing persons at each floor and in the elevator.
        """
        self.up_queue: list[int] = []
        self.down_queue: list[int] = []
        self.priority_queue: list[int] = []
        self.current_floor: int = 1
        self.direction_up: bool = True
        self.is_open: bool = True
        self.persons: dict = {"elevator": []}

    def process_request(self, source, button) -> None:
        """
        Processes the given button request and determines what to do.

        Parameters:
            source (int | str): The source of the button press.
            button (int | str | list[int , str]): The button pressed.
        """
        priority: bool = False

        # Check for priority queuing
        if isinstance(button, list):
            if "close" in button:
                priority = True
                # ? This is done here to return the correct argument in press_button() in app.py
                # Make sure a number is at the beginning, when taking first index.
                if (
                    13 in button
                    or not 1
                    <= sorted(button, key=lambda x: (isinstance(x, str), x))[0]
                    <= TOP_FLOOR
                ):
                    raise InvalidButton()
                button = sorted(button, key=lambda x: (isinstance(x, str), x))
                button: int = button[0]

        self.process_button(source, button, priority)

    # pylint: disable=too-many-branches
    def process_button(self, source, button, priority: bool) -> None:
        """
        Ensures button combination is valid and takes the appropriate action.

        Parameters:
            source (int | str): The source of the button press.
            button (int | str | list[int , str]): The button pressed.
            priority (bool): If the button was prioritized.
        """
        if isinstance(button, list) or isinstance(source, list):
            raise InvalidButton()
        if isinstance(source, int):
            if source == 13 or not 1 <= source <= TOP_FLOOR:
                raise InvalidButton()
            if isinstance(button, str):
                if button.lower() == "down":
                    self.add_down_stop(source)
                elif button.lower() == "up":
                    self.add_up_stop(source)
                else:
                    raise InvalidButton()
            else:
                raise InvalidButton()

        if isinstance(source, str):
            if source.lower() != "elevator":
                raise InvalidButton()
            if isinstance(button, int):
                if button == 13 or not 1 <= button <= TOP_FLOOR:
                    raise InvalidButton()
                self.add_stop(button, priority)
            else:
                raise InvalidButton()

    # pylint: enable=too-many-branches

    def update(self) -> None:
        """Determines what the next action for the elevator is."""
        if len(self.priority_queue) == len(self.up_queue) == len(self.down_queue) == 0:
            return
        if self.priority_queue:
            self.priority_update()

        elif self.direction_up:
            self.up_update()

        elif not self.direction_up:
            self.down_update()

    def priority_update(self) -> None:
        """Called when there is an item in the priority queue, determines action to take."""
        self.down_queue = []
        self.up_queue = []
        if self.current_floor == self.priority_queue[0]:
            self.priority_queue.pop(0)
            self.open()
        elif self.priority_queue[0] > self.current_floor:
            self.move(True)
        else:
            self.move(False)
        if not self.priority_queue:
            self.requeue_all()

    def up_update(self) -> None:
        """Called when the current direction of the elevator is up, determines action to take."""
        if self.up_queue:
            if self.current_floor == self.up_queue[0]:
                self.up_queue.pop(0)
                self.open()
            elif self.up_queue[0] > self.current_floor:
                self.move(True)
                # ? If the next item in the up_queue is below the current floor, start going down
                # ? The down_queue will be read next
            else:
                self.move(False)
        else:
            if self.down_queue:
                if self.down_queue[0] < self.current_floor:
                    self.move(False)
                else:
                    self.move(True)

    def down_update(self) -> None:
        """Called when the current direction of the elevator is down, determines action to take."""
        if self.down_queue:
            if self.current_floor == self.down_queue[0]:
                self.down_queue.pop(0)
                self.open()
            elif self.down_queue[0] < self.current_floor:
                self.move(False)
            # ? If the next item in the down_queue is aboce the current floor, start going up
            # ? The up_queue will be read next
            else:
                self.move(True)
        else:
            if self.up_queue:
                if self.up_queue[0] < self.current_floor:
                    self.move(False)
                else:
                    self.move(True)

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

        total_weight: float = sum(
            person.weight + person.cargo for person in self.persons["elevator"]
        )
        entering_person_index: int = 0
        while (
            total_weight < MAX_WEIGHT
            and self.persons.get(self.current_floor)
            and len(self.persons.get(self.current_floor)) > entering_person_index
            and len(self.persons["elevator"]) < MAX_CAPACITY
        ):
            entering_person: Person = self.persons[self.current_floor][
                entering_person_index
            ]
            if (
                entering_person.destination > self.current_floor
                and self.direction_up
                or entering_person.destination < self.current_floor
                and not self.direction_up
            ):
                if (
                    total_weight + entering_person.weight + entering_person.cargo
                    <= MAX_WEIGHT
                ):
                    self.persons[self.current_floor].pop(0)
                    self.persons["elevator"].append(entering_person)
                    self.add_stop(entering_person.destination)
                    total_weight = sum(
                        person.weight + person.cargo
                        for person in self.persons["elevator"]
                    )
                else:
                    break
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

    def move(self, up: bool) -> None:
        """
        Moves the elevator.

        Parameters:
            up (bool): Move up if true, move down if false.
        """
        if up:
            self.move_up()
        else:
            self.move_down()

        previous_floor: int = self.current_floor - (1 if up else -1)
        # ? If people were unable to board on the previous floor, requeue the previous floor.
        if self.persons.get(previous_floor, []):
            # pylint: disable=expression-not-assigned
            [
                self.add_person_stop(person)
                for person in self.persons.get(previous_floor, [])
            ]
            # pylint: enable=expression-not-assigned

        # ? Skip the 13th floor by moving again.
        if self.current_floor == 13:
            self.move(up)

    def move_up(self) -> None:
        """Moves the elevator upwards."""
        self.is_open = False
        self.direction_up = True
        self.current_floor += 1
        if self.current_floor == TOP_FLOOR:
            self.direction_up = False

    def move_down(self) -> None:
        """Moves the elevator downwards."""
        self.is_open = False
        self.direction_up = False
        self.current_floor -= 1
        if self.current_floor == 1:
            self.direction_up = True

    def add_stop(self, stop: int, priority=False) -> None:
        """
        Processes given a stop queued from inside the elevator and adds it to the currently used queue.

        Parameters:
            stop (int): The floors to stop at.
            priority (boolean): If the floor is a priority stop, defaults to false.
        """
        if not self.validate_stop(stop):
            return
        if priority and stop not in self.priority_queue:
            self.priority_queue.append(stop)
        elif stop > self.current_floor:
            self.add_up_stop(stop)
        else:
            self.add_down_stop(stop)

    def validate_stop(self, stop: int) -> bool:
        """
        Validates the stop to ensure it is in the system or current floor, If it is the current floor, it reopens the
        doors.

        Parameters:
            stop (int): The stop to validate.

        Returns: True if the stop is a valid floor, otherwise False.
        """
        if not 0 < stop <= TOP_FLOOR:
            return False
        if stop == self.current_floor:
            self.open()
            return False
        return True

    def add_up_stop(self, stop: int) -> None:
        """
        This will only be called from outside the elevator. Adds a stop to the downward queue if valid.

        Parameters:
            stop (int): The stop to be queued in the downward direction.
        """
        if not self.validate_stop(stop) or stop in self.up_queue:
            return
        up_stops: list[int] = self.up_queue
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
        """
        This will only be called from outside the elevator. Adds a stop to the upward queue if valid.

        Parameters:
            stop (int): The stop to be queued in the upward direction.
        """
        if not self.validate_stop(stop) or stop in self.down_queue:
            return
        down_stops: list[int] = self.down_queue
        down_stops.append(stop)
        down_stops.sort()
        split_index: int = bisect.bisect_left(down_stops, self.current_floor)

        if self.direction_up:
            on_way: list[int] = down_stops[split_index:]
            on_return: list[int] = down_stops[:split_index][::-1]
        else:
            on_way: list[int] = down_stops[:split_index][::-1]
            on_return: list[int] = down_stops[split_index:]

        self.down_queue = on_way + on_return

    def add_person(self, person: Person) -> None:
        """
        Adds a person to the elevator and queues their location.

        Parameters:
            person (Person): The person to add to the elevator.
        """
        self.persons.setdefault(person.location, []).append(person)
        # ? If the added person is on the floor of the current elevator and it is open, load immediately.
        if person.location == self.current_floor and self.is_open:
            self.open()
        else:
            self.add_person_stop(person)

    def add_person_stop(self, person: Person) -> None:
        """
        Adds the person's floor to the correct queue.

        Parameters:
            person (Person): The person's stop to add.
        """
        if person.location < person.destination:
            self.add_up_stop(person.location)
        else:
            self.add_down_stop(person.location)

    def requeue_all(self) -> None:
        """Called after the elevator clears it's priority queue to requeue all persons in the simulation."""
        for person in self.persons["elevator"]:
            self.add_stop(person.destination)
        for i in range(1, TOP_FLOOR + 1):
            for person in self.persons.get(i, []):
                self.add_person_stop(person)
