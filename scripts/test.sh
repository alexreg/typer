#!/usr/bin/env bash -ex

./scripts/test-files.sh

# Use `xdist-pytest --forked` to ensure modified `sys.path` for importing relative modules in examples
pytest --cov-config=.coveragerc --cov --cov-report=term-missing -o console_output_style=progress --numprocesses=auto "$@"
