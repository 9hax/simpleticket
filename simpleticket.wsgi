# Import sys and os for path manipulation
import sys, os

# Change into the SimpleTicket Install Directory so we find all imports and language files.
os.chdir('/opt/simpleticket')

# Add all files in the SimpleTicket install Directory to the path, just to make sure we find all files we need.
sys.path.insert(0, '/opt/simpleticket')

# import the flask app as application so wsgi can access and load it
from simpleticket import app as application

