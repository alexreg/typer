#!/usr/bin/env bash

python3 -m mkdocs build

cp ./docs/index.md ./README.md
