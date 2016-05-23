#!/bin/sh

echo "Start Server on Port:5000"

cd /git_home
sudo pip3 install -r requirements.txt
python3 timeline/__init__.py > /dev/null 2>&1 &

