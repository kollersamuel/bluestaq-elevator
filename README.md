# bluestaq-elevator

[Bluestaq Elevator Problem](https://github.com/kollersamuel/bluestaq-elevator)

This is an elevator program written as part of the interview process for Bluestaq, Colorado Springs. The goal of this application is to have a finite elevator state machine with manually entered events.

A major assumption of this program is not for expansion as part of a larger system, but just as a stand alone component and built for a single machine and user.

This program simulates some real attributes of most elevators, including there not being a thirteenth floor, and being able to make priority stops.

# Setup

This application was built using Python 3.11, for best results use this version.

Ensure you have postman or a terminal to send endpoints from.

First, run `pip install -r ./requirements.txt` (for production) and optionally `pip install -r ./requirements.dev.txt` (for development).

# Usage

You may change values in the `src/utils/constants.py` file to reconfigure how the application works.

The following endpoints have been implemented.

## GET /health

### Description

Health Check for the Application

### Responses

- **200 OK**
  - Description: Success
  - Message: Elevator is Online

## GET /steps/<steps>

### Description

Progress the elevator by given number of steps.

### Parameters:
- Steps: An integer representing the number of steps to take.

### Responses

- **200 OK**
  - Description: Success.
  - Message: Moved 0 step(s).


## POST /press_button

### Description

Route to manually press a button(s).

### Request Body
JSON list of buttons to press, each button must follow the format of {"source": int | str, "button": int | str | [int, str]}.

### Responses

- **200 OK**
  - Description: Success.
  - Message: Succesfully pressed requested button(s).
- **400 ERROR**
  - Description: Failed.
  - Submitted button invalid, details show invalid button.

## POST /create_person

### Description

Route to create a person(s).

### Request Body
JSON list of persons to add, each person must follow the format of {"origin": int , "destination": int}, with optional keys of {"weight": float, "cargo": float}.

### Responses

- **200 OK**
  - Description: Success
  - Message: Succesfully created requested person(s).
- **400 ERROR**
  - Description: Success
  - Message: Submitted person invalid, details show invalid person.

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
