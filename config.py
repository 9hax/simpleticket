# interface ip and port number to launch the ticket system on.
# setting 0.0.0.0 as the interface ip exposes the flask host on all available interfaces.
INTERFACE_IP = "0.0.0.0"
INTERFACE_PORT = "80"

#require login for reading and writing to tickets and to create new tickets?
REQUIRE_LOGIN = True

#the password salt used to salt the hashes for the database.
# warning! changing the password salt will make all passwords in the system invalid.
PASSWORD_SALT = "randomletters" 

#language that the web interface for simpleticket uses. en_EN is default.
LANGUAGE = "de_DE"
#the language system passes this string if it cannot find the default string for the specified language.
DEFAULT_STRING = "There should a a string here, but we couldn't read it from the language file database. Please report this to the devs at https://github.com/9hax/simpleticket"

#site name that is displayed in multiple places
SITE_NAME = "SimpleTicket Development Instance"