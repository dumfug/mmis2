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
DEPENDENCIES_APACHE="apache2"
DEPENDENCIES_PHP="php5 php5-mysql php5-curl php5-gd php5-mcrypt"
DEPENDENCIES_PYTHON="python python3-pip python3-matplotlib python3-pandas python-pygraphviz python-virtualenv libapache2-mod-wsgi"
DEPENDENCIES_JAVA="openjdk-6-jdk"
DEPENDENCIES_TOMCAT="tomcat7-user libapache2-mod-jk"
DEPENDENCIES_MYSQL="mysql-server phpmyadmin"


## configuration for mysql
#echo mysql-server mysql-server/root_password select "vagrant" | debconf-set-selections
#echo mysql-server mysql-server/root_password_again select "vagrant" | debconf-set-selections

## configuration for phpmyadmin
#echo 'phpmyadmin phpmyadmin/dbconfig-install boolean false' | debconf-set-selections
#echo 'phpmyadmin phpmyadmin/reconfigure-webserver multiselect apache2' | debconf-set-selections
#echo 'phpmyadmin phpmyadmin/app-password-confirm password vagrant' | debconf-set-selections
#echo 'phpmyadmin phpmyadmin/mysql/admin-pass password vagrant' | debconf-set-selections
#echo 'phpmyadmin phpmyadmin/password-confirm password vagrant' | debconf-set-selections
#echo 'phpmyadmin phpmyadmin/setup-password password vagrant' | debconf-set-selections
#echo 'phpmyadmin phpmyadmin/database-type select mysql' | debconf-set-selections
#echo 'phpmyadmin phpmyadmin/mysql/app-pass password vagrant' | debconf-set-selections
#echo 'dbconfig-common dbconfig-common/mysql/app-pass password vagrant' | debconf-set-selections
#echo 'dbconfig-common dbconfig-common/mysql/app-pass password' | debconf-set-selections
#echo 'dbconfig-common dbconfig-common/password-confirm password vagrant' | debconf-set-selections
#echo 'dbconfig-common dbconfig-common/app-password-confirm password vagrant' | debconf-set-selections
#echo 'dbconfig-common dbconfig-common/app-password-confirm password vagrant' | debconf-set-selections
#echo 'dbconfig-common dbconfig-common/password-confirm password vagrant' | debconf-set-selections

echo "update.."
sudo apt-get update

echo "install dependencies..."
apt-get install -y $DEPENDENCIES_BASE
apt-get install -y $DEPENDENCIES_PYTHON
#apt-get install -y $DEPENDENCIES_APACHE
#apt-get install -y $DEPENDENCIES_PHP
#apt-get install -y $DEPENDENCIES_JAVA
#apt-get install -y $DEPENDENCIES_TOMCAT
#apt-get install -y $DEPENDENCIES_MYSQL

echo "various settings..."
usermod -a -G adm vagrant

#echo "activate apache modules..."
#a2enmod proxy
#a2enmod proxy_http
#a2enmod rewrite
#a2enmod headers
#a2enmod wsgi
#a2enmod jk

#echo "restart apache..."
#service apache2 restart

