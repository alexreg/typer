#!/usr/bin/env bash -ex

mypy --install-types --non-interactive typer
black typer tests docs_src --check
isort typer tests docs_src --check-only
