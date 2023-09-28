# SimpleTicket Ticket Management System

SimpleTicket is a simple ticket system built using python, flask and apache-wsgi.

Its designed to be easy to use and set up, providing a fast, easy and portable solution for smaller teams.

The code is designed to be very lightweight, allowing the ticket system to run with acceptable performance even on small single board computers like the RaspberryPi Zero.

## TODOS

Easier password resets

## Installation

You can easily install SimpleTicket on any debian System using the provided install script.

The default path for the installation is /opt/simpleticket and cannot be changed for now
(If you implement this, please create a pull request and let me know!).

The install script can be run using this command: (sudo and curl are required!)

    curl -s https://raw.githubusercontent.com/9hax/simpleticket/main/install_simpleticket.sh | sudo bash

This will install apache2, git, python3 and some python3 libraries.
It will also disable the default apache2 welcome page which runs on port 80 to stop it from showing up when not called with the correct domain.

Please put your configuration into userconfig.py to prevent version merging issues during upgrades.

## Usage

Just open the Web interface at Port 80! 
If your Hostname is ``ticket``, the url would be http://ticket:80.

You can also implement Port 443 with HTTPS by editing the simpleticket.conf file in /etc/apache2/sites-available. 

TODO: Add sample SSL VirtualHost Configuration File and automatically copy it to Destination in Install and Upgrade Script

## Creating the first Admin User

To create an admin user, just visit /add-admin to open a signup form.

For security, this is disabled by default. To enable it temporarily, run ``touch /opt/simpleticket/_CREATE_ADMIN_ALLOWED`` . 
This path can be changed in config.py.  

Please make sure to delete the _CREATE_ADMIN_ALLOWED file after adding all the administrator accounts you need!
Leaving the file present will allow anyone to create their own admin users without authentication.

## Creating normal users

To create a normal user, visit /add-user while logged in as an admin.

This will open the same user creation form as /add-admin, but the created user will only have base privileges.

# Contributing

Feel free to send code my way. The best way to do this is using a pull request here on GitHub.

# Security

For reporting security vulnerabilities to the project, please refer to my [security contact information file](https://9h.ax/security.txt).
Learn more at https://securitytxt.org/ !
