#!/usr/bin/env bash

set -e
set -x

mypy --install-types --non-interactive typer
black typer tests docs_src --check
isort typer tests docs_src --check-only
