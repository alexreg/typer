#!/usr/bin/env bash -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports typer tests docs_src

./scripts/format.sh
