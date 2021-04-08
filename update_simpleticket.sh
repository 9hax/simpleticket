#!/bin/bash

# stop apache fto close the database file
sudo service apache2 stop

# Pull changes
cd /opt/simpleticket
sudo git pull

# make simpleticket directory accessible
sudo chmod 777 /opt/simpleticket -R

# Start database migrations
flask db upgrade

# Start apache2
sudo service apache2 start