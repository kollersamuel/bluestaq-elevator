"""
app.py
Samuel Koller
Created: 15 October 2024
Updated: 17 October 2024

Main file for the Bluestaq Elevator Application. Houses the Flask server and relevant endpoints.

Functions:
    health_check(): A route to check if the service is running.
"""

__version__ = "0.3.0"

from dotenv import load_dotenv
from flask import Flask, jsonify

from src.classes.elevator import Elevator

load_dotenv()
app = Flask(__name__)
elevator = Elevator()

@app.route("/", methods=["GET"])
def health_check():
    """
    Health check route to ping for application status. Returns a response message and status code.

    Responses:
        - **200 OK**: "Elevator is Online"

    Returns:
        JSON, int
    """
    return jsonify({"message": "Elevator is Online"}), 200

@app.route("/floor/<int:floor>", methods=["GET"])
def add_stop(floor):
    elevator.add_stop(floor)
    return jsonify({}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded = True)
