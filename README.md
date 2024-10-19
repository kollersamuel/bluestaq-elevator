# bluestaq-elevator

Bluestaq Elevator Problem

Elevator program written as part of the interview process for Bluestaq, Colorado Springs. The goal of this application is to have a continuously running elevator system with randomly generated events. A user may use endpoints to manually add events.

`https://github.com/kollersamuel/bluestaq-elevator`

# Setup

This application was build using Python 3.11, for best results use this version.

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

# Future Work
Have the elevator and flask add requests to the same queue.