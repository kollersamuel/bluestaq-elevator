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

import json
import multiprocessing
import time
from time import sleep

from dotenv import load_dotenv
from flask import Flask, Response, request

from src.classes.elevator import Elevator
from src.utils.constants import TIMEOUT_TIME

load_dotenv()
app = Flask(__name__)
elevator = Elevator()


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check route to ping for application status.

    Responses:
        - **200 OK**: "Elevator is Online"
    """
    return Response("Elevator is Online", status=200)


@app.route("/request", methods=["POST"])
def make_request():
    """
    Route to submit a request to the elevator system.

    Responses:
        - **200 OK**: {}
    """
    new_request = request.get_json()

    with open("./requests.json", "r", encoding="utf-8") as requests_json:
        requests = json.load(requests_json)
    requests.append(new_request)
    with open("./requests.json", "w", encoding="utf-8") as requests_json:
        json.dump(requests, requests_json, indent=2)

    return Response({}, status=200)


def start_flask() -> None:
    """Runs the app via a function, so it can be used with multiprocessing."""
    # ! NOTE: This will NOT work in debug mode !
    app.run(debug=False, port=3148)


if __name__ == "__main__":
    flask_process = multiprocessing.Process(target=start_flask, daemon=False)
    flask_process.start()

    tik = time.time()
    while True:
        res = health_check()
        if res.status_code == 200:
            break
        if time.time() - tik > TIMEOUT_TIME:
            raise TimeoutError
        sleep(0.1)

    elevator_process = multiprocessing.Process(
        target=elevator.state_machine, daemon=True
    )
    elevator_process.start()

    elevator_process.join()
    flask_process.terminate()
    flask_process.join()
