#!/usr/bin/env bash -e

if [[ -d 'dist' ]]; then
    rm -r dist
fi
if [[ -d 'site' ]]; then
    rm -r site
fi
