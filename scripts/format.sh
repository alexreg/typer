#!/usr/bin/env bash -ex

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place docs_src typer_cloup tests --exclude=__init__.py
black typer_cloup tests docs_src
isort typer_cloup tests docs_src
