#!/bin/sh

export PYTHONPATH=$(pwd):$PYTHONPATH
find test/ -name "__pycache__" -type d -exec rm -rf {} \;
find test/ -name "*.pyc" -type f -exec rm -rf {} \;
find test/ -name ".coverage*" -type f -exec rm -rf {} \;

startingDir=$(pwd)
rm -rf temp
for dir in $(find test/ -type d)
do
    dir=${dir%*/}
    cd ${dir}; coverage run --omit "${startingDir}/venv*" -p -m unittest discover .; cd ${startingDir}
done

mkdir -p temp
find test/ -name ".coverage*" -exec cp {} temp/ \;
cd temp && coverage combine && coverage html --rcfile=${startingDir}/.coveragerc && cd ${startingDir}

xdg-open temp/htmlcov/index.html 

exit 0

