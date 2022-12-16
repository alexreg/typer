#!/usr/bin/env bash -ex

cd ./site

if [[ -f docs.zip ]]; then
    rm -rf docs.zip
fi
zip -r docs.zip ./
