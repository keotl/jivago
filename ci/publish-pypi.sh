#!/bin/sh
apk add git
pip install git

pip install build twine
python3 -m build
python3 -m twine upload --non-interactive --repository testpypi dist/*
