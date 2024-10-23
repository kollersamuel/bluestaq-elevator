# bluestaq-elevator

[Bluestaq Elevator Problem](https://github.com/kollersamuel/bluestaq-elevator)

This is an elevator program written as part of the application process for Bluestaq, Colorado Springs. The goal of this program is imitate the way an elevator works via a finite elevator state machine with manually entered events.

# Assumptions

- The elevator is a finite state machine, meaning it only updates by request.

- This program is not for expansion as part of a larger system, but just as a stand alone component. This program was also not designed to be expanded into an elevator system with multiple elevators.

- This program built for a single machine and user and is not meant to be scaled.

- The elevator uses a prioritization method of the next floor in current direction of travel until depleted, before switching to the opposite direction of travel and corresponding queue, putting a hold to queued floors in the original direction of travel that were not on route. These queues are both put on hold if there is a priority stop.

- This is an elevator system that uses Natural Numbers (not zero) and does not use the thirteenth floor, as is realistic with many elevators in reality.

- This elevator has the ability to prioritize stops for cases of emergencies by pressing the close and a floor button simultaneously. This button has to be intentionally pressed, and thus can not be done via a personell interaction. In the unlikely case of multiple priority stops, the stops are done in a standard queue (first in, first out).

- The elevator has a maximum capacity in the form of individuals and weight. This is done by assuming people will not breach this capacity limit prior to entering the elevator.

- People have weights and are possibly holding cargo with weight as well.

- Once a person has left the elevator, they are removed from the simulation.

- People board the elevator in a standard queue (first in, first out) method of when they arrived at the elevator.

- There is no reason to open or close the doors via the buttons in this elevator, with the exception of making a priority stop. There is no reason to do an emergency stop (stopping the elevator completely and taking it offline) or a call. These buttons are found in most elevators.

- The elevator is meticulously maintained and does not break down.

- The elevator remains open and stationary if there are no passengers and no stops queued.

# Setup

This program was built using Python 3.11, for best results use this version.

Ensure you have postman or a terminal to send endpoints from.

First, run `pip install -r ./requirements.txt` (for production) and optionally `pip install -r ./requirements.dev.txt` (for development).

Then, run `python app.py` and see the **Usage** section for guidance on interaction endpoints. Debug mode is currently turned off, to change this, edit the argument to `False` in `app.run(debug=False, port=3148)` in `app.py`.

Note: You may change values in the `src/utils/constants.py` file to reconfigure how the program works. Beware: There is no validation on these values and may break the program if invalid values are assigned, validation may be implemented in the future.

# Usage

The following endpoints have been implemented.

## GET /health

### Description

Health Check for the Program.

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

Examples:

- Request for the elevator to stop at floor 3 on the way up: [{"source": 3, "button": "up"}]
- Request for the elevator to stop at floors 5 and 7 while inside: [{"source": "elevator", "button": 5}, {"source": "elevator", "button": 7}]
- Request for the elevator to immediately go to floor 12 from inside: [{"source": "elevator:, "button": ["close", 12]}]

### Responses

- **200 OK**
  - Description: Success.
  - Message: Succesfully pressed requested button(s).
- **400 ERROR**
  - Description: Failed.
  - Submitted button invalid, details show invalid button.

## POST /create_person

### Description

Route to create a person(s) with journeys.

### Request Body

JSON list of persons to add, each person must follow the format of {"origin": int , "destination": int}, with optional keys of {"weight": float, "cargo": float}.

Examples:

- Two people with randomly generated weights and cargos requesting to move from floor 1 to 3: [{"origin": 1, "destination": 3}, {"origin": 1, "destination": 3}]
- A person with a set weight and cargo requesting to move from floor 1 to 3: [{"origin": 1, "destination": 3, "weight": 180, "cargo": 50}]

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

The CI pipeline will check the linting and testing using these tools and their specific versions (noted in `requirements.dev.txt`), in Python 3.11.

Please update the `CHANGELOG.md` with any notable changes.

# Author

Samuel Koller: - E-mail: `samuel.a.koller@gmail.com` - LinkedIn: `https://www.linkedin.com/in/koller-samuel/` - GitHub: `https://github.com/kollersamuel`

## Acknowledgements

GitHub's template for pylint CI workflow and python project `.gitignore`.

# Possible Future Work:

- Implement infinite state machine (with sleep methods in updates) and use multi-threading to allow requests to be processed while maintaining access to shared data.
- Implement multiple elevators into one system, using shared queues. This will require a re-design of the data flow.
- Minor updates can be found in the `TODO.md`.
