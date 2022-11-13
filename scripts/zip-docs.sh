#!/usr/bin/env bash -ex

if [[ -f docs.zip ]]; then
    rm -rf docs.zip
fi
zip -r docs.zip ./site
