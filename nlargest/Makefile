PYTHON = python3
VENV = env
PYVENV = /usr/bin/pyvenv
PYVENVOPTS = --clear
PIP_BIN = pip
REQUIREMENTS = requirements.txt
PIP = .make-pip
ACTIVATE = $(VENV)/bin/activate

.PHONY: all clean test

all: $(VENV) $(PIP)

$(VENV):
	@printf -- '-- Initializing virtual environment ...\n'
	rm -f -- "$(PIP)"
	$(PYVENV) $(PYVENVOPTS) "$(VENV)"

$(PIP): $(REQUIREMENTS)
	@printf -- '-- Running pip to satisfy package dependencies ...\n'
	[ -r "$(ACTIVATE)" ] && . "$(ACTIVATE)"; $(PIP_BIN) install -r "$^"
	@touch "$@"

clean:
	@printf -- '-- Removing virtual environment and state file ...\n'
	rm -rf -- "$(VENV)" "$(PIP)"

test:
	@printf -- '-- Running tests ...\n'
	[ -r "$(ACTIVATE)" ] && . "$(ACTIVATE)"; $(PYTHON) -m unittest
