#!/bin/sh
export PYTHONPATH=$(pwd):$PYTHONPATH

python e2e_test/runner.py
