#!/bin/bash

###############################
# Install Packages            #
###############################

sudo apt update

sudo apt install apache2 git nano -y
sudo apt install python3 python3-pip -y
sudo apt install libapache2-mod-wsgi-py3 -y

###############################
# Clone GitHub Repository     #
###############################

# Clone the GitHub Repo to /opt/simpleticket
sudo git clone https://github.com/9hax/simpleticket /opt/simpleticket

# make simpleticket directory accessible
sudo chmod 777 /opt/simpleticket -R

###############################
# Begin user configuration    #
###############################

# Start a nano editor with the simpleticket configuration file, let the user edit the default values
sudo nano /opt/simpleticket/config.py

###############################
# Begin apache2 configuration #
###############################

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

# Start database migrations
flask db upgrade

#################
# Start website #
#################

# Start apache2
sudo service apache2 start