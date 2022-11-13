#!/usr/bin/env bash -e

python3 -m mkdocs build

cp ./docs/index.md ./README.md
