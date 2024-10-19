# bluestaq-elevator

[Bluestaq Elevator Problem](https://github.com/kollersamuel/bluestaq-elevator)

Elevator program written as part of the interview process for Bluestaq, Colorado Springs. The goal of this application is to have a continuously running elevator system with randomly generated events. A user may use endpoints to manually add events.

A major assumption of this program is that this is a standalone application for a single machine and user. If future intentions were to have multiple users access the elevator or to integrate this into a system as a microservice, a key required change would be to not use `requests.json` as a "database"/"queue"; Rather one would likely substitute this with a service such as RabbitMQ. The reason for this is the danger of reading and writing to the file from multiple processes, which can lead to file (in this case the database) corruption and would ultimately cause the application to have a fatal exception. In the current set up, it is difficult to overload the system when manually accessing endpoints.

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

## POST /request

### Description

Route to submit a request to the elevator system.

### Responses

- **200 OK**
  - Description: Request successfully submitted.
  - Message: {}

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
