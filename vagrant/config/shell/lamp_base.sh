#!/bin/sh
if cd "`dirname \"$0\"`"; then
    absdirpath=`pwd`
    cd "$OLDPWD" || exit 1
else
    exit 1
fi
SCRIPTDIR=$absdirpath
BASEDIR=$(dirname $SCRIPTDIR)
SCRIPTNAME=$(basename $0 .sh)

echo ""
echo "===== $SCRIPTNAME ====="
echo ""

## PACKAGES

DEPENDENCIES_BASE="curl zip bzip2 vim lynx ntp git subversion git-svn"
DEPENDENCIES_PYTHON="python python3.5 python-dev python3.5-dev python-virtualenv"

echo "add repos..."
sudo add-apt-repository ppa:fkrull/deadsnakes

echo "update.."
sudo apt-get update

echo "install dependencies..."
apt-get install -y $DEPENDENCIES_BASE
apt-get install -y $DEPENDENCIES_PYTHON

echo "various settings..."
usermod -a -G adm vagrant
