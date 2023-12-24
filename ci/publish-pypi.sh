#!/bin/sh
apk add git

git describe --tags --exact-match
if [ $? -ne 0 ]; then
    echo "Not a tagged commit. Skipping."
    exit 0;
fi

pip install build twine
python3 -m build
python3 -m twine upload --non-interactive --repository testpypi dist/*
