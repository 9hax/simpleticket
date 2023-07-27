#!/bin/bash

#print color
green=`tput setaf 2`
reset=`tput sgr0`

###############################
# Install Packages            #
###############################
echo ${green}Install Packages${reset}

sudo apt update

sudo apt install apache2 git nano -y
sudo apt install python3 python3-pip -y
sudo apt install libapache2-mod-wsgi-py3 -y

# Create simpleticket user for the wsgi process
sudo useradd simpleticket -c "SimpleTicket WSGI Daemon Owner" -r -m
sudo usermod -L simpleticket

###############################
# Prepare installation folder #
###############################

sudo chmod 777 /opt 

###############################
# Clone GitHub Repository     #
###############################
echo ${green}Clone GitHub Repository${reset}

# Clone the GitHub Repo to /opt/simpleticket
sudo -u simpleticket git clone https://github.com/9hax/simpleticket /opt/simpleticket

# make simpleticket directory accessible
sudo chown simpleticket:simpleticket /opt/simpleticket* -R

#####################################
# Create folder for upgrade backups #
#####################################
echo ${green}Create backup folder${reset}

# make the folder
sudo -u simpleticket mkdir /opt/simpleticket_backups

##################################
# Create User configuration File #
##################################
echo ${green}Create user configuration file${reset}

# copy stock config file to userconfig.py. this is in the gitignore, so git should never touch it.
sudo -u simpleticket cp /opt/simpleticket/config.py /opt/simpleticket/userconfig.py

#######################
# Python dependencies #
#######################
echo ${green}Python dependencies setup${reset}

# move to simpleticket directory o make the following steps easier
cd /opt/simpleticket

# install current requirements using pip3
sudo -u simpleticket python3 -m pip install -r requirements.txt --break-system-packages

###############################
# Begin apache2 configuration #
###############################
echo ${green}Begin apache2 configuration${reset}

# Disable the default apache2 site
sudo a2dissite 000-default.conf

# Copy the simpleticket configuration file to the apache2 config directory
sudo cp /opt/simpleticket/simpleticket.conf /etc/apache2/sites-available

# Enable the site by linking to sites-enabled
sudo a2ensite simpleticket.conf

# Reload apache2 web server to make site available
sudo service apache2 stop

####################
# Begin Flask init #
####################
echo ${green}Begin Flask init${reset}

# Start database migrations
sudo -u simpleticket python3 -m flask db upgrade
sudo -u simpleticket python3 -m flask db migrate -m "Initial installation"
sudo -u simpleticket python3 -m flask db upgrade

#################
# Start website #
#################
echo ${green}Start website${reset}

# Start apache2
sudo service apache2 start

echo ${green}You can set up SimpleTicket with the file /opt/simpleticket/userconfig.py and smtpsetup.py.${reset}
