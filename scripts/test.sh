#!/usr/bin/env bash

set -e
set -x

bash ./scripts/test-files.sh
# Use xdist-pytest --forked to ensure modified sys.path to import relative modules in examples keeps working
coverage run -m pytest -o console_output_style=progress --forked --numprocesses=auto ${@}
