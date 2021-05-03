###################################
# SIMPLETICKET CONFIGURATION FILE #
###################################

###############################################
# Flask Development Environment Configuration #
###############################################
# This is not used when using the WSGI mod for apache.

# interface ip and port number to launch the ticket system on.
# setting 0.0.0.0 as the interface ip exposes the flask host on all available interfaces.
INTERFACE_IP = "0.0.0.0"
INTERFACE_PORT = "80"

######################################
# General SimpleTicket Configuration #
######################################

# Require login for opening the home page?
# This will automatically redirect to login if not logged in already.
REQUIRE_LOGIN = True

# Language file that is used for the web interface.
# The language file has .json as a file format and is located in the lang directory at the simpleticket install path root.
LANGUAGE = "en_EN"

# Site Name (Displayed in header, title, about page...)
SITE_NAME = "SimpleTicket Development Instance"

# Needed for sessions. Change this to logout all users.
SECRET_KEY = 'm-_2hz7kJL-oOHtwKkI5ew'

# create-admin-user file path
CREATE_ADMIN_FILE = "_CREATE_ADMIN_ALLOWED"

# Custom Properties go here.
# Reference the manual for more information on custom config properties.

TIMEFORMAT = "%H:%M:%S, %d.%m.%Y"