#!/bin/bash

green=`tput setaf 2`
reset=`tput sgr0`

# stop apache fto close the database file
echo ${green}Stopping apache...${reset}
sudo service apache2 stop

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

# Start apache2
echo ${green}Starting apache...${reset}
sudo service apache2 start
