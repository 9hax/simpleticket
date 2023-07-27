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

###############################
# Clone GitHub Repository     #
###############################
echo ${green}Clone GitHub Repository${reset}

# Clone the GitHub Repo to /opt/simpleticket
sudo git clone https://github.com/9hax/simpleticket /opt/simpleticket

# make simpleticket directory accessible
sudo chmod 777 /opt/simpleticket -R

#####################################
# Create folder for upgrade backups #
#####################################
echo ${green}Create backup folder${reset}

# make the folder
mkdir /opt/simpleticket_backups

# make simpleticket_backups directory accessible
sudo chmod 777 /opt/simpleticket_backups -R

##################################
# Create User configuration File #
##################################
echo ${green}Create user configuration file${reset}

# copy stock config file to userconfig.py. this is in te gitignore, so git should never touch it.
cp /opt/simpleticket/config.py /opt/simpleticket/userconfig.py

#######################
# Python dependencies #
#######################
echo ${green}Python dependencies setup${reset}

# move to simpleticket directory o make the following steps easier
cd /opt/simpleticket

# install current requirements using pip3
pip3 install -r requirements.txt --break-system-packages

###############################
# Begin apache2 configuration #
###############################
echo ${green}Begin apache2 configuration${reset}

# Disable the default apache2 site
sudo a2dissite 000-default.conf

# Copy the simpleticket configuration file to the apache2 config directory
sudo cp /opt/simpleticket/simpleticket.conf /etc/apache2/sites-available

# Create simpleticket user for the wsgi process
sudo useradd -M simpleticket
sudo usermod -L simpleticket

# Enable the site by linking to sites-enabled
sudo a2ensite simpleticket.conf

# Reload apache2 web server to make site available
sudo service apache2 stop

####################
# Begin Flask init #
####################
echo ${green}Begin Flask init${reset}

# Start database migrations
flask db upgrade
flask db migrate -m "Initial installation"
flask db upgrade

#################
# Start website #
#################
echo ${green}Start website${reset}

# Start apache2
sudo service apache2 start

echo ${green}You can set up SimpleTicket with the file /opt/simpleticket/config.py and smtpsetup.py.${reset}
