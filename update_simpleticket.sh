#!/bin/bash

green=`tput setaf 2`
reset=`tput sgr0`

# stop apache fto close the database file
echo ${green}Stopping apache...${reset}
sudo service apache2 stop

# make backup of the current system
echo ${green}Creating backup...${reset}
mkdir /opt/simpleticket_backups/$(date +"%d-%m-%Y")
cp /opt/simpleticket /opt/simpleticket_backups/$(date +"%d-%m-%Y") -R

# Pull changes
echo ${green}Pulling updates...${reset}
cd /opt/simpleticket
sudo git pull

# make simpleticket directory accessible
echo ${green}Changing directory perms...${reset}
sudo chmod 777 /opt/simpleticket -R

# Start database migrations
echo ${green}Running database migrations...${reset}
flask db upgrade
flask db migrate -m "SimpleTicket Update"

# Copy config file from backup in case git decides to overwrite it during pull
cp /opt/simpleticket_backups/$(date +"%d-%m-%Y")/config.py /opt/simpleticket

# Start apache2
echo ${green}Starting apache...${reset}
sudo service apache2 start
