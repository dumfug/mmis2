#!/bin/sh


cd /git_home

echo "Install dependencies"
sudo pip3 install -r requirements.txt

echo "Start Server on Port:5000"
python3 timeline/__init__.py > /dev/null 2>&1 &

