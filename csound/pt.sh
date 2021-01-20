#!/usr/bin/env bash

# pt: paste-n-test

pbpaste > test_$1.csd
csound test_$1.csd

