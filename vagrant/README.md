lampX
=====

Vagrant example for a simple LAMP-Stack (http://en.wikipedia.org/wiki/LAMP_%28software_bundle%29)
To get more information about vagrant visit http://vagrantup.com/

Please install the following requirements for your operating system:
- VirtualBox 4.3.14+  (http://virtualbox.org) 
- Vagrant 1.6.5+ (http://vagrantup.com) 
- under Windows: git-scm (http://git-scm.com/)

The example contains:
 - Ubuntu 14.04 Server
 - PHP
 - Java, Tomcat, mod_jk
 - Python, mod_wsgi

Getting started: 
 - Start VM: 
   - cd /path/to/this/dir
   - vagrant up
     - the first run of this command downloads a basic virtual box (VB) and installs within VB all dependencies you need to run your project ("provisionising"). 
     - it can take long in the first run
 - Open Browser in your host: http://localhost:8080

Customization
 - Customize install script (THISDIR/config/shell/custom.sh)
 - Add your application source in source folder 
 - Customize apache config (THISDIR/config/files/apache/)
 - Destroy and start VM
   - cd /path/to/this/dir
   - vagrant destroy
   - vagrant up
 - To turn off the VB: vagrant halt
 - To navigate into VB: vagrant ssh
