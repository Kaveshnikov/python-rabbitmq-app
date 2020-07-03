#!/bin/bash
set -e
# This file need for a pre-commit hook.
# The hook works only through script because mypy must be used from the same venv from sources are executed.
source "$WORKON_HOME/python-rabbitmq-app/bin/activate"
exec prospector
