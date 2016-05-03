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

# NOTE: this script will run as root !

echo "add here your install commands.."

##e.g. add database
#mysql -u root -p"vagrant" -e ";CREATE DATABASE myapp; GRANT ALL ON myapp.* TO myapp@localhost IDENTIFIED BY 'mypass';FLUSH PRIVILEGES;"


## use this for php applications
### add apache config
#cp /vagrant/config/files/apache/myphpapp.conf /etc/apache2/sites-available/myapp.conf
### activate apache conf
#a2ensite myapp.conf



### copy application files 
#cp -R /git_home/src/. /home/vagrant/
### set rights
chown -R vagrant:vagrant /home/vagrant/



## use this for tomcat applications
### add apache config
#cp /vagrant/config/files/apache/mytomcatapp.conf /etc/apache2/sites-available/myapp.conf
### activate apache conf
#a2ensite myapp.conf
### add tomcat instance under /home/vagrant/tomcat
#su vagrant -c "cd ~/ && tomcat7-instance-create tomcat"
### change tomcatconfig
#cp /vagrant/config/files/tomcat/server.xml tomcat/conf/server.xml
#sed -i -e 's/JAVA_OPTS="-Djava.awt.headless=true -Xmx128M"/JAVA_OPTS="-Djava.awt.headless=true -Xmx512M"/' /home/vagrant/tomcat/bin/setenv.sh
### copy application files 
#cp -R /vagrant_data/example/java /home/vagrant/tomcat/webapps/ROOT
### set rights
#chown -R vagrant:vagrant /home/vagrant/tomcat/webapps
#chown vagrant:vagrant /home/vagrant/tomcat/conf/server.xml
#chown vagrant:vagrant /home/vagrant/tomcat/bin/setenv.sh
### start tomcat
#su vagrant -c "cd ~/tomcat && ./bin/startup.sh"
### for troubleshooting read tomcat logs under /home/vagrant/tomcat/logs

## use this for python web (!) applications
### add apache config
#cp /vagrant/config/files/apache/mypythonwebapp.conf /etc/apache2/sites-available/myapp.conf
### activate apache conf
#a2ensite myapp.conf
### create python virtualenv environment
#su vagrant -c "cd ~/ && mkdir -p ~/wsgi/env && cd ~/wsgi/env && virtualenv --no-site-packages ."
### copy application files 
#cp /vagrant_data/example/python/script.wsgi /home/vagrant/wsgi/env/script.wsgi
#mkdir /home/vagrant/wsgi/env/myapp/
### set rights
#chown vagrant:vagrant /home/vagrant/wsgi/env/script.wsgi
#chmod +x /home/vagrant/wsgi/env/script.wsgi
#chown -R vagrant:vagrant /home/vagrant/wsgi/env/myapp

# additional dependencies:
sudo pip3 install Flask

# disable default site
#a2dissite 000-default.conf

# restart apache
#service apache2 restart


## troubleshooting 

### if you have problems with memory try to add a swap file
#echo "add swap file..."
#dd if=/dev/zero of=/root/myswapfile bs=1M count=4096
#chmod 600 /root/myswapfile
#mkswap /root/myswapfile
#swapon /root/myswapfile
#sed "/\/root\/myswapfile/s/^/#/" -i /etc/fstab
#echo "/root/myswapfile   swap   swap   defaults   0 0" >> /etc/fstab



