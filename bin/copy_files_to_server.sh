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

echo "remove old files..."
rm -rf ../vagrant/src/*

echo "copy files"
cp -R ../src/. ../vagrant/src/

cd ../vagrant
vagrant ssh -c "/vagrant/config/service/start_backend.sh"



