#!/bin/bash

green=`tput setaf 2`
reset=`tput sgr0`

# stop apache fto close the database file
echo ${green}Stopping apache...${reset}
sudo service apache2 stop

# make backup of the current system
echo ${green}Creating backup...${reset}
mkdir /opt/simpleticket_backups/$(date +"%d-%m-%Y")
cp /opt/simpleticket/* /opt/simpleticket_backups/$(date +"%d-%m-%Y") -R

# Pull changes
echo ${green}Pulling updates...${reset}
cd /opt/simpleticket
sudo -u simpleticket git pull


# Start database migrations
echo ${green}Running database migrations...${reset}
sudo -u simpleticket python3 -m flask db upgrade
sudo -u simpleticket python3 -m flask db migrate -m "SimpleTicket Update"
sudo -u simpleticket python3 -m flask db upgrade
sudo -u simpleticket python3 -m flask db migrate -m "SimpleTicket Update"

# Start apache2
echo ${green}Starting apache...${reset}
sudo service apache2 start
