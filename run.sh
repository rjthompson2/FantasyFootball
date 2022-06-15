#!/bin/bash

python setup.py build
python setup.py install
pip install .

run=$1
if [ -n "$1" ]; then
    python $run
fi