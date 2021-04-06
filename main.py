# main files for a simple open source ticketing system
# written from scratch by 9hax
# this uses the flask framework

from flask import *
from config import *

app = Flask(__name__)

@app.route('/')
def printTickets():
    return render_template('index.html', sitename=SITE_NAME, username="Textuser")

app.run(debug = True)