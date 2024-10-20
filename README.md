# bluestaq-elevator

[Bluestaq Elevator Problem](https://github.com/kollersamuel/bluestaq-elevator)

Elevator program written as part of the interview process for Bluestaq, Colorado Springs. The goal of this application is to have a continuously running elevator system with randomly generated events. A user may use endpoints to manually add events.

A major assumption of this program is that this is a finite state machine and the application is built for a single machine and user.

This program also assumes that there is no thirteenth floor, similar to real life.

# Setup

This application was build using Python 3.11, for best results use this version.

Ensure you have postman or a terminal to send endpoints from.

First, run `pip install -r ./requirements.txt` (for production) and `pip install -r ./requirements.dev.txt` (for development).

# Usage

You may change values in the `.env` file to reconfigure how the application works.

The following endpoints have been implemented.

## GET /health

### Description

Health Check for the Application

### Responses

- **200 OK**
  - Description: Application is running.
  - Message: "Elevator is Online"

## GET /steps/<steps>

### Description

Progress the elevator by given number of steps.

### Parameters:
- Steps: An integer representing the number of steps to take.

### Responses

- **200 OK**
  - Description: Steps taken.
  - Message: "Moved 0 steps."


## POST /press_button

### Description

Route to manually press a button(s).

### Request Body
JSON list of buttons to press, each button must follow the format of {"source": int | str, "button": int | str}.

### Responses

- **200 OK**
  - Description: Request successfully submitted.
  - Message: "Pushed requested button(s)"

## POST /create_person

### Description

Route to create a person(s).

### Request Body
JSON list of persons to add, each person must follow the format of {"origin": int , "destination": int}, with optional keys of {"weight": float, "cargo": float}.

### Responses

- **200 OK**
  - Description: Request successfully submitted.
  - Message: "Created Person 0 with the following attributes: Origin: 1, Destination: 2, Weight: 150, Cargo: 25."

# Contributing

When contributing please continue to use the consistency standards set in place. To do this, ensure you have installed the development requirements. If so, run these commands (or run `. precommit.sh`):

1. `python -m black . -- quiet`, this will auto-format your code to match the black standards.
2. `python -m isort . --quiet`, this will auto-sort imports to match the isort standards.
3. `(echo -e "Pylint Report Generated $(date -u +%Y-%m-%dT%H:%M:%S%Z):\n" && python -m pylint . --output-format=text) > linting_report.txt`, this will generate a report with the current pylint rating of the code, and should be maintained at full marks.
4. `(echo -e "Coverage Report Generated $(date -u +%Y-%m-%dT%H:%M:%S%Z):\n" && python -m coverage run -m pytest -vv . && python -m coverage report -m) > testing_report.txt`, this will generate a report with the current coverage rating of the code, and should be maintained at close to full marks (>95%).

The CI pipeline will check the linting and testing using these tools, in Python 3.11.

Please update the CHANGELOG with any notable changes.

# Author

Samuel Koller: E-mail: `samuel.a.koller@gmail.com`, GitHub: `https://github.com/kollersamuel`
