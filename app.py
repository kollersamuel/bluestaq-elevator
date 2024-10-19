"""
app.py
Samuel Koller
Created: 15 October 2024
Updated: 19 October 2024

Main file for the Bluestaq Elevator Application. Houses the Flask server and relevant endpoints.

Functions:
    health_check(): A route to check if the service is running.
"""

__version__ = "0.3.0"


import logging
from dotenv import load_dotenv
from flask import Flask, Response, request

from src.classes.elevator import Elevator
from src.classes.person import Person

load_dotenv()
app = Flask(__name__)
elevator = Elevator()


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger("Elevator")  



@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check route to ping for application status.

    Responses:
        - **200 OK**: "Elevator is Online"
    """
    return Response("Elevator is Online", status=200)

@app.route("/step/<int:steps>", methods=["GET"])
def step(steps:int):
    """
    Route to submit a request to the elevator system.

    Responses:
        - **200 OK**: {}
    """
    for _ in range(steps):
        logger.debug(f"After this step, the elevator is now at {elevator.current_floor} and has a queue of stops for these floors: {elevator.stop_queue}.")
        [logger.debug(f"Currently, there are: {len(v)} persons in the location of {k}") for k, v in elevator.persons.items()]
        elevator.update()

    logger.info(f"After {steps} steps, the elevator is now at {elevator.current_floor} and has a queue of stops for these floors: {elevator.stop_queue}.")
    return Response({}, status=200)

@app.route("/press_button", methods=["POST"])
def press_button():
    """
    Route to submit a request to the elevator system.

    Responses:
        - **200 OK**: {}
    """
    new_request = request.get_json()

    [elevator.process_request(**button) for button in new_request]

    return Response({}, status=200)


@app.route("/create_person", methods=["POST"])
def create_person():
    new_request = request.get_json()

    for person in new_request:
        new_person = Person(**person)
        elevator.add_person(new_person)

    
    return Response({}, status=200)


if __name__ == "__main__":
    app.run(debug=True, port=3148)
