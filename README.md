# bluestaq-elevator
Bluestaq Elevator Problem


# Setup

First, run `pip install -r ./requirements.txt` (for production) and `pip install -r ./requirements.dev.txt` (for development).

# Contributing

When contributing please continue to use the consistency standards set in place. To do this, ensure you have installed the development requirements. If so, run these commands:

1. `python -m black .`
2. `python -m isort .`
3. `(echo -e "Pylint Report Generated: $(date -u +%Y-%m-%dT%H:%M:%S%Z):\n" && python -m pylint . --output-format=text) > pylint_results.txt`, this will generate a report with the current pylint rating of the code, and should be maintained at full marks.