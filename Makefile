# Python version Python3.12
PYTHON = python3.12

# Define application name and source directory
APP_NAME = data-pre-processing
APP_DIR = .


# Pip environment configuration
PIP_ENV = venv

# Define paths
REQUIREMENTS_DIR = .
REQUIREMENTS_FILE = ${REQUIREMENTS_DIR}/requirements.txt
REQUIREMENTS_IN = ${REQUIREMENTS_DIR}/requirements.in

# Targets
all: run

# Create virtual environment
venv:
	$(PYTHON) -m pip install virtualenv
	$(PYTHON) -m virtualenv $(PIP_ENV)

# Activate virtual environment
activate-env:
	@source $(PIP_ENV)/bin/activate

# Install dependencies from pip-compile
install-deps: venv # activate-env
	$(PYTHON) -m pip install -r $(REQUIREMENTS_FILE)

# Clean virtual environment
deactivate-env:
	deactivate

clean-env:
	rm -rf $(PIP_ENV)

# Run Flask app
run: install-deps # activate-env
	$(PYTHON) $(APP_DIR)/processing.py

# Test Flask app
test: install-deps # activate-env
	# Add your test commands here
	@echo "Not integrated"

# Help message
help:
	@echo "Available targets:"
	@echo "  all         		: Build and run the application"
	@echo "  venv        		: Create a virtual environment"
	@echo "  activate-env   : Activate the virtual environment"
	@echo "  install-deps 	: Install dependencies using pip-compile"
	@echo "  deactivate-env : Deactivate the virtual environment"
	@echo "  clean-env      : Clean the virtual environment"
	@echo "  run         		: Run the Flask application"
	@echo "  test        		: Run tests for the Flask application"
	@echo "  help        		: Show this help message"

.PHONY: all venv activate-env install-deps deactivate-env clean-env run test
