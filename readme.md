# SimpleTicket Ticket Management System

SimpleTicket is a simple ticket system built using flask and wsgi.

Its designed to be easy to use and set up, providiing a fast, easy and portable solution for smaller teams.

It even runs on a [Raspberry Pi](https://raspberrypi.org)!

## Installation

You can easily install SimpleTicket on any debian System using the provided install script.

The default path for the installation is /opt/simpleticket and cannot be changed for now
(If you implement this, please create a pull request and let me know!).

The install script can be run using this command:

    curl -s https://raw.githubusercontent.com/9hax/simpleticket/main/install_simpleticket.sh | sudo bash

This will install apache2, git, python3 and some python3 libraries.
It will also disable the default apache2 welcome page which runs on port 80 to stop it from showing up when not called with the correct domain.

## Usage

Just open the Web interface at Port 80! 
If your Hostname is ticket, the url would be (```http://ticket:80```)[http://ticket:80].
The rest of the process should be very simple to understand.
