#!/usr/bin/env bash

set -e
set -x

bash ./scripts/test-files.sh
# It seems xdist-pytest ensures modified sys.path to import relative modules in examples keeps working
pytest --cov-config=.coveragerc --cov --cov-report=term-missing -o console_output_style=progress --numprocesses=auto ${@}
