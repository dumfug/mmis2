#!/bin/bash

cd /timeline/git

echo "create virtual environment"
virtualenv -p /usr/bin/python3.5 ~/venv

echo "activate virtual environment"
source ~/venv/bin/activate

echo "install requirements using pip"
pip install -r requirements.txt

echo "start timeline server on port 5000"
python3.5 timeline/__init__.py > /dev/null 2>&1 &
