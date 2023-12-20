#!/bin/sh
pip install -r requirements.txt
sh run_tests.sh
sh run_e2e_tests.sh
