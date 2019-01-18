#!/bin/sh

export PYTHONPATH=$(pwd):$PYTHONPATH
find test/ -name "__pycache__" -type d -exec rm -rf {} \;
find test/ -name "*.pyc" -type f -exec rm -rf {} \;
find -name ".coverage.*" -type f -exec rm -rf {} \;
rm -rf htmlcov
rm .coverage

startingDir=$(pwd)

coverage run -m unittest discover test

coverage run --concurrency=multiprocessing e2e_test/runner.py

coverage combine
coverage html
xdg-open htmlcov/index.html

exit 0

